from astropy.coordinates import EarthLocation
from astropy.time import Time
from astropy import units as u

#LST at beginning of pointing is 06h49m:08s

MeerKAT_location = EarthLocation.from_geocentric( 5109360.133 ,  2006852.586  ,   -3238948.127 , unit=u.meter ) #this coordinates are taken from TEMPO

observing_time = Time('2020-11-30 12:43:58.53', format='iso', scale='utc', location=MeerKAT_location)
observing_time.sidereal_time('apparent')
