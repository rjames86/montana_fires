PELICAN="${HOME}/.virtualenvs/montana_fires/bin/pelican"
GH_IMPORT="${HOME}/.virtualenvs/montana_fires/bin/ghp-import"

pushd "$HOME/Dropbox/blogs/montana_fires";
$PELICAN -d -s publishconf.py >/dev/null;
$GH_IMPORT -b 'gh-pages' '/tmp/montana_fires' -p > /dev/null 2>&1
popd;
