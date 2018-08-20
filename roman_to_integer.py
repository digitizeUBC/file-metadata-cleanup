#!/usr/bin/env python

import os
import shutil
import re
import argparse
import sys

'''Edited 2018-07-23 by R Dickson (@rebeckson)

For use when someone decides to name files using transcribed Roman numerals. (Hopefully never again!)

BEFORE YOU RUN: make sure the source folder is named using the object's digital identifier, per Digitization Centre convention.

Roman numerals in the filename that correspond to the object identifier (e.g. in "1890_10_189_263i_cxxv_122.tif")
will be left alone so long as the folder is named correctly (e.g. is named "1890_10_189_263i_cxxv")

The script will find any roman numeral that appears in a filename... 
(a) after the digital identifier (which, again, is assumed to be the folder name)
(a) bounded by an underscore on the left, and whitespace or an underscore on the right (e.g. "cool_rbsc_object_xix" or "cool_rbsc_object_xvii_001")

'''

def find_roman_numerals(text):
	'''returns a list of all roman numerals in the given text'''
	pattern = re.compile("(?<=_)[iIvVxXlLcCdDmM]+(?=_*)")
	match = re.findall(pattern, text)
	return match

def roman_to_int(roman):
	'''returns the integer value of the roman numeral provided'''
	roman_map = {'I':1, 'V':5, 'X':10, 'L':50, 'C':100, 'D':500, 'M':1000}
	try:
		roman = roman.upper()
		for char in roman:
			values = []
			for char in roman:
				value = roman_map[char]
				values.append(value)
			# calculate integer
			i = 0
			total = 0
			while ( i < len(values)):
				if (i+1 < len(values)):
					if (values[i] < values[i+1]):
						val = values[i+1] - values[i]
						total = total + val
						i = i + 1
					else:
						val = values[i]
						total = total + values[i]
				else:
					val = values[i]
					total = total + values[i]
				i = i + 1
			# return value zero-filled to 3 digits
			return "{:03}".format(total)
	except KeyError:
		print(roman + " contains an invalid roman numeral character")

def is_thumbs_or_ds(file):
	if file.endswith('.DS_Store') or file.endswith('.db'):
		return True
	else:
		return False

def get_new_filename(file, object_identifier):
	# isolate text after object identifier
	filename = os.path.basename(file)
	extension = file.split('.')[-1]
	numeral_range = filename.split(object_identifier)[-1]
	
	# find roman numeral to be translated
	if numeral_range is not None:
		match = find_roman_numerals(numeral_range)
		if len(match) == 1:
			numeral = match[0]
			integer = str(roman_to_int(numeral))
			# note: can't just find/replace the numeral for filename. will cause error if roman numeral is also valid character in object id (e.g. 1891_03_113_cxxxii_c)
			new_filename = object_identifier + '_RN-' + integer + '.' + extension
			return new_filename
		elif len(match) > 1:
			# this shouldn't happen
			print "multiple roman numerals present, oh no!"
			return None
		elif len(match) == 0:
			print "[No roman numeral found]\n"
			return None
	else:
		return None

def main(source_folder):
	object_identifier = source_folder.split('/')[-1]
	source_folder = os.path.abspath(source_folder)
	target_folder = source_folder + "_renamed"
	num_files = 0
	num_renamed = 0
	num_unchanged = 0
	try:
		os.makedirs(target_folder)
		print("make", target_folder)
	except OSError:
		pass
	for file in os.listdir(source_folder):
		src_filepath = os.path.join(source_folder, file)
		if not is_thumbs_or_ds(file):
			num_files += 1
			print("Original: " + src_filepath)
			new_filename = get_new_filename(src_filepath, object_identifier)
			new_filepath = ''
			if new_filename is not None:
				new_filepath = os.path.join(target_folder, new_filename)
				num_renamed +=1
				print("New:     " + new_filepath + '\n')
				if os.path.exists(new_filepath):
					print("File already exists. Check original roman numerals for errors.")
					raise FileExistsError
				else:
					shutil.copy(src_filepath, new_filepath)
			else:
				new_filepath = os.path.join(target_folder, file)
				num_unchanged +=1
				shutil.copy(src_filepath, new_filepath)
	print("Total files in original folder (excludes DS.store, thumbs.db): " + str(num_files))
	print("Total files renamed: " + str(num_renamed))
	print("Total unchanged: " + str(num_unchanged))


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='')
	parser.add_argument('source_folder')
	args = parser.parse_args()
	sys.exit(main(args.source_folder))