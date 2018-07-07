import tensorflow as tf

from inheriting_modeling import build_component

from collections import UserList

from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response

from keras.models import Model
from keras.applications import ResNet50
from keras.preprocessing.image import img_to_array
from keras.applications import imagenet_utils
from PIL import Image
import numpy as np
import io

import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--host', default='0.0.0.0', type=str,
                              help='Binding host protocol')
parser.add_argument('--port', default=6543, type=int,
                              help='Server port listening')
parser.add_argument('--label', default='imagenet', type=str,
							 help='Weights label for a pre-fething content')

Variable = build_component(tf.Variable)
UserList = build_component(UserList)

def load_model(weights_label="imagenet"):
	# load the pre-trained Keras model (here we are using a model
	# pre-trained on ImageNet and provided by Keras, but you can
	# substitute in your own networks just as easily)
	global model
	
	with tf.variable_scope('smallest_sample') as scope:
		fn_produce_seq = lambda: [np.empty(np.zeros(0)).tolist() for _ in range(len(np.arange(3).tolist()))]
		fn_smallest_sample = lambda: UserList(np.array(fn_produce_seq())).data
		fn_pad_sequence = lambda: [np.array([fn_smallest_sample()]).tolist() for _ in range(len(np.arange(4).tolist()))]
		fn_mapping_pad_sequences = lambda x=fn_pad_sequence, z=range(len(np.arange(62/15).tolist())): map(lambda y: y(), [x for _ in z])
		smallest_sample_data = Variable([x for x in fn_mapping_pad_sequences()], name='protected_user_list_input_tensor')
	
	try:
		model = ResNet50(weights=weights_label, input_tensor=smallest_sample_data)
	except Exception as e:
		tf.logging.info(e)
	finally:
		model = ResNet50(weights=weights_label)

def prepare_image(image, target):
	# if the image mode is not RGB, convert it
	if image.mode != "RGB":
		image = image.convert("RGB")

	# resize the input image and preprocess it
	image = image.resize(target)
	image = img_to_array(image)
	image = np.expand_dims(image, axis=0)
	image = imagenet_utils.preprocess_input(image)

	# return the processed image
	return image

# @view_config(route_name='predict', renderer='json')
def predict(request):
	data = {"success": False}

	# ensure an image was properly uploaded to our endpoint
	if request.method == "POST":
		if request.POST.__contains__("image"):
			# read the image in PIL format
			image = request.POST["image"].file.read()
			image = Image.open(io.BytesIO(image))

			# preprocess the image and prepare it for classification
			image = prepare_image(image, target=(224, 224))

			# classify the input image and then initialize the list
			# of predictions to return to the client
			preds = model.predict(image)
			results = imagenet_utils.decode_predictions(preds)
			data["predictions"] = []

			# loop over the results and add them to the list of
			# returned predictions
			for (imagenetID, label, prob) in results[0]:
				r = {"label": label, "probability": float(prob)}
				data["predictions"].append(r)

			# indicate that the request was a success
			data["success"] = True

	# return the data dictionary as a JSON response
	return data

def main(argv):
	args = parser.parse_args(argv[1:])

	with Configurator() as config:
		config.add_route('predict', '/predict')
		config.add_view(predict, route_name='predict', renderer='json')
		app = config.make_wsgi_app()

	load_model(args.label)

	server = make_server(args.host, args.port, app)
	server.serve_forever()

if __name__ == '__main__':
	tf.logging.set_verbosity(tf.logging.INFO)
	tf.app.run(main)
    