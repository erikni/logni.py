#!/bin/sh

sudo apt-get install cdbs debhelper python3-setuptools -y

cp debian/rules debian/python-logni.rules
cp debian/install debian/python-logni.install

fakeroot dpkg-buildpackage -us -uc -ui -i -b
