from setuptools import setup

setup(
   name='tracky_tracky',
   version='1.2',
   description='Provides a decorator for memory usage tracking. The part of FOSS course. Remastered by Ilya.',
   long_description_content_type='text/markdown',
   license='MIT',
   author='Ilya Altynnikov',
   author_email='altynnikovila@gmail.com',
   url='https://github.com/Altynny/dev_culture/tree/main/tracky_tracky',
   packages=['mtracker'], 
   install_requires=[], # it is empty since we use standard python library
   extras_require={
        'test': [
            'pytest',
            'coverage',
        ],
   },
   python_requires='>=3',
)