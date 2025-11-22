# Build the Nginx server
FROM nginx:1.29.3-alpine

# Copy the custom Nginx configuration file
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Clear default Nginx logs
RUN rm -f /var/log/nginx/* 

# Expose port 80
EXPOSE 80

# Start Nginx when the container launches
CMD ["nginx", "-g", "daemon off;"]
