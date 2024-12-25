# Set your Cloudinary credentials
# ==============================
from dotenv import load_dotenv
load_dotenv()
# Import the Cloudinary libraries
# ==============================
import cloudinary
from cloudinary import CloudinaryImage
import cloudinary.uploader
import cloudinary.api

# Import to format the JSON responses
# ==============================
import json

# Set configuration parameter: return "https" URLs by setting secure=True  
# ==============================
config = cloudinary.config(secure=True)


def uploadImage(file, file_name):

  # Upload the image and get its URL
  # ==============================

  # Upload the image.
  # Set the asset's public ID and allow overwriting the asset with new versions
  cloudinary.uploader.upload(file, public_id=file_name, unique_filename = False, overwrite=True)

  # Build the URL for the image and save it in the variable 'srcURL'
  srcURL = CloudinaryImage(file_name).build_url()
  image_info=cloudinary.api.resource(file_name)
  print(json.dumps(image_info, indent=2))
  # Log the image URL to the console. 
  # Copy this URL in a browser tab to generate the image on the fly.
  return srcURL
  
def getAssetInfo(file_name):

  # Get and use details of the image
  # ==============================

  # Get image details and save it in the variable 'image_info'.
  image_info=cloudinary.api.resource(file_name)
  return image_info

 