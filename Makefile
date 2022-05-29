.POSIX:

PREFIX = ~/.local

all: install

tuxi:

install:
	mkdir -p ${DESTDIR}${PREFIX}/bin
	cp tuxi.py ${DESTDIR}${PREFIX}/bin/tuxi.py

uninstall:
	rm -f ${DESTDIR}${PREFIX}/bin/tuxi.py

.PHONY: all install uninstall
