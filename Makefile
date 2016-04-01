changelog:
	@rm -f .deb-changelog
	@rm -f version.properties
	@head -1 debian/changelog | cut -d " " -f1 | tr -d '\n' > .deb-changelog
	@echo -n " (" >> .deb-changelog
	@head -1 debian/changelog  | cut -d"(" -f2 | cut -d")" -f1 | cut -d"." -f1,2 | tr -d '\n' >> .deb-changelog
	@head -1 debian/changelog  | cut -d"(" -f2 | cut -d")" -f1 | cut -d"." -f1,2 | tr -d '\n' >> version.properties
	@echo -n "." >> .deb-changelog
	@echo -n "." >> version.properties
	@V3=$$((`head -1 debian/changelog  | cut -d"(" -f2 | cut -d")" -f1 | cut -d"." -f3` + 1)); echo -n $${V3} >> .deb-changelog
	@V3=$$((`head -1 debian/changelog  | cut -d"(" -f2 | cut -d")" -f1 | cut -d"." -f3` + 1)); echo -n $${V3} >> version.properties
	@echo ") unstable; urgency=low" >> .deb-changelog
	@echo >> .deb-changelog
	@echo "  * " >> .deb-changelog
	@echo >> .deb-changelog
	@echo -n " -- $$(sed -n '/^Maintainer:/s/^.*: //p' debian/control)  " >> .deb-changelog
	@date -R >> .deb-changelog
	@echo >> .deb-changelog
	@cat debian/changelog >> .deb-changelog
	@echo >> .deb-changelog
	@editor .deb-changelog
	@mv .deb-changelog debian/changelog

/usr/bin/dpkg-buildpackage:
	@echo packages dpkg-dev and curl must be install (apt-get install dpkg-dev curl)
	@exit 1

deb: /usr/bin/dpkg-buildpackage changelog 
	@dpkg-buildpackage -uc -us
	@curl --verbose -T ../python-logni_`cat version.properties`_all.deb -uerikni:db17318ea051248fa023ac98e969639f135ddfe3 https://api.bintray.com/content/logni/deb/python-logni/`cat version.properties`/python-logni_`cat version.properties`;deb_distribution=squeeze,wheezy,jessie;deb_component=main;deb_architecture=i386,amd64

clean:
	@rm -rf debian/python2.4-logni debian/python2.5-logni debian/files
	@mv -v ../python-logni*.deb /tmp/

