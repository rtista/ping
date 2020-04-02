FROM centos:8

# Install system requirements
RUN dnf install -y epel-release
RUN dnf install -y \
    htop vim net-tools nginx \
    gcc libev-devel python36-devel

# Configure Nginx
RUN rm -f /etc/nginx/conf.d/* /etc/nginx/nginx.conf
COPY assets/nginx.conf /etc/nginx/
COPY assets/vhosts/*.conf /etc/nginx/conf.d/

# Expose Nginx
EXPOSE 80

# Start Nginx and sleep infinity to keep container running
CMD pip3 install -r /opt/ping/src/api/requirements.txt ; /usr/sbin/nginx -c /etc/nginx/nginx.conf ; sleep infinity
