from setuptools import setup

with open("README", 'r') as f:
    long_description = f.read()

setup(
   name='BoligaScraper',
   version='1.0',
   description='A module that can help read Boliga.dk',
   author='Henrik Christoffersen',
   author_email='hchristoffersen100@gmail.com',
   packages=['BoligaScraper'],
   install_requires=['pandas', 'numpy'],
   scripts=[
            'scripts/cool',
           ]
)
