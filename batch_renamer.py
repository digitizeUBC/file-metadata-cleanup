
import os, sys, argparse
from os.path import isfile, isdir, join
'''

Given a folder containing a series of subfolders, renames files as [containing_subfolder_name]_[number].

To use:
1. Create a new folder on your desktop (e.g. "objects_to_rename")
2. Copy the object directories from the server into that folder
3. Make sure that (a) object directories are properly named and (b) image files inside are listed in the correct order.
The directory structure should look something like:
	objects_to_rename
		object_001
			img_001.tif
			img_002.tif
		object_002
			cheese_001.tif
			cheese_002.tif

4. Open Terminal, and use the following command syntax:

		python batch_rename.py [target folder]

	For example:

		python batch_rename.py /Users/NotAlbertBertilsson/Desktop/objects_to_rename

	The result will look something like:

	objects_to_rename
		object_001
			object_001_001.tif
			object_001_002.tif
		object_002
			object_002_001.tif
			object_002_002.tif
		object_003

'''

def is_thumbs_or_ds(file):
	if file.endswith('Store') or file.endswith('.db'):
		return True
	else:
		return False

def main(source_folder):
	objects = [o for o in os.listdir(source_folder) if isdir(join(source_folder, o))]
	for o in objects:
		identifier = o
		object_dir = os.path.join(source_folder, o)
		print('\nProcessing object ' + identifier + ' in ' + object_dir)
		files = [f for f in os.listdir(object_dir) if isfile(join(object_dir, f))]
		file_count = 0
		files_renamed = 0
		for f in files:
			file_path = os.path.abspath(join(source_folder, o, f))
			file_extension = file_path.split('.')[-1]
			# ignore thumbs.db and ds_store
			if not is_thumbs_or_ds(f):
				new_filename = identifier + '_' + format(file_count+1, "03d") + '.' + file_extension
				file_count +=1
				# ignore file if name starts with identifier starts with filename already, indicating it's been renamed already
				if not f.startswith(identifier):
					new_path = os.path.abspath(join(source_folder, o, new_filename))
					files_renamed+=1
					try: 
						os.rename(file_path, new_path)
						print('--Renamed ' + file_path + ' to ' + new_path)
					except OSError:
						pass
				else:
					print('--Unchanged: ' + f)
		print('Files found: ' + str(file_count))
		print('Files renamed: ' + str(files_renamed))

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='')
	parser.add_argument('source_folder')
	args = parser.parse_args()
	sys.exit(main(args.source_folder))