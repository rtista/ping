FROM centos:8

# Install system requirements
RUN dnf install -y epel-release
RUN dnf install -y \
    wget htop vim net-tools \
    gcc libev-devel python36-devel \
    mariadb-server

#
# Install PIP Dependencies
# 
# COPY src/api/requirements.txt
# RUN pip3 install -r /root/requirements.txt

#
# Nginx Installation and Configuration
# 

# Install Nginx ALPN
RUN dnf install -y nginx
RUN rm -f /etc/nginx/conf.d/* /etc/nginx/nginx.conf
COPY assets/nginx.conf /etc/nginx/
COPY assets/api.conf /etc/nginx/conf.d/

EXPOSE 80

# Start Nginx and sleep infinity to keep container running
CMD /usr/sbin/nginx -c /etc/nginx/nginx.conf ; sleep infinity
