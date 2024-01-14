#!/usr/bin/env bash
# This script prepares my web servers for static deployment

# Install Nginx if not already installed
apt-get update
apt-get install -y nginx

# Create necessary folders
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

# Create a fake HTML file
echo "<html>
  <head>
  </head>
  <body>
      Holberton School
   </body>
</html>" | tee /data/web_static/releases/test/index.html > /dev/null

# Create symbolic link
ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership to the ubuntu user and group
chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
printf %s "server {
	listen 80 default_server;
	listen [::]:80 default_server;
	add_header X-Served-By $HOSTNAME;
	root   /var/www/html;
	index  index.html index.htm;

	location /hbnb_static {
		alias /data/web_static/current;
		index index.html index.htm;
	}

	location /redirect_me {
		return 301 https://www.youtube.com/;
	}

	error_page 404 /404.html;
	location /404 {
		root /var/www/html;
		internal;
	}
}" > /etc/nginx/sites-available/default

# Restart Nginx
service nginx restart

# Exit successfully
exit 0
