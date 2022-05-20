from __future__ import print_function

import os.path
import json
import requests

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/presentations','https://www.googleapis.com/auth/photoslibrary.readonly']

# The ID of a sample presentation.
PRESENTATION_ID = '1tbij68JPklixRdAOFK70QUV0i2dAouYPqf5Tu9c-C3I'


def main():
    """Shows basic usage of the Slides API.
    Prints the number of slides and elments in a sample presentation.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secrets.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())


    try:

        #
        # Google Photo: Get image URL (No python library, so use REST)
        #

        credential = json.loads(creds.to_json())
        headers = {'Authorization': 'Bearer {}'.format(credential['token'])}
        ## EXAMPLE - Get the Album id
        # req_uri = 'https://photoslibrary.googleapis.com/v1/albums'
        # r = requests.get(req_uri, headers=headers)

        # Please refer to https://developers.google.com/photos/library/guides/list#listing-album-contents
        req_uri = 'https://photoslibrary.googleapis.com/v1/mediaItems:search'
        payload = {
            "pageSize": "100",
            "albumId": "ADHNBi3lhIl_B3_desmHQBQOmhHIYdMIWGs3OY2hrLdHK4JRIcnTNNdPavWkkRjzoY5A9DjJmDNF"
        }
       
        r = requests.post(req_uri, data=payload, headers=headers)
        photos = json.loads(r.text)
        # Only one picture in my test album, please change to a for loop 
        image_url = photos['mediaItems'][0]['baseUrl']
        

        #
        # Google Slides: Insert the image into the slide 
        #

        # page id, need to query it first if multiple pages
        page_id = 'g12d63d03bc3_0_0'

        slides_service = build('slides', 'v1', credentials=creds)
        # Create a new image, using the supplied object ID,
        # with content downloaded from IMAGE_URL.
        image_requests = []
        image_id = 'MyImage_01'
        emu4M = {
            'magnitude': 4000000,
            'unit': 'EMU'
        }
        image_requests.append({
            'createImage': {
                'objectId': image_id,
                'url': image_url,
                'elementProperties': {
                    'pageObjectId': page_id,
                    'size': {
                        'height': emu4M,
                        'width': emu4M
                    },
                    'transform': {
                        'scaleX': 1,
                        'scaleY': 1,
                        'translateX': 100000,
                        'translateY': 100000,
                        'unit': 'EMU'
                    }
                }
            }
        })

        # Execute the request.
        body = {
            'requests': image_requests
        }
        response = slides_service.presentations() \
            .batchUpdate(presentationId=PRESENTATION_ID, body=body).execute()
        create_image_response = response.get('replies')[0].get('createImage')
        print('Created image with ID: {0}'.format(
            create_image_response.get('objectId')))

    except HttpError as err:
        print(err)

    

if __name__ == '__main__':
    main()
