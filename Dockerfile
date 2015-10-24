FROM ubuntu:14.04
MAINTAINER lagesonum

# Install pygments (for syntax highlighting) 
RUN apt-get -qq update \
    && DEBIAN_FRONTEND=noninteractive apt-get -qq install -y --no-install-recommends python3-pip gettext curl \
    && rm -rf /var/lib/apt/lists/*

RUN echo "Hello World"

# Create working directory
ADD ./ /tmp/lagesonum
WORKDIR /tmp/lagesonum

RUN pip3 install -r requirements_dev.txt
ENV SECRET_KEY='foo'

# Expose default django port
EXPOSE 8000

# Automatically build site
#ONBUILD ADD site/ /usr/share/blog
#ONBUILD RUN hugo -d /usr/share/nginx/html/

# By default, serve site
CMD ./start.sh


