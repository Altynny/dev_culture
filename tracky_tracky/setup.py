from setuptools import setup

setup(
   name='tracky_tracky',
   version='1.1',
   description='Provides a decorator for memory usage tracking. The part of FOSS course. Remastered by Ilya.',
   long_description_content_type='text/markdown',
   license='MIT',
   author='Artem Vesnin',
   author_email='artemvesnin@gmail.com',
   url='https://github.com/standlab/mtracker',
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