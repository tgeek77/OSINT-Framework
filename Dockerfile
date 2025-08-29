#####################################################################
#                            Build Stage                            #
#####################################################################
FROM docker.io/nginx

# Set the working directory
WORKDIR /usr/share/nginx/

# Copy the current directory contents into the container
COPY . /usr/share/nginx/

