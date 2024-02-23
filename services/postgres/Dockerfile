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

# Install Postgres
RUN apt-get install -y postgresql-14

# Copy conf
RUN mv /etc/postgresql/14/main/pg_hba.conf /etc/postgresql/14/main/pg_hba.conf.or
COPY pg_hba.conf /etc/postgresql/14/main/pg_hba.conf 
COPY postgresql.conf /etc/postgresql/14/main/postgresql.conf

# Chown conf
RUN chown -R postgres:postgres /etc/postgresql

# Create user/db script
COPY create_webapp_DB_and_user.sql /
RUN chown postgres:postgres /create_webapp_DB_and_user.sql

# Supervisord scripts
COPY run_postgres.sh /etc/supervisor/conf.d/
RUN chmod 755 /etc/supervisor/conf.d/run_postgres.sh
COPY supervisord_postgres.conf /etc/supervisor/conf.d/

# Entrypoint
COPY entrypoint.sh /
RUN chmod 755 /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
