# Use the official Nginx image as a base
FROM nginx:alpine

# Copy custom configuration file for Nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Expose port 80 to the outside world
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
