#%% Import packages
import os, subprocess
import numpy as np
import re

regexp_numeric_pattern = r'[-+]? (?: (?: \d* \. \d+ ) | (?: \d+ \.? ) )(?: [Ee] [+-]? \d+ ) ?'
# This expression needs compiled by regexp
any_number = re.compile(regexp_numeric_pattern, re.VERBOSE)

#%% TO RUN THIS ON DOKIMI
#conda activate py27 #to run tilesim in anaconda installation of mosaic which is written in python 2
#python3 gen_regionfile.py # to run this script in python 3

#%% Set observation variables
workdir = '/raid/ecarli/SMC/mosaic_SMC_beamforming/1st_Pointing_0049-7312/'
ds9_dir = '/raid/ecarli/SMC/ds9_SMC_targets/Regions/First_Pointing_0049-7312/Tilings/'
observation_date = '2020.01.12' #YYYY.MM.DD
middle_of_obs_time = '09:30:00.00' #UTC
beam_total = 480
dishes = '000,001,002,003,004,006,007,008,009,011,012,013,014,015,016,017,018,019,020,021,022,023,024,026,027,029,030,031,032,033,034,035,036,037,038,039,040,041,042,043,044,045,046,047'

#%% Set sources

tiling_centres = ['00:47:07 -73:08:36','00:48:19.6 -73:19:40', '00:49:07.7 -73:14:45','00:51:06.7 -73:21:26']
source_names = ['TripleSNR','SNR0048-7319','SNR0049-7314', 'SNR0051-7321']
numbers_of_beams = [100,30,40,35]


print('There are '+str(beam_total-sum(numbers_of_beams))+' beams left to tile at boresight.')


for tiling_centre, source_name, number_of_beams in zip(tiling_centres, source_names, numbers_of_beams):
#%% Build TileSim command

    tilesim_command = 'python ~/PULSAR_SOFTWARE/mosaic/mosaic/tilesim.py --ants antenna.csv --freq 1.284e9 --source '+tiling_centre+'  --datetime '+observation_date+' '+middle_of_obs_time+' --beamnum '+str(number_of_beams)+'  --verbose --overlap 0.75 --resolution 1 --size 1000 --subarray '+dishes
    

#%% Run TileSim

    os.system('cd '+workdir)
    tilesim_run = subprocess.run(tilesim_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    
    tilesim_stdout_handle =  open(workdir+'Outputs/output_tiling_'+source_name, 'w')
    tilesim_stdout_handle.write(tilesim_run.stdout.decode('utf-8')+'\n')
    tilesim_stdout_handle.close()
    
    tilesim_stdout_handle =  open(workdir+'Outputs/output_tiling_'+source_name, 'r')
    for line in tilesim_stdout_handle:
        result_width1 = re.search('tiling: width1: ([-+]?\d*\.\d+|\d+)', line)
        if result_width1:
            width1 = result_width1.groups()[0]
            width1 = str(width1)
        result_position_angle = re.search('angle: ([-+]?\d*\.\d+|\d+)', line)
        if result_position_angle:
            position_angle = result_position_angle.groups()[0]
            position_angle = str(-float(position_angle))
        result_width2 = re.search('width2: ([-+]?\d*\.\d+|\d+) arcsec in equatorial plane', line)
        if result_width2:
            width2 = result_width2.groups()[0]
            width2 = str(width2)
#%% Convert TileSim output to ds9

    beam_positions = np.genfromtxt(workdir+'tilingCoord')
    region_file_handle = open((ds9_dir+'tiling_'+source_name+'.reg'),'w')
    region_file_handle.write('global color=black rotate=0 move=0 edit=0 width=2\n')
    region_file_handle.write('j2000\n')
    
        
    
    for beam in range(len(beam_positions[:,0])):
        region_file_handle.write('ellipse '+str(beam_positions[beam,0])+'d '+str(beam_positions[beam,1])+'d '+width1+'" '+width2+'" '+position_angle+'d \n')
    
    region_file_handle.close()
    os.remove(workdir+'tilingCoord')
    os.remove(workdir+'tiling.svg')
    os.remove(workdir+'tilingCoord_pixel')
    os.remove(workdir+'beamWithFit.png')



