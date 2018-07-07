
def fn_default_url(sub):
	if 'URL' in sub.environ:
		DEFAULT_URL = '%s/predict' % sub.environ['URL']
	if not 'URL' in sub.environ:
		DEFAULT_URL='http://localhost:6543/predict'
		os.environ['URL'] = DEFAULT_URL
	return DEFAULT_URL