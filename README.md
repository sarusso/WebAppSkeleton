# Web App Skeleton

A Web App Skeleton project based on Django.

## Quickstart

Requirements:
    
    Bash, Git and Docker.

Build

    $ webappskeleton/build

Run

	$ webappskeleton/run

List running services

    # webappskeleton/ps

Populate demo data

    $ webappskeleton/populate
    # You can now point your browser to http://localhost:8080 or https://localhost
    # Log in using "testuser@web.app""and password "testpass"

Clean

	# webappskeleton/clean


## Configuration

### Webapp

These are the webapp service configuration parameters and their defaults:

      - DJANGO_DB_ENGINE="django.db.backends.postgresql_psycopg2"
      - DJANGO_DB_NAME="webapp"
      - DJANGO_DB_USER="webapp_master"
      - DJANGO_DB_PASSWORD="949fa84a"
      - DJANGO_DB_HOST="postgres"
      - DJANGO_DB_PORT=5432
      - DJANGO_DEV_SERVER=true
      - DJANGO_DEBUG=true
      - DJANGO_LOG_LEVEL=ERROR
      - WEBAPPLOG_LEVEL=ERROR
      - DJANGO_EMAIL_SERVICE=Sendgrid
      - DJANGO_EMAIL_APIKEY=""
      - DJANGO_EMAIL_FROM="Web App <notifications@web.app>"


### Proxy

These is the proxy service configuration parameter and its default:

      - PUBLIC_HOST=localhost

Certificates can be automatically handled with Letsencrypt. By default, a snakeoil certificate is used. To set up Letsencrypt, you need to run the following commands inside the proxy service (once in its lifetime).

    $ webappskeleton/shell proxy

First of all remove the default snakeoil certificates:

	$ sudo rm -rf /etc/letsencrypt/live/YOUR_PUBLIC_HOST
Then:

    $ nano /etc/apache2/sites-available/proxy-global.conf
    
...and change the certificates for the domain that you want to enable with Letsencrypt to use the snakeoils located in `/root/certificates/` as per the first lines of the `proxy-global.conf` file (otherwise next command will fail).

Now restart apache to pick up the new snakeoils:

	$  sudo apache2ctl -k graceful

Lastly, tell certbot to generate and validate certificates for the domain:

    $ sudo certbot certonly --apache --register-unsafely-without-email --agree-tos -d YOUR_PUBLIC_HOST
    
This will initialize the certificates in /etc/letsencypt, which are stored on the host in `./data/proxy/letsencrypt`

Finally, re-run the proxy service to drop the temporary changes and pick up the new, real certificates:

    $ webappskeleton/rerun proxy


## Development

### Live code changes

Django development server is running on port 8080 of the "webapp" service.

To enable live code changes, add or comment out the following in docker-compose.yaml under the "volumes" section of the "webapp" service:

    - ./services/webapp/code:/code
    
This will mount the code from services/webapp/code as a volume inside the webapp container itself allowing to make immediately effective codebase edits.

Note that when you edit the Django ORM model, you need to make migrations and apply them to migrate the database:

    $ webappskeleton/makemigrations
    $ webappskeleton/migrate


### Testing

Run Django unit tests:
    
    $ webappskeleton/test


### Logs


Check out logs for Docker containers (including entrypoints):


    $ webappskeleton/logs web

    $ webappskeleton/logs proxy


Check out logs for supervisord services:

        
    $ webappskeleton/logs web startup
    
    $ webappskeleton/logs web server

    $ webappskeleton/logs proxy apache
    
    $ webappskeleton/logs proxy certbot

    
## Known issues

### Building errors

It is common for the build process to fail with a "404 not found" error on an apt-get instructions, as apt repositories often change their IP addresses. In such case, try:

    $ CACHE=false webappskeleton/build nocache

## License

This work is licensed under the Apache License 2.0, unless otherwise specified.


