FROM ubuntu:22.04
MAINTAINER Stefano Alberto Russo <stefano.russo@gmail.com>

# Set non-interactive
ENV DEBIAN_FRONTEND noninteractive

# Update
RUN apt-get update

# Install utilities
RUN apt-get install -y nano telnet wget supervisor net-tools iproute2 iputils-ping sudo curl 

# Create bash_profile for loading correct env (/env.sh created by entrypoint.sh)
RUN echo "source /env.sh" > /root/.bash_profile

# Supervisord global conf
COPY supervisord.conf /etc/supervisor/

# Download get-pip script
RUN curl -O https://bootstrap.pypa.io/pip/3.6/get-pip.py

# Install Python3 and Pip3 (python3-distutils required for pip3)
RUN apt-get install python3 python3-distutils -y 

# Install Python3 and Pip3 (python3-distutils required for pip3)
RUN apt-get install python3 python3-distutils -y 
RUN python3 get-pip.py 'pip==21.0.1'

# Python 3 dev (for pycrypto), postgres driver required for psycopg2 and build-essential for uWSGI
RUN apt-get install -y python3-dev libpq-dev build-essential

# Add webapp group, with GID 65527 to try avoiding conflicts.
RUN groupadd -g 65527 webapp

# Add webapp user, with UID 65527 to try avoiding conflicts.
RUN useradd webapp -d /webapp -u 65527 -g 65527 -m -s /bin/bash

# Install Python requirements
COPY requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt

# Patch Django 2.2 non-ascii chars in /usr/local/lib/python3.10/dist-packages/django/views/templates/technical_500.html
RUN sed -i 's/[\x80-\xFF]/./g' /usr/local/lib/python3.10/dist-packages/django/views/templates/technical_500.html

# Prepare code dir, copy code & fix permissions
RUN mkdir /code
COPY code /code
RUN chown -R webapp:webapp /code

# Prepare for logs
RUN mkdir /var/log/webapp/ && chown webapp:webapp /var/log/webapp/

# Set proper permissions to the log dir
RUN chown webapp:webapp /var/log/webapp

# Supervisord scripts
COPY supervisord_webapp.conf /etc/supervisor/conf.d/
COPY run_webapp.sh /etc/supervisor/conf.d/
RUN chmod 755 /etc/supervisor/conf.d/run_webapp.sh

# Entrypoint
COPY entrypoint.sh /
RUN chmod 755 /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]