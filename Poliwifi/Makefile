

all: uic language

uic:
	@echo "Generating ui..."
	@pyside-uic wizard.ui > src/poliwifi/interface.py
	@echo "Done."

language:
	@echo "Generating language files..."
	@lrelease poliwifi.pro
	@echo "Done.."

clean:
	@rm il8n/*.qm
	@rm src/poliwifi/interface.py

cleanpy: clean
	@rm src/poliwifi/*.pyc
	@rm *.pyc

install: uic language
	@echo "Creating Dirs..."
	@install -d  $(DESTDIR)/usr/share/poliwireless/il8n
	@install -d 	$(DESTDIR)/usr/share/poliwireless/poliwifi
	@install -d  $(DESTDIR)/usr/share/applications
	@install -d  $(DESTDIR)/usr/share/pixmaps
	@echo "Installing translations..."
	@install -m 644 il8n/*.qm $(DESTDIR)/usr/share/poliwireless/il8n
	@echo "Installing scripts..."
	@install -m 644 src/poliwifi/*.py $(DESTDIR)/usr/share/poliwireless/poliwifi
	@install -m 755 -D poliwireless.py $(DESTDIR)/usr/bin/poliwireless
	@install -m 755 quirks.py $(DESTDIR)/usr/share/poliwireless/
	@echo "Installing icon.."
	@install -m 644 poliwireless.desktop $(DESTDIR)/usr/share/applications
	@install -m 644 poliwireless.png $(DESTDIR)/usr/share/pixmaps
	@echo "Install done."
.PHONY : install uic
	
