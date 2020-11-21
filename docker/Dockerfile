FROM centos:8

# Install system requirements
RUN dnf install -y net-tools nginx gcc libev-devel python38-devel

# Configure Nginx
RUN rm -f /etc/nginx/conf.d/* /etc/nginx/nginx.conf
COPY assets/nginx.conf /etc/nginx/
COPY assets/ping.conf /etc/nginx/conf.d/

# Expose Nginx
EXPOSE 80

# Start Nginx and sleep infinity to keep container running
CMD cd /opt/ping ; pip3 install -r requirements.txt ; python3 ping-cli.py start ; \
    cd /opt/ping/ui/ ; npm install ; ng serve --aot ; \
    /usr/sbin/nginx -c /etc/nginx/nginx.conf ; \
    sleep infinity
