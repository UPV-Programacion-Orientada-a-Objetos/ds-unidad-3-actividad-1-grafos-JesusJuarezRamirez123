from setuptools import setup, Extension
from Cython.Build import cythonize
import os

# Definir la extension
extensions = [
    Extension(
        "neuronet",
        sources=["neuronet.pyx", "src/GrafoDisperso.cpp"],
        include_dirs=["src"],  # Para encontrar los headers .h
        language="c++",
        extra_compile_args=["-std=c++14"],
    )
]

setup(
    name="neuronet",
    ext_modules=cythonize(extensions, compiler_directives={'language_level': "3"}),
)
