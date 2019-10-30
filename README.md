# Download Landsat Images

## Installation
1. Install landsat-util: [https://pythonhosted.org/landsat-util/installation.html](https://pythonhosted.org/landsat-util/installation.html)

2. Clone this repo

3. Create a virtualenvironment

```
virtualenv env
source env/bin/activate
```

4. Install requirements

```
pip install -r requirements.txt
```

## Usage
* Update satellite image params in data.json (search dates, which sat and locations)
* Either define location with sat name and path or lat long. For satellite names and paths see: [https://landsat.usgs.gov/landsat_acq#convertPathRow](https://landsat.usgs.gov/landsat_acq#convertPathRow)
* Note the operation dates of each satellite: 
	* landsat 5 Launch date: 1 March 1984, Deactivated: 5 June 2013
	* landsat 7: Launch date: April 15, 1999
	* landsat 8: Launch date: February 11, 2013
* Cloudy tiles are discarded.
* Script downloads all bands of sat data. Bands are combined in combine_tile function in the order defined in stack.sh file. Note that landsat 5,7 and 8 all have different band orders. Adjust stack.sh if you want to combine different bands. RGB for Landsat 8 are bands 4, 3, and 2 which will produce a true color image.
* Script also does a crude color correction in the function color_correct(). This could be improved! 

For more on Landsat 8 bands, see these guides by the ever brilliant Charlie Lloyd:
* [Putting Landsat 8’s Bands to Work](https://blog.mapbox.com/putting-landsat-8s-bands-to-work-631c4029e9d1)
* [https://blog.mapbox.com/processing-landsat-8-using-open-source-tools-d1c40d442263](https://blog.mapbox.com/processing-landsat-8-using-open-source-tools-d1c40d442263)