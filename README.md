# MosaicUtils

-----
tilesim.py

Generates the MeerKAT TAB PSF + tiling pattern based on observation parameters.

EXAMPLE: 
python tilesim.py --ants antenna.csv --freq 1.284e9 --source 01:34:31.97 +22:00:00.0 --datetime 2020.02.11 14:00:00.0000 --beamnum 780 --verbose --overlap 0.25 --subarray 000,001,002,004,005,006,007,008,009,010,012,013,014,015,016,017,018,019,020,021,022,024,025,026,027,028,029,030,031,034,035,036,038,039,040,041


-----
detections_plot.py

Creates a quick plot of beam positions with detections coloured in. 

1. Run tilesim with the obs parameters.

This will produce a file called tilingCoord which has the RAs and Decs of each TAB.
It will also print out width1 = the height of the TABs in arcseconds, and width2 = TAB width, as well as the TAB orientation.

2. Run detections_plot.py -f {coord file} --w {TAB width} --h {TAB height} --a {TAB angle} --d {beam#} {beam#} {beam#}...

EXAMPLE:
If tilesim.py gives width1=62 and width2=42, and there are detections of a source in beams 123,125, and 126, 
to plot those beam positions, run:

python detections_plot.py -f tilingCoord --w 42 --h 62 --a -18.5 --d 123 125 126


-----
Primary_plotter.py

Plots the size of the primary beam at various wavelengths (L-band), corrected from horizontal into celestial coordinates, 
over a given series of TAB tiling patterns (e.g. at different Decs or RAs or overlap levels).

For each tiling pattern you want to make:
1. Run tilesim.py with the desired parameters.
2. Fill out the config file to look like example.txt

Then, just run Primary_plotter.py

EXAMPLE:
python Primary_plotter.py -f example.txt


---
gen_regionfile.py

Creates a DS9 region file with ellipses with desired coordinates & sizes. Useful for overlaying on a PSF generated by tilesim.py
to check that suspected sidelobe detections match up with predicted sidelobe positions.
Just edit the ras, decs, widths, heights, and pas arrays with the parameters of the ellipeses you want, and run the script. Generates
a "regionfile.reg" that can be imported into DS9.


---
compile_coordinates.py

Used in a directory with pulse archives and a run_summary.json CA log file compiles beam coordinates + SN values in the right format
for use with SeeKAT.py


---
gen_tilesim_cmd.py

python gen_tilesim_cmd.py -f run_summary.json

generates the appropriate command for a tilesim simulation based on the parameters in the run_summary.json log file
