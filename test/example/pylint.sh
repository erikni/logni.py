#!/bin/sh

sudo pip3 install -r requirements.txt

PYLINT_BIN="/usr/bin/pylint3"
if [ ! -f "$PYLINT_BIN" ]; then
	echo -n "sudo ln -s /usr/bin/pylint $PYLINT_BIN ... "
	sudo ln -s /usr/bin/pylint $PYLINT_BIN
	echo "done"
fi

pylint3 --version
pylint3 *.py logni/*.py test/example/*.py test/unit/*.py
