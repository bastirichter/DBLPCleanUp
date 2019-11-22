# DBLPCleanUp
Cleans up DBLP entries in bib file

This tool scans the .bib file given as argument for DBLP citekeys (e.g. DBLP:journals/iandc/Knuth65).
It then downloads the bib entries in the selected style (condensed, standard, cross ref) from DBLP and saves them in a new bib file. 
Non-DBLP entries are copied. Duplicates (based on citekey) are skipped. 

Download function based on https://github.com/shack/dblpbib/blob/master/dblpbib.py
