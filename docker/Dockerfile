FROM centos:8

# Install system requirements
RUN dnf install -y epel-release
RUN dnf install -y \
    htop vim net-tools nginx \
    gcc libev-devel python36-devel

# Configure Nginx
RUN rm -f /etc/nginx/conf.d/* /etc/nginx/nginx.conf
COPY assets/nginx.conf /etc/nginx/
COPY assets/api.conf /etc/nginx/conf.d/

#
# Install PIP Dependencies
# 
# COPY src/api/requirements.txt
# RUN pip3 install -r /root/requirements.txt

# Expose Nginx and MariaDB
EXPOSE 80

# Start Nginx and sleep infinity to keep container running
CMD mysql_install_db --user=root --datadir=/var/lib/mysql/ ; \
    /usr/bin/mysqld_safe --datadir='/var/lib/mysql/'; \
    /usr/sbin/nginx -c /etc/nginx/nginx.conf ; \
    sleep infinity
