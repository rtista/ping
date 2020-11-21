docker-build:
	@docker build -t ping docker/
	@docker create --name ping \
					-v $(shell pwd)/:/opt/ping/:Z \
					-p 8080:80 \
					ping

docker-start:
	@echo "-- Starting Container --"
	@docker start ping

docker-enter:
	@echo "-- Entering Container --"
	@docker exec -it ping /bin/bash

docker-stop:
	@echo "-- Stopping Container --"
	@docker stop ping

docker-clean:
	@echo "-- Docker Clean --"
	@docker rm -f ping
	@docker image rm -f ping
