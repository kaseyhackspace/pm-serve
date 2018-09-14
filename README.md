# Project Structure:
## logger
Contains MVC Logic for running the PM-Serve Information System. Uses Django Framework
## mesh_master
Contains code for uploading to the mesh network master Arduino UNO node.
## mesh_station
Contains code for uploading to the mesh network station Arduino UNO node.
## gateway.py
Receives station data from the mesh network via the mesh master and uploads to the information system using exposed REST URI

## Setup
### Installation of Geospatial libs:
sudo apt-get install binutils libproj-dev gdal-bin

### Installation of PostgreSQL:
sudo apt-get install postgresql-9.5 postgresql-9.5-postgis postgresql-server-dev-9.5 python-psycopg2
pip install psycopg2-binary

### Configure PostgreSQL:
sudo -u postgres psql

postgres=# CREATE USER geodjango PASSWORD 'p@ssw0rd';
CREATE ROLE
postgres=# CREATE DATABASE geodjango OWNER geodjango;
CREATE DATABASE
postgres=# CREATE EXTENSION postgis;
CREATE EXTENSION
