Gene info
=============

Uses [Entrez
api](https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.ESearch)
to search for combinations of genes with various terms and outputs html.

Installing on OS X
------------------

1. Install [Homebrew](http://brew.sh/)
1. From a terminal, run

   ```
   brew install python3
   pip3 install -e .
   ```

Running on OS X
---------------

Run

```
geneinfo --genes genes.txt --terms terms.txt --extra-term regulation
```

Where `genes.txt` is of the format

```
HDG1
GED
IHD4
```

and `terms.txt` is of the format

```
lung function
tissue development
```

Output will be in the `html` directory, and a csv will be at `totals.csv`.
