.PHONY : report title clear main open

report : main open

TOR : ./doc/TOR.docx
	-mkdir pdf
	unoconv -o ./pdf/TOR.pdf ./doc/TOR.docx
	okular pdf/TOR.pdf

title : ./doc/report.docx
	-mkdir pdf
	unoconv -o ./pdf/title.pdf ./doc/report.docx

main : ./tex/MakefileTex
	cd ./tex && make -f MakefileTex
#	pdfunite pdf/title.pdf pdf/report.pdf pdf/fullReport.pdf

open :
	xdg-open pdf/report.pdf

clear :
	rm -rf ./pdf/report.pdf ./out/
	cd ./tex && make -f MakefileTex clear
