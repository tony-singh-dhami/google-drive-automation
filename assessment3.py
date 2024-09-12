#!/usr/bin/env python3
'''
Title: assessment3.py

Author: Tony Dhami

Purpose: Script to copy the content (nested files/folders) of the source folder to the destination
		 folder.
'''
import gdrive

def main():
	#Update variable to use another source folder.
	source_file_id = 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'

    #Update variable to use another destination folder.
	destination_folder_id = 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'

	service = gdrive.create_service()

	top_level_objects = gdrive.get_top_level_objects(service, source_file_id)

	for key in top_level_objects:
		#Recursive copy.
		copy_recursive(service, key, destination_folder_id)

def create_folder(service, folder_name, parent_folder_id):
    '''
    Takes parent_folder_id, folder_name, drive service object
    and creates folder underneath parent_folder_id.

    Args:
    	service: Drive api service instance.
    	file_name: Name to be used for new folder
    	parent_folder_id: Parent folder ID to create new folder underneath.
    Return:
        new_folder: dictionary of newly created folder metadata
    '''
    metadata = {
        'name': folder_name,
        'parents': [parent_folder_id],
        'mimeType': 'application/vnd.google-apps.folder',
    }

    #Copy folder.
    new_folder = service.files().create(body=metadata, supportsAllDrives=True).execute()

    return new_folder

def copy_file(service, source_file_id, destination_folder_id):
    '''
    Takes source_file_id, destination_folder_id, drive service object
    and copies files.

    Args:
    	service: Drive api service instance.
    	source_file_id: ID of the drive file to copy
    	destination_folder_id: ID of the drive folder to copy to.
    '''

    #Get file name.
    source_file_metadata = gdrive.get_metadata(service, source_file_id)
    source_file_name = source_file_metadata.get('name', 'Unknown File')

    metadata = {
        'name': source_file_name,
        'parents': [destination_folder_id],
    }

    #Copy file.
    new_file = service.files().copy(fileId=source_file_id, body=metadata, supportsAllDrives=True).execute()
    
def copy_recursive(service, source_object_id, destination_folder_id):
    '''
    Takes source_folder_id, destination_folder_id, drive service object
    and copies files/folder recursively to recreate files/folders in new location.

    Args:
    	service: Drive api service instance.
    	source_object_id: ID of the drive object to copy
    	destination_folder_id: ID of the drive folder to copy to.
    '''
	
	#Get name.	
    source_object_metadata = gdrive.get_metadata(service, source_object_id)
    source_object_name = source_object_metadata['name']

    if source_object_metadata['mimeType'] == 'application/vnd.google-apps.folder':

        root_folder = create_folder(service, source_object_name, destination_folder_id)

		#Iterate over items in source folder
        results = gdrive.get_folder_contents(service, source_object_id)

        for index in results.get('files', []):
			
			#If drive object is folder, recursively call this function.
            if index['mimeType'] == 'application/vnd.google-apps.folder':
                copy_recursive(service, index['id'], root_folder['id'])
            else:
                copy_file(service, index['id'], root_folder['id'])

    #If not a folder, copy file.
    else:
        copy_file(service, source_object_id, destination_folder_id)

if __name__ == '__main__':
	main()