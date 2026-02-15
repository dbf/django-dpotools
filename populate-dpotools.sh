#!/usr/bin/env bash
# dbf, 19 Jul 2025
#
# Populate dpotools with example data
# Example users:
# erwin - is_superuser, is_staff
# hugo - is_staff
# kuno
# user name = user password (caveat!)

### functions
err() {
  echo "ERROR       (will exit): $*" >&2
}

### sanity checks and settings
# better not run this as root
[[ "${EUID}" -eq "0" ]] &&
  {
    err "This script is not supposed to be run with root privileges."
    exit 1
  }
# are we in main project dir?
[[ -f "./manage.py" && -d "./dpotools" ]] ||
  {
    err "This script must be run in the main dpotools project dir."
    exit 1
  }
# is a Python venv active (hopefully the project's venv)?
[[ -z "${VIRTUAL_ENV}" ]] &&
  {
    err "This script must be run with the project's Python venv being active."
    exit 1
  }

python manage.py makemigrations breach rpa
python manage.py migrate
python manage.py loaddata rpa/fixtures/models-users-groups-permissions.json 
python manage.py loaddata examples-breach/example_breachreport_en.json 
python manage.py loaddata examples-breach/example_breachreport_de.json 
python manage.py loaddata examples-rpa/example_rpa_de.json 
python manage.py loaddata examples-rpa/example_rpa_en.json 
django-admin compilemessages

exit 0

