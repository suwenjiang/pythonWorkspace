__author__ = 'jiangmb'
from distutils.core import setup
import py2exe
from glob import glob


data_files = [("Microsoft.VC90.CRT", glob(r'C:\Program Files (x86)\ArcGIS\Desktop10.3\bin\Microsoft.VC90.CRT\*.*'))]
setup(
    data_files=data_files,

)

setup(console=['BatchPublishMapService.py'])