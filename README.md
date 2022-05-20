# Insert an image into Google Slides from your Google Photos
This example quickly show how to insert an image into your slides from Google photos images. 

When inserting an image into the slide, you need a publicly accessible URL of the image for the Slides API. 
It's not easy to get the public access url from the images located in Google Drive (the shared link is not public, and not direct link to the image)
Using images on Google Cloud Storage (GCS), you also need a singed url for the images. 
That's why I choose google photos as the image source. 
This example is based on the quickstart from google sldes and photos official documents. 



## Enable related APIs
Please go to GCP console, and enable the following APIs
- Google Slides API
- GOogle Photos API


## OAuth2.0 Parameters
You need to set up the oauth2 credentials from GCP console first. 
Then, put your client_id and client_secret into a file named "client_secrets.json"

```
{
  "installed": {
    "client_id": "837647042410-75ifg...usercontent.com",
    "client_secret":"asdlkfjaskd",
    "redirect_uris": ["http://localhost", "urn:ietf:wg:oauth:2.0:oob"],
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://accounts.google.com/o/oauth2/token"
  }
}
```

