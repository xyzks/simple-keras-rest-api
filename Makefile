build:
	docker build -t simple-keras-rest-api .

run:
	docker run -it --rm -p 6543:6543 --name image_classifier simple-keras-rest-api

deploy:
	now --docker --public

.PHONY: build run