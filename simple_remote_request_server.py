# USAGE
# python simple_request_server.py

# import the necessary packages
import os
import requests

# initialize the Keras REST API endpoint URL along with the input
# image path
URL = os.environ["URL"]
KERAS_REST_API_URL = "{0}/predict".format(URL)
IMAGE_PATH = "pelican.jpg"

# load the input image and construct the payload for the request
image = open(IMAGE_PATH, "rb").read()
payload = {"image": image}

# submit the request
r = requests.post(KERAS_REST_API_URL, files=payload).json()

# ensure the request was sucessful
if r["success"]:
	# loop over the predictions and display them
	for (i, result) in enumerate(r["predictions"]):
		print("{}. {}: {:.4f}".format(i + 1, result["label"],
			result["probability"]))

# otherwise, the request failed
else:
	print("Request failed")