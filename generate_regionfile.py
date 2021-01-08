#%% Import packages
import os, subprocess
import numpy as np
import re


#%% TO RUN THIS ON DOKIMI
#conda activate py27 #to run tilesim in anaconda installation of mosaic which is written in python 2
#python3 gen_regionfile.py # to run this script in python 3

#%% Set observation variables
workdir = '/raid/ecarli/SMC/mosaic_SMC_beamforming/2nd_Pointing_0055-7226/'
ds9_dir = '/raid/ecarli/SMC/ds9_SMC_targets/Regions/2nd_Pointing_0055-7226/Tilings/'
observation_date = '2020.01.12' #YYYY.MM.DD
middle_of_obs_time = '11:30:00.00' #UTC
beam_total = 480

maximum_dishes_number = 47
formatter = '{:03d}'.format #mosaic needs leading zeros so that each dish number has 3 digits
dishes_list = list(map(formatter,list(range(0,maximum_dishes_number+1))))
dishes = ','.join(map(str,dishes_list))

#%% Set sources

tiling_centres = ['0:59:27.70 -72:10:10.0','0:52:59.90 -72:36:47.0', '0:56:28.10 -72:09:42.2','0:57:49.90 -72:11:47.1','0:56:25.00 -72:19:05.0','0:55:14.6910 -72:26:06.899']
source_names = ['SNR0059-7210','SNR0052-7236','CandSNR0056-7209', 'CandSNR0057-7211', 'CandSNR0056-7219', 'boresight']
numbers_of_beams = [25,100,90,30,60,175]


print('There are '+str(beam_total-sum(numbers_of_beams))+' beams left.')


for tiling_centre, source_name, number_of_beams in zip(tiling_centres, source_names, numbers_of_beams):
#%% Build TileSim command

    tilesim_command = 'python ~/PULSAR_SOFTWARE/mosaic/mosaic/tilesim.py --ants antenna.csv --freq 1.284e9 --source '+tiling_centre+'  --datetime '+observation_date+' '+middle_of_obs_time+' --beamnum '+str(number_of_beams)+'  --verbose --overlap 0.75 --resolution 1 --size 1000 --subarray '+dishes
    

#%% Run TileSim

    os.system('cd '+workdir)
    tilesim_run = subprocess.run(tilesim_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    
    if number_of_beams != 1:
        tilesim_stdout_handle =  open(workdir+'Outputs/output_tiling_'+source_name, 'w')
    else:
        tilesim_stdout_handle =  open(workdir+'Outputs/output_beam_'+source_name, 'w')    
    
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
    if number_of_beams != 1:
        region_file_handle = open((ds9_dir+'tiling_'+source_name+'.reg'),'w')
    else:
        region_file_handle = open((ds9_dir+'beam_'+source_name+'.reg'),'w')
    region_file_handle.write('global color=black rotate=0 move=0 edit=0 width=2\n')
    region_file_handle.write('j2000\n')
    
        
    
    for beam in range(len(beam_positions[:,0])):
        region_file_handle.write('ellipse '+str(beam_positions[beam,0])+'d '+str(beam_positions[beam,1])+'d '+width1+'" '+width2+'" '+position_angle+'d \n')
    
    region_file_handle.close()
    os.remove(workdir+'tilingCoord')
    os.remove(workdir+'tiling.svg')
    os.remove(workdir+'tilingCoord_pixel')
    os.remove(workdir+'beamWithFit.png')


