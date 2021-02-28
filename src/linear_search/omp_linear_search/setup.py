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
      name        = 'omp_linear_search',
      cmdclass    = {'build_ext':build_ext},
      include_dirs=[numpy.get_include()],
      ext_modules = [Extension("omp_linear_search",["omp_linear_search.pyx"], 
                               extra_compile_args=['/openmp'], 
                               extra_link_args=['/openmp'])]
      )

