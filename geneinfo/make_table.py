import csv

from jinja2 import Environment, PackageLoader

env = Environment(loader=PackageLoader('geneinfo', 'templates'))
index_template = env.get_template('index.html')


def make_table():
    with open('totals.csv') as f:
        reader = csv.reader(f)
        headers = next(reader)
        gene_totals = list(reader)

    genes = [
        dict(
            name=totals[0],
            totals=[
                dict(
                    i=i,
                    val=val
                )
                for i, val in enumerate(totals[1:])
            ]
        )
        for totals in gene_totals
    ]
    with open('html/index.html', 'w') as out:
        out.write(index_template.render(
            headers=headers,
            genes=genes
        ))
