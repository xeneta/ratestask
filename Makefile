
NAME = rate
VERSION = 0.0.1

.PHONY: all stop build run

all: stop build run

build:
	docker-compose build

run:
	docker-compose up

watch:
	fswatch . | (while read; do make all; done)

stop:
	docker-compose stop
