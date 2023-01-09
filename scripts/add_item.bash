#!/bin/bash
set -euo pipefail
# Adds item to collection
# Usage: ./add_item.bash 85 'de groene $(date +"%V %d %B %Y")'
SCRIPTDIR=`dirname -- "$( readlink -f -- "$0"; )"`
COLLECTION_ID=$1
NAME="$2"
DATE=$(date +%F)
echo 'INSERT INTO "main"."item" ("collection_id", "name", "owned", "want", "read", "owned_date") VALUES ('$COLLECTION_ID', "'$NAME'", 1, 0, 0, "'$DATE'");' | sqlite3 $SCRIPTDIR/../web/app.sqlite

