#!/usr/bin/env python3
'''
Title: gdrive.py

Author: Tony Dhami

Purpose: Libary for common functions and imports used in assessment scripts.

Requirements:
	- Client secret file located in script folder as .gdrive_client_secret.json
		- https://developers.google.com/workspace/guides/create-credentials

	pip: google-api-python-client 
		 google-auth-httplib2 
		 google-auth-oauthlib

'''

import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = ['https://www.googleapis.com/auth/drive']
TOKEN = '.gdrive_token.json'
CLIENT_SECRET = '.gdrive_client_secret.json'

def get_folder_contents(service, folder_id):
    '''
    Takes folder_id and returns dictionary of folder contents using
    drive service object.

    Args:
    	service: Drive api service instance.
    	folder_id: ID of the folder to retrieve contents from.
    Return:
    	results: Dictionary of items returned from query using folder_id.
    '''
    results = service.files().list(
		pageSize=1000,
		q=f"'{folder_id}' in parents",
		fields="nextPageToken, files(id, name, mimeType)",
		includeItemsFromAllDrives=True,
		supportsAllDrives=True
	).execute()

    return results

def get_metadata(service, id):
	'''
	Returns metadata name, mimeType from file/folder id.

    Args:
    	service: Drive api service instance.
    	id: drive file/folder ID to return metadata for.
    Return:
    	Dictionary of name,mimeType returned from query.
    '''
	return service.files().get(fileId=id, fields='name,mimeType').execute()

def get_top_level_objects(service, source_folder_id, folders_only=False):
    '''
    Takes source_folder_id, drive service object and returns 
    top level data.

    Args:
    	service: Drive api service instance.
    	source_folder_id: ID of the folder to get top level data for.
    	folders_only: (Optional) Argument to count only folders, default is false.
    Return:
    	top_level_objects: Dictionary of top level folder data.
    '''
    
    #Get folder contents.
    results = get_folder_contents(service, source_folder_id)

	#initliaze dictionary for top level data.
    top_level_objects = {}

	#Loops through contents of folder.
    for index in results.get('files', []):
        if folders_only:
            if index['mimeType'] == 'application/vnd.google-apps.folder':
                top_level_objects[index['id']] = index
        else:
            top_level_objects[index['id']] = index
    
    return top_level_objects

def create_service():
	'''
	Builds and returns Drive service object using oauth flow.
	Prompts for authorization if needed.

    Return:
    	service: Drive service object.
    '''

	creds = None

	# Load existing credentials from TOKEN if file exists.
	if os.path.exists(TOKEN):
		creds = Credentials.from_authorized_user_file(TOKEN, SCOPES)
	
	if not creds or not creds.valid:		
		#Refresh credentials.
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		
		else:
			#User authenticates again
			flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET, SCOPES)
			creds = flow.run_local_server(port=0)
		
		# Save the credentials for the next run.
		with open(TOKEN, "w") as token:
			token.write(creds.to_json())

	#Build service object with credentials.
	service = build('drive', 'v3', credentials=creds)

	return service