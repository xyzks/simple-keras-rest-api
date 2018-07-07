# USAGE
# python simple_request_server.py

# import the necessary packages
import os

import tensorflow as tf
import requests

from remote import fn_default_url

import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--rest_api_url', default=fn_default_url(os), type=str,
                              		  help='Address to predict')
parser.add_argument('--image_path', default='pelican.jpg', type=str,
									help='Predictible image')

def main(argv):
	args = parser.parse_args(argv[1:])
	# load the input image and construct the payload for the request
	image = open(args.image_path, "rb").read()
	payload = {"image": image}

	# submit the request
	r = requests.post(args.rest_api_url, files=payload).json()

	# ensure the request was sucessful
	if r["success"]:
		# loop over the predictions and display them
		for (i, result) in enumerate(r["predictions"]):
			print("{}. {}: {:.4f}".format(i + 1, result["label"],
				result["probability"]))

	# otherwise, the request failed
	else:
		print("Request failed: %s -X POST -F image=@dog %s" % ('curl', args.rest_api_url))

if __name__ == '__main__':
	tf.logging.set_verbosity(tf.logging.INFO)
	tf.app.run(main)