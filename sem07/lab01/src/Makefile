run: main.py
	python3 main.py

convert: ./gui/distributions.ui
	pyuic5 ./gui/distributions.ui -o mainwindow.py
	sed 's/from mplwidget import/from gui.mplwidget import/g' mainwindow.py > ./gui/mainwindow.py
	rm mainwindow.py
