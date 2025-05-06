from setuptools import setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
setup(
   name='ants',
   version='1.0',
   description='Finds the shortest route in graph via ant algorithm.',
   long_description=long_description,
   long_description_content_type='text/markdown',
   license='MIT',
   author='Ilya Altynnikov',
   author_email='altynnikovila@gmail.com',
   url='https://github.com/Altynny/dev_culture/tree/main/pypi/ants',
   packages=['ants'],
   install_requires=[],
   extras_require={
        'test': [
            'pytest',
            'coverage',
        ],
   },
   python_requires='>=3',
)