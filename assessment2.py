#!/usr/bin/env python3
'''
Title: assessment2.py

Author: Tony Dhami

Purpose: Script to generate a report that shows the number of child objects (recursively)
		 for each top-level folder under the source folder id and a total of nested 
		 folders for the source folder.
'''

import gdrive

def main():
    #Update variable to use another folder.
    source_folder_id = 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'

    service = gdrive.create_service()

    top_level_folders = gdrive.get_top_level_objects(service, source_folder_id, folders_only=True)

    for folder in top_level_folders:
        print("Top Level Folder: %s" % top_level_folders[folder]['name'])

        count = count_child_objects(service,folder)

        print("\tTotal Child Objects: %s" % count)

        #Count folder objects for source folder.
	source_nested_folder_count = count_child_objects(service,source_folder_id,count=0,folders_only=True)

	source_folder_metadata = gdrive.get_metadata(service, source_folder_id)

	print("\nSource Folder: %s" % source_folder_metadata['name'])
	print("\tNested folders: %s" % source_nested_folder_count)


def count_child_objects(service, source_folder_id, count = 0, folders_only=False):
    '''
    Takes source_folder_id, drive service object and counts 
    number of child objects recursively.

    Args:
    	service: Drive api service instance.
    	source_folder_id: ID of the folder to count stats for.
    	count: (Optional) Argument to pass counter recursively
    	folders_only: (Optional) Argument to count only folders, default is false.
    Return:
    	count: int counter of number of child objects.
    '''

    results = gdrive.get_folder_contents(service, source_folder_id)

	#Loops through contents of folder
    for index in results.get('files', []):
		#Count folders recursively.
        if index['mimeType'] == 'application/vnd.google-apps.folder':
            count = count_child_objects(service,index['id'],count+1, folders_only)
        else:
            if not folders_only:
                count+=1

    return count

if __name__ == '__main__':
	main()
