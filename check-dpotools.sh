#!/usr/bin/env bash
# dbf, Dec 29 2022
#
# Quick and dirty pre-push check for dpotools project.
# Will not touch any files, but print warnings about things
# that can be easily forgotten:
# - SQLite dev database present
# - coverage remainders present
# - migrations dirs present
# - GNU PO files with long lines present (django-rosetta does this)
# - GNU MO binary files present
# - black check
# - flake8 check
# - check for open files
# Must be called from main dpotools project dir.
# Unix old school: No output = hunky-dory.
#set -x

### constants
export PATH=/usr/local/bin:/usr/bin:/bin:/sbin:/usr/sbin
export LC_ALL=C
PY_FILES="
./contact/urls.py
./contact/views.py
./contact/tests/test_views.py
./contact/tests/test_forms.py
./contact/apps.py
./contact/forms.py
./breach/urls.py
./breach/views.py
./breach/admin.py
./breach/tests/test_models.py
./breach/tests/test_functional.py
./breach/tests/test_views.py
./breach/tests/test_forms.py
./breach/apps.py
./breach/models.py
./breach/templatetags/breach_get_choice_text.py
./breach/forms.py
./landing/urls.py
./landing/views.py
./landing/tests/test_views.py
./landing/apps.py
./rpa/urls.py
./rpa/views.py
./rpa/admin.py
./rpa/tests/test_models.py
./rpa/tests/test_functional.py
./rpa/tests/test_views.py
./rpa/tests/test_forms.py
./rpa/apps.py
./rpa/models.py
./rpa/templatetags/rpa_get_choice_text.py
./rpa/forms.py
./dpotools/urls.py
"

### functions
warn() {
  echo "WARNING (will continue): $*" >&2
}
err() {
  echo "ERROR       (will exit): $*" >&2
}
is_installed() {
  program="$1"
  pathname=$(command -v "${program}" 2>/dev/null)
  [[ -z "${pathname}" ]] &&
    {
      err "Cannot locate ${program} in path."
      exit 1
    }
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
# add venv bin to $PATH
export PATH=/usr/local/bin:/usr/bin:/bin:/sbin:/usr/sbin:${VIRTUAL_ENV}/bin
# required programs installed?
is_installed find
is_installed black
is_installed flake8
is_installed lsof
is_installed awk
# GNU grep required
is_installed grep

### main
# check for dev database
[[ -f db.sqlite3 ]] &&
  warn "SQLite dev database present"
# check for coverage remainders
output=$(find . -type d -name "htmlcov")
[[ -z "${output}" ]] ||
  warn "coverage HTML output directory present"
output=$(find . -type f -name "coverage.*")
[[ -z "${output}" ]] ||
  warn "one or more coverage.* report files present"
[[ -f ".coverage" ]] &&
  warn "coverage results file present (.coverage)"
# check for migrations dirs
output=$(find . -type d -name "migrations")
[[ -z "${output}" ]] ||
  warn "database migrations directories present"
# check for long lines in GNU gettext PO files
pofiles=$(find . -name "django.po")
if [[ -n "${pofiles}" ]]; then
  for file in ${pofiles}; do
    hit=$(awk 'length>90' "${file}")
    if [[ -n "${hit}" ]]; then
      warn "PO file ${file} has long lines"
    fi
  done
fi
# check for MO files
output=$(find . -name django.mo)
[[ -z "${output}" ]] ||
  warn "GNU gettext MO binary files present (django.mo)"
# check for Python source code syntax and formatting using black
for file in ${PY_FILES}; do
  if [[ -f "${file}" ]]; then
    black --quiet --check "${file}" 2>/dev/null ||
      warn "${file} has syntax errors or is not properly formatted"
  else
    warn "${file} does not exist or is not accessible"
  fi
done
# check for Python source code syntax and formatting using flake8
for file in ${PY_FILES}; do
  if [[ -f "${file}" ]]; then
    flake8 --isolated --extend-ignore E501 "${file}" >/dev/null 2>&1 ||
      warn "${file} is griped about by flake8"
  else
    warn "${file} does not exist or is not accessible"
  fi
done
# check for open files in or below $PWD (sloppy!)
rawoutput=$(lsof -w -F n +D "${PWD}")
output=$(echo "${rawoutput}" | grep '^n')
myname=$(basename "${0}")
if [[ -n "${output}" ]]; then
  for str in ${output}; do
    hit=$(echo "${str}" | grep -E -v "(""${PWD}""$|""${myname}""$)")
    if [[ -n "${hit}" ]]; then
      warn "There may be open files in or below ${PWD}"
      break
    fi
  done
fi
