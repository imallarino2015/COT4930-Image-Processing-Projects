from distutils.core import setup, Extension

rng_module=Extension('rng',sources=['rng.c'])

setup(
    name='rng',
    version=1,
    description='Random number generation module',
    ext_modules=[rng_module]
)
