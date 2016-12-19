import asyncio
import os.path

from bs4 import BeautifulSoup
from tqdm import tqdm
import aiohttp
from jinja2 import Environment, PackageLoader

from pubmedasync.fetch import Fetcher
from geneinfo.process import extract_paper_info

env = Environment(loader=PackageLoader('geneinfo', 'templates'))
gene_template = env.get_template('gene.html')
index_template = env.get_template('index.html')


async def process_gene(session, pbar, gene, terms):
    results = await asyncio.gather(*[
        process_search(session, pbar, gene, term)
        for term in terms
    ])
    with open('html/genes/{}.html'.format(gene), 'w') as out:
        out.write(gene_template.render(
            gene=gene,
            terms=[
                dict(
                    name=term,
                    papers=papers,
                    count=count
                )
                for term, (count, papers) in zip(terms, results)
            ]
        ))


async def process_search(session, pbar, gene, term):
    fetcher = Fetcher(session, '{} {} cancer'.format(gene, term),
                      max_papers=500)
    await fetcher.search()

    # Iterate through all the pages and extract all authors
    results = []
    for data in await asyncio.gather(*fetcher.get_pages()):
        soup = BeautifulSoup(data, "lxml")
        papers = soup.find_all('pubmedarticle')

        for paper in papers:
            results.append(extract_paper_info(paper))
    pbar.update(1)
    return (fetcher.total, results)


# Get list of results
async def process_genes(genes, terms):
    with open('html/index.html', 'w') as out:
        out.write(index_template.render(genes=genes))
    genes = [
        gene
        for gene in genes
        if not os.path.exists('html/genes/{}.html'.format(gene))
    ]
    async with aiohttp.ClientSession() as session:
        with tqdm(total=len(genes) * len(terms), unit='query') as pbar:
            await asyncio.gather(*[
                process_gene(session, pbar, gene, terms)
                for gene in genes
            ])
