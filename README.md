# AFC_Summary
Python tool for summarizing data availability along with useful metadata for ARM field campaigns.  The script runs off a configuration file, like those shown in the conf directory to produce these Gantt style charts.  In addittion to data availability, the code will also display associated DOIs on the chart or in a separate table.  Listing associated DQRs in a table is also an option. Updated documentation coming soon!

## Usage
python afc_summary.py -c ./conf/conf.py

# DS Heatlh
This is a python wrapper function around Brian Ermolds nc_find_overlap program to gauge the health of ARM datastreams.  It is meant to run on the ADC systems with access to /data/archive.  The code will look for file splits and the use the results of the nc_find_overlaps to calculate a score for each datastream.  The more problems (file splits, overlapping times, reprocessing issues, etc...) the lower the score.  The user will need to set the site and the excluded directories.  Generally, one would want to avoid any instruments that produce a large number of files per day on a normal basis suchas scanning radars, scanning lidars, and cameras.  Also, it is beneficial to avoid any large files such as spectra.

## Usage
python ds_health.py
