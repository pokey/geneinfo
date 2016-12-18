import asyncio
import itertools

from bs4 import BeautifulSoup
from tqdm import tqdm
import aiohttp

from pubmedasync.fetch import Fetcher
from geneinfo.process import extract_paper_info


async def process_search(session, pbar, gene, term):
    fetcher = Fetcher(session, '{} {} cancer'.format(gene, term))
    await fetcher.search()

    # Iterate through all the pages and extract all authors
    results = []
    for data in await asyncio.gather(*fetcher.get_pages()):
        soup = BeautifulSoup(data, "lxml")
        papers = soup.find_all('pubmedarticle')

        for paper in papers:
            results.append(extract_paper_info(paper))
    pbar.update(1)
    return results


# Get list of results
async def process_genes(genes, terms):
    async with aiohttp.ClientSession() as session:
        with tqdm(total=len(genes) * len(terms), unit='term') as pbar:
            results = await asyncio.gather(*[
                process_search(session, pbar, gene, term)
                for gene, term in itertools.product(genes, terms)
            ])
            print(results)
