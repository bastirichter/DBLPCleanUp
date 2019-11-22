import argparse
import urllib.request
import bibtexparser

#condensed 0
#standard 1
#cross ref 2
bib_style = 1

def download_dblp(key):
    url = 'http://dblp.uni-trier.de/rec/bib{}/{}.bib'.format(bib_style, key)
    response = urllib.request.urlopen(url)
    data = response.read()
    text = data.decode('utf-8')
    return text



parser = argparse.ArgumentParser(
        description="rebuild DBLP entries in *.bib file",
        epilog="""This tool scans the .bib file given as argument for DBLP citekeys (e.g. DBLP:journals/iandc/Knuth65).
               It then downloads the bib entries from DBLP and saves them in a new bib file. Non-DBLP entries are copied. 
               Duplicates (based on citekey) are skipped.""")

parser.add_argument('infile', metavar="file", type=str, help='input bib file to scan for citations')
parser.add_argument("-o", "--output",  required=True, help="output bib file to write missing entries to", type=str)
parser.add_argument("-s", "--style", required=False, help="Style of bib code: 0 condensed, 1 standard (default), 2 cross ref", type=int)
args = parser.parse_args()

bib_style = 1 if args.style == None else args.style

print("Style set to " + str(bib_style))

with open(args.infile) as input_file:
    bib_database = bibtexparser.load(input_file)

keys_done = []
dblp_entries = []
non_dblp_entries = []
num_skipped = 0

for entry in bib_database.get_entry_list():
    id = entry['ID']

    if not (id in keys_done):
        if id[0:4] == "DBLP":
            print("downloading " + id)
            bib_str = download_dblp(id[5:])
            temp_db = bibtexparser.loads(bib_str)
            dblp_entries.append(temp_db.entries[0])
        else:
            non_dblp_entries.append(entry)

        keys_done.append(id)

    else:
        num_skipped += 1
        print(id + " skipped")

print("#DBLP entries = " + str(len(dblp_entries)))
print("#non DBLP entries = " + str(len(non_dblp_entries)))
print("#entries skipped = " + str(num_skipped))

print("writing new bib...", end="")
#dblp_entries.extend(non_dblp_entries)
new_bib = bibtexparser.bibdatabase.BibDatabase()
new_bib.entries.extend(dblp_entries)
new_bib.entries.extend(non_dblp_entries)

with open(args.output, "a") as output_file:
    bibtexparser.dump(new_bib, output_file)

print('done')