# Use the official nginx image from the Docker Hub
FROM nginx:alpine

# Copy the nginx configuration file
COPY nginx.conf /etc/nginx/nginx.conf

# Copy the static files into the container
COPY . /usr/share/nginx/html

# Expose the port nginx runs on
EXPOSE 80
