#!/bin/bash
#https://landsat.usgs.gov/what-are-band-designations-landsat-satellites

if [ "$1" = "5" ];then
	rio stack --rgb $2{4,3,2}.TIF $3
fi
if [ "$1" = "7" ];then
	rio stack --rgb $2{3,2,1}.TIF $3
fi
if [ "$1" = "8" ];then
	rio stack --rgb $2{4,3,2}.TIF $3
fi
