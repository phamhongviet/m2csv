#!/usr/bin/env python2
# This little program convert mysql output into csv file
# Usage:
# mysql -u u1 -p db1 -e 'select * from table1\G' | m2csv
#
# mysql -u u1 -p db1 -e 'select * from table1\G' > result.txt
# m2csv -i result.txt -o result.csv

from __future__ import print_function
import getopt
import csv
import sys
import fileinput

class m2csv:
# read input from file object input_fo
# transform into CSV
# write result to file object output_fo
	def convert(self, input_fo, output_fo):
		# guess header using the first record
		line1 = input_fo.readline()
		if not self._is_record_seperator(line1):
			print("ERROR: I'm expecting a header like this:", file=sys.stderr)
			print("       *************************** n. row ***************************", file=sys.stderr)
			print("ERROR: Format is not supported. Aborted")
			return 1
		# search for next record seperator
		next_rs = False
		header = []
		row1 = {}
		while not next_rs:
			line = input_fo.readline()
			if self._is_record_seperator(line):
				next_rs = True
			else:
				line = line.strip()
				colon = line.index(':')
				field_name = line[0:colon]
				header.append(field_name)
				row1[field_name] = line[colon+2:]
		# start writing CSV file
		writer = csv.DictWriter(output_fo, fieldnames=header)
		# write header and first row
		writer.writerow( dict([ (field, field) for field in header ])) # python 2.6 compatible
		writer.writerow(row1)
		del row1

		# convert the rest of the file
		row = {}
		for line in input_fo:
			if self._is_record_seperator(line):
				writer.writerow(row)
				del row
				row = {}
			else:
				line = line.strip()
				colon = line.index(':')
				field_name = line[0:colon]
				row[field_name] = line[colon+2:]
		writer.writerow(row)
		del row
				
# check if string is a record seperator
# look like this:
# *************************** 1. row ***************************
	def _is_record_seperator(self, s):
		s = s.strip()
		if len(s) < 62:
			return False
		if s[0:28] != '*************************** ':
			return False
		if s[-33:-1] != '. row **************************':
			return False
		return True


if __name__ == "__main__":
# Get input and output file name
# If not specify, use STDIN and STDOUT
	output_file = ''
	input_file = ''
	verbose = False
	opts, _ = getopt.getopt(sys.argv[1:], "o:i:v")
	for flag, value in opts:
		if flag == '-o':
			output_file = value
		elif flag == '-i':
			input_file = value
		elif flag == '-v':
			verbose = True
		else:
			assert False, "Unhandled option: %s" % flag

# Define input file object
	if not input_file:
		if verbose:
			print("Using STDIN for input", file=sys.stderr)
		input_fo = fileinput.input()
	else:
		if verbose:
			print("Reading from %s" % input_file, file=sys.stderr)
		input_fo = open(input_file, 'r')

# Define output file object
	if not output_file:
		if verbose:
			print("Using STDOUT for output", file=sys.stderr)
		output_fo = sys.stdout
	else:
		if verbose:
			print("Writing to %s" % output_file, file=sys.stderr)
		output_fo = open(output_file, 'w')

# Convert to CSV
	converter = m2csv()
	converter.convert(input_fo, output_fo)

# Clean up
	input_fo.close()
	output_fo.close()
