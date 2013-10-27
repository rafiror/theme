from distutils.core import setup
from Cython.Build import cythonize

setup(name = 'cython_test_def',
      ext_modules = cythonize('cython_test_def.pyx'))
