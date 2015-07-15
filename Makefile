changelog:
	@rm -f .deb-changelog
	@head -1 debian/changelog | cut -d " " -f1 | tr -d '\n' > .deb-changelog
	@echo -n " (" >> .deb-changelog
	@head -1 debian/changelog  | cut -d"(" -f2 | cut -d")" -f1 | cut -d"." -f1,2 | tr -d '\n' >> .deb-changelog
	@echo -n "." >> .deb-changelog
	@V3=$$((`head -1 debian/changelog  | cut -d"(" -f2 | cut -d")" -f1 | cut -d"." -f3` + 1)); echo -n $${V3} >> .deb-changelog
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
	@echo chybi balik dpkg-dev (apt-get install dpkg-dev)
	@exit 1

deb: /usr/bin/dpkg-buildpackage changelog 
	@dpkg-buildpackage

clean:
	@rm -rf debian/python2.4-logni debian/python2.5-logni debian/files
	@mv -v ../python-logni*.deb /tmp/

