#!/bin/bash

while true;do 
	sufix=$(date +%Y%m%d%H)
	wget -O /tmp/WWLLN_${sufix}.kmz http://flash3.ess.washington.edu/lightning_src.kmz
	python parsea_kml.py /tmp/WWLLN_${sufix}.kmz
	sleep 600
done
