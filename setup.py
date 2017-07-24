from distutils.core import setup

setup(name='pyPEC',
      version='0.1.0',
      author='Fabian Beutel',
      author_email='fabian.beutel@uni-muenster.de',

      packages=['pypec'],
      scripts=['bin/pypec'],

      url='https://zivgitlab.uni-muenster.de/beutelf/pyPEC',
      license='GPL v3',
      description='Simulate material stacks for proximity effect corrections (PEC) using PENELOPE.',

      install_requires=[
          'appdirs>=1.0.0',
          'ConfigArgParse>=0.12.0',
          'pyyaml'
      ],

      classifiers=[]
)
