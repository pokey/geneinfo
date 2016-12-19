import asyncio
from itertools import zip_longest
import os
import os.path

from bs4 import BeautifulSoup
from tqdm import tqdm
import aiohttp
from jinja2 import Environment, PackageLoader

from pubmedasync.fetch import Fetcher

from geneinfo.make_table import make_table
from geneinfo.process import extract_paper_info

env = Environment(loader=PackageLoader('geneinfo', 'templates'))
gene_template = env.get_template('gene.html')


async def process_gene(session, pbar, gene, terms, do_gene_files, extra_term):
    results = await asyncio.gather(*[
        process_search(session, pbar, gene, term, do_gene_files, extra_term)
        for term in terms
    ])
    if do_gene_files:
        with open('html/genes/{}.html'.format(gene), 'w') as out:
            out.write(gene_template.render(
                gene=gene,
                terms=[
                    dict(
                        name=term,
                        papers=papers,
                        count=count,
                        i=i
                    )
                    for i, (term, (count, papers))
                    in enumerate(zip(terms, results))
                ]
            ))
    return [count for (count, papers) in results]


async def process_search(session, pbar, gene, term, do_gene_files, extra_term):
    fetcher = Fetcher(session, '{} {} {}'.format(gene, term, extra_term),
                      max_papers=500)
    await fetcher.search()

    # Iterate through all the pages and extract all authors
    results = []
    if do_gene_files:
        for data in await asyncio.gather(*fetcher.get_pages()):
            soup = BeautifulSoup(data, "lxml")
            papers = soup.find_all('pubmedarticle')

            for paper in papers:
                results.append(extract_paper_info(paper))
    pbar.update(1)
    return (fetcher.total, results)


def grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)


# Get list of results
async def process_genes(genes, terms, do_gene_files, extra_term):
    os.makedirs('html/genes', exist_ok=True)
    if do_gene_files:
        genes = [
            gene
            for gene in genes
            if not os.path.exists('html/genes/{}.html'.format(gene))
        ]
    async with aiohttp.ClientSession() as session:
        with tqdm(total=len(genes) * len(terms), unit='query') as pbar:
            groups = grouper(10, genes)
            gene_totals = []
            for group in groups:
                gene_totals += await asyncio.gather(*[
                    process_gene(session, pbar, gene, terms, do_gene_files,
                                 extra_term)
                    for gene in group
                    if gene is not None
                ])
        with open('totals.csv', 'w') as out:
            out.write('gene,' + ','.join(terms) + '\n')
            for gene, totals in zip(genes, gene_totals):
                row = [gene] + [str(total) for total in totals]
                out.write(','.join(row) + '\n')
    make_table()
