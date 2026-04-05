#!/bin/sh
set -eu

PUBLIC_SOURCE=/opt/bootstrap/public
PUBLIC_TARGET=/var/www/html/public
STORAGE_SOURCE=/opt/bootstrap/storage
STORAGE_TARGET=/var/www/html/storage

mkdir -p "$PUBLIC_TARGET" "$STORAGE_TARGET"

sync_public() {
    if [ ! -d "$PUBLIC_SOURCE" ]; then
        return
    fi

    rsync -a --delete "$PUBLIC_SOURCE/" "$PUBLIC_TARGET/"
}

sync_storage() {
    if [ ! -d "$STORAGE_SOURCE" ]; then
        return
    fi

    rsync -a --ignore-existing "$STORAGE_SOURCE/" "$STORAGE_TARGET/"
}

sync_public
sync_storage

chown -R www-data:www-data "$PUBLIC_TARGET" "$STORAGE_TARGET" 2>/dev/null || true

exec "$@"
