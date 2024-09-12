#!/usr/bin/env python3
'''
Title: assessment1.py

Author: Tony Dhami

Purpose: Script to generate a report that shows the number of files and
         folders in total at the root of the source folder.
'''

import gdrive

def main():
    #Update variable to use another folder.
    source_folder_id = 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
	
    service = gdrive.create_service()

    print_folder_stats(service,source_folder_id)

def print_folder_stats(service, source_folder_id):
    '''
    Takes folder id, drive service object and counts 
    number of files/folders and outputs results.

    Args:
    	service: Drive api service instance.
    	folder_id: ID of the folder to retrieve stats for.
    '''

    file_count = 0
    folder_count = 0

    results = gdrive.get_folder_contents(service, source_folder_id)

    #Loops through contents of folder
    for index in results.get('files', []):

        #If folder increment counter and output name.
        if index['mimeType'] == 'application/vnd.google-apps.folder':
            print("Folder: %s" % index['name'])
            folder_count+=1

        #If not a folder increment counter and output name
        else:
            print("File: %s" % index['name'])
            file_count+=1

    print("\nTotal Folders: %s" % folder_count)
    print("Total Files: %s" % file_count)

if __name__ == '__main__':
	main()
