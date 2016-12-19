# -*- coding: utf-8 -*-

import asyncio

import click

from geneinfo import process_genes


def process_file(f):
    return [
        line.strip()
        for line in f
    ]


@click.command()
@click.option('--genes', help='file containing list of genes',
              type=click.File('r'))
@click.option('--terms', help='file containing list of search terms',
              type=click.File('r'))
def main(genes, terms):
    """Console script for geneinfo"""
    loop = asyncio.get_event_loop()
    loop.run_until_complete(process_genes(process_file(genes),
                                          process_file(terms)))
    loop.close()