#!/usr/bin/env python

"""merge_sheets.py: Takes an excel workbook containing multiple sheets of digital object metadata, and outputs a single consolidated CSV file."""

import os
import xlrd
import unicodecsv as csv

# Update the following 2 variables with filepaths for:
## (1) your existing metadata workbook, e.g. "/Users/wonderwoman/Desktop/metadata_master.xlsx"
## (2) the filepath where you want the consolidated CSV to be saved, e.g. "/Users/wonderwoman/Desktop/metadata_merged.csv"
meta_book = "MY_METADATA_WORKBOOK.xlsx"
output = "MY_SUPER_AWESOME_MERGED_CSV.csv" 

# Store item data and fieldnames.
items = []
fieldnames = []

# check if output file exists. Rename if it does.
def check_file(o):
    if os.path.exists(o):
        o = rename(o)
    else:
        o_split = o.split('.')
        if o_split[-1] != 'csv':
            o = o + ".csv"
    return o

def rename(o):
    o_split = o.split('.')
    lastchar = o_split[0][-1]
    if lastchar.isdigit():
        lastchar = int(lastchar) + 1
        o = o_split[0][:-1] + str(lastchar) + '.csv'
        if os.path.exists(o):
            return rename(o)
        else:
            return o
    else:
        o = o_split[0] + '_1.csv'
        if os.path.exists(o):
            return rename(o)
        else:
            return o

with xlrd.open_workbook(meta_book) as wb:
	sheets = wb.sheets()
	fieldnames = sheets[0].row_values(0)
	print fieldnames
	# put row contents into dicts, using fields as keys
	for s in sheets:
		for rownum in range(s.nrows):
			fields = (s.row_values(0))
			vals = (s.row_values(1))
			item_dict = dict(zip(fields,vals))
			items.append(item_dict)

for i in items:
	vals = i.values()
	for v in vals:
		if type(v) == float:
			v = str(v)
		v = v.encode("utf-8")
		v = v.replace("\'", "\"")

out = check_file(output)
with open(out, 'wb') as outfile:
	writer = csv.DictWriter(outfile, fieldnames=fieldnames, extrasaction='ignore')
	writer.writeheader()
	writer.writerows(items)