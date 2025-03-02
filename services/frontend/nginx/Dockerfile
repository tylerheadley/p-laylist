# Use the official NGINX Alpine image
FROM nginx:alpine

# Copy the NGINX configuration file
COPY ./nginx.conf /etc/nginx/conf.d/default.conf

# Copy the static files from the frontend build
# COPY ../build /usr/share/nginx/html

# Expose port 80 for HTTP traffic
EXPOSE 80

# Start NGINX
CMD ["nginx", "-g", "daemon off;"]
# FROM nginx:1.25

# RUN rm /etc/nginx/conf.d/default.conf
# COPY nginx.conf /etc/nginx/conf.d

