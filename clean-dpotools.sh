#!/usr/bin/env bash
# dbf, 16 Jan 2025
#
# Clean up dpotools project dir:
# - Remove SQLite dev database
# - Remove coverage remainders
# - Remove migration dirs
# - Remove GNU MO files
# - Remove Python cache dirs
# Must be called from main dpotools project dir.
# Unix old school: No output = hunky-dory.

#set -x
shopt -s lastpipe

### constants
export PATH=/usr/local/bin:/usr/bin:/bin:/sbin:/usr/sbin
export LC_ALL=C

### functions
err() {
  echo "[$(date +'%Y-%m-%dT%H:%M:%S%z')] $(basename "$0"): $*" >&2
}
info() {
  echo -n "INFO (will/would delete): $* " >&2
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
print_usage() {
echo "$(basename "$0"): clean up project dir from temporary files."
echo "usage: $(basename "$0") [-w] [-h]"
echo "no options:   dry run (show what would have been deleted)"
echo "-h (help):    show this help text"
echo "-w (wet run): really delete stuff (including SQLite db)"
}

GODEL=0
while getopts ':wh' OPTION
do
  case $OPTION in
    w) GODEL=1
       ;;
    h) print_usage
       exit 0
       ;;
    ?) echo "$(basename "$0"): clean project dir - use \"-h\" for help"
       exit 1
       ;;
  esac
done
shift "$((OPTIND-1))"

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
# required programs installed?
is_installed find

### main
DIDSOMETHING=0
DELCMD="echo"
if [ $GODEL -eq 1 ]; then
  DELCMD="rm -rfv"
fi

# check for dev database
[[ -f db.sqlite3 ]] && {
  info "SQLite dev database"
  eval "$DELCMD db.sqlite3"
  DIDSOMETHING=1
  }
# check for coverage remainders
find . \( -type d -name "htmlcov" \
  -o -type f -name ".coverage" \
  -o -type f -name "coverage.*" \) | while IFS= read -r fod
  do
    info "coverage remainder"
    eval "$DELCMD ${fod@Q}"
    DIDSOMETHING=1
  done
# check for migrations dirs
find . -type d -name "migrations" | while read -r fod
  do
    info "db migration dir"
    eval "$DELCMD $fod"
    DIDSOMETHING=1
  done
# check for MO files
find . -type f -name "django.mo" | while read -r fod
  do
    info "gettext MO file"
    eval "$DELCMD $fod"
    DIDSOMETHING=1
  done
# check for Python cache dirs
find . -type d -name "__pycache__" | while read -r fod
  do
    info "python cache dir"
    eval "$DELCMD $fod"
    DIDSOMETHING=1
  done
# flight evaluation report
if [ $GODEL -eq 1 ] && [ $DIDSOMETHING -eq 1 ]; then
  echo "*** WET RUN - files and dirs deleted"
elif [ $GODEL -eq 0 ] && [ $DIDSOMETHING -eq 1 ]; then
  echo "DRY RUN - files and dirs NOT deleted"
fi

exit 0

