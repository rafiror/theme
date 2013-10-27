from distutils.core import setup
from Cython.Build import cythonize

setup(name = 'map_cal',
      ext_modules = cythonize('map_cal.pyx'))
