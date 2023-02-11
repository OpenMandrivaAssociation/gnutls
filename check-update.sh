#!/bin/sh
MAJOR=$(curl https://www.gnupg.org/ftp/gcrypt/gnutls/ 2>/dev/null |grep -E -- '>v[0-9\.]*<' |sed -E 's,(.*)>v([0-9\.]*)<.*,\2,' |sort -V |tail -n1)
curl https://www.gnupg.org/ftp/gcrypt/gnutls/v${MAJOR}/ 2>/dev/null |grep .tar.xz |sed -e 's,\.tar\.xz.*,,;s,.*gnutls-,,' |sort -V |tail -n1
