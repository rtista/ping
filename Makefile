docker-build:
	@docker build -t ping docker/
	@docker create --name ping \
					-v $(shell pwd)/:/opt/ping/:Z \
					-p 8080:80 \
					ping
	@docker create --name pingdb \
					-e MYSQL_ROOT_PASSWORD=password \
					-p 3306:3306 \
					mariadb:10.3

docker-start:
	@echo "-- Starting Container --"
	@docker start ping
	@docker start pingdb
	@docker exec -it pingdb mysql -h 127.0.0.1 -P 3306 -u root -ppassword -e"GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'password' WITH GRANT OPTION; FLUSH PRIVILEGES;"

docker-enter:
	@echo "-- Entering Container --"
	@docker exec -it $(name) /bin/bash

docker-stop:
	@echo "-- Stopping Container --"
	@docker stop ping
	@docker stop pingdb

docker-clean:
	@echo "-- Docker Clean --"
	@docker rm -f ping pingdb
	@docker image rm -f ping mariadb:10.3
