from setuptools import setup

setup(
   name='ants',
   version='1.0',
   description='Finds the shortest route in graph via ant algorithm.',
   license='MIT',
   author='Ilya Altynnikov',
   author_email='altynnikovila@gmail.com',
   url='https://github.com/Altynny/dev_culture/tree/main/pypi/ants',
   packages=['ants'],
   install_requires=[],
   extras_require={
        'test': [
            'pytest',
            # 'coverage',
        ],
   },
   python_requires='>=3',
)