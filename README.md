# PingDB

Ping.

## Docker Setup

1. Build the dockers:

```bash
make docker-build
```

2. Start the dockers:

```bash
make docker-start
```

3. Grant privilege to root from anywhere:

```bash
# Enter the container
make docker-enter name=pingdb

# Grant privilege to all
mysql -h 127.0.0.1 -P 3306 -u root -ppassword -e"GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'password' WITH GRANT OPTION; FLUSH PRIVILEGES;"

# Create ping database
mysql -h 127.0.0.1 -P 3306 -u root -ppassword mysql -e"CREATE DATABASE ping"
```
