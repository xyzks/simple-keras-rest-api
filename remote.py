import os

if 'URL' in os.environ:
	DEFAULT_URL = os.environ['URL']
elif not 'URL' in os.environ:
	DEFAULT_URL='http://localhost:6543/predict'
