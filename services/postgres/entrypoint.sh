#!/bin/bash

# Exit on any "error". More sophisticated approaches could be implemented in future.
# See also: https://stackoverflow.com/questions/4381618/exit-a-script-on-error
set -e

echo ""
echo "[INFO] Executing entrypoint..."


#------------------------------
# Setup Postgres
#------------------------------
echo "[INFO] Setting up Postgres..."

if [ ! -d "/data/postgres/14" ]; then
    echo "Data dir does not exist"
    # Setup /data/postgres
    mkdir -p /data/postgres
    chown postgres:postgres  /data/postgres
    chmod 700 /data/postgres

    # Setup /data/postgres/14
    mkdir -p /data/postgres/14
    chown postgres:postgres /data/postgres/14
    chmod 700 /data/postgres/14

    # Copy files
    mv /var/lib/postgresql/14/main /data/postgres/14/

    # Create link
    ln -s /data/postgres/14/main /var/lib/postgresql/14/main

    # Move conf
    #mv /etc/postgresql/14/main/pg_hba.conf /data/postgres
    #ln -s /data/postgres/pg_hba.conf /etc/postgresql/14/main/pg_hba.conf
    #chown postgres:postgres /data/postgres/pg_hba.conf

    # Move conf
    #mv /etc/postgresql/14/main/postgresql.conf /data/postgres
    #ln -s /data/postgres/postgresql.conf /etc/postgresql/14/main/postgresql.conf
    #chown postgres:postgres /data/postgres/postgresql.conf

else
    echo "Data dir does exist"
    mv /var/lib/postgresql/14/main /var/lib/postgresql/14/main_or
    ln -s /data/postgres/14/main /var/lib/postgresql/14/main

    #mv /etc/postgresql/14/main/pg_hba.conf /etc/postgresql/14/main/pg_hba.conf_or
    #ln -s /data/postgres/pg_hba.conf /etc/postgresql/14/main/pg_hba.conf
    #chown postgres:postgres /data/postgres/pg_hba.conf

    #mv /etc/postgresql/14/main/postgresql.conf /etc/postgresql/14/main/postgresql.conf_or
    #ln -s /data/postgres/postgresql.conf /etc/postgresql/14/main/postgresql.conf
    #chown postgres:postgres /data/postgres/postgresql.conf

fi


# Check correct permissions. Incorrect permissions might occur when changing base images,
# as the user "postgres" might get mapped to a differend uid / guid.
PERMISSIONS=$(ls -alh /data/postgres | grep main | awk '{print $3 ":" $4}')
if [[ "x$PERMISSIONS" == "xpostgres:postgres" ]] ; then
    # Everything ok
    :
else
    # Fix permissions
    chown -R postgres:postgres /data/postgres/
    #chown -R postgres:postgres /data/postgres/14 
    #chown -R postgres:postgres /data/postgres/pg_hba.conf  
    #chown -R postgres:postgres /data/postgres/postgresql.conf
    chown -R postgres:postgres /var/run/postgresql
fi


# Configure Postgres (create user etc.)
if [ ! -f /data/postgres/configured_flag ]; then
    echo 'Initializing as /data/postgres/configured_flag is not found...'   
    echo "Running postgres server in standalone mode for configuring users..."
    # Run Postgres. Use > /dev/null or a file, otherwise Reyns prestarup scripts end detection will fail
    /etc/supervisor/conf.d/run_postgres.sh &> /dev/null &

    # Save PID
    PID=$!

    echo "PID=$PID"

    # Wait for postgres to become ready (should be improved)
    sleep 10

    echo 'Creating user/db...'
    # Execute sql commands for webapp user/db
    su postgres -c "psql -f /create_webapp_DB_and_user.sql"

    # Set configured flag
    touch /data/postgres/configured_flag

    echo "Stopping Postgres"

    # Stop Postgres
    kill $PID

    echo "Ok, configured"
else
    echo ' Not configuring as /data/postgres/configured_flag is found.'
fi


#------------------------------
#   Save environment to file
#------------------------------
echo "[INFO] Dumping env..."

env | \
while read env_var; do
  if [[ $env_var == HOME\=* ]]; then
      : # Skip HOME var
  elif [[ $env_var == PWD\=* ]]; then
      : # Skip PWD var
  else
      echo "export $env_var" >> /env.sh
  fi
done


#------------------------------
#  Execute entrypoint command
#------------------------------
if [[ "x$@" == "x" ]] ; then
    ENTRYPOINT_COMMAND="supervisord"
else
    ENTRYPOINT_COMMAND=$@
fi

echo -n "[INFO] Executing entrypoint command: "
echo $ENTRYPOINT_COMMAND
exec "$ENTRYPOINT_COMMAND"
