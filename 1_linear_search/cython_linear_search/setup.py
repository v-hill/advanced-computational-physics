"""
setup.py

To build this file run the command from within anaconda prompt:
    python setup.py build_ext --inplace --compiler=msvc
"""

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

import numpy
setup(
      name        = 'linear_search',
      cmdclass    = {'build_ext':build_ext},
      include_dirs=[numpy.get_include()],
      ext_modules = [Extension("openmp_linear_search",["openmp_linear_search.pyx"], 
                               extra_compile_args=['-fopenmp'], 
                               extra_link_args=['-fopenmp'])]
      )

