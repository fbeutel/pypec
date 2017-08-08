pyPEC
========

Author: Fabian Beutel (fabian.beutel@uni-muenster.de)

pyPEC is a small package to perform Monte Carlo simulations to be used for proximity corrections for E-Beam lithography.

The software uses PENELOPE (https://www.oecd-nea.org/tools/abstract/detail/nea-1525) to perform the simulations.
It is based on scripts written originally by Silvia Diewald (silvia.diewald@kit.edu).

Installation
--------------

The software can be installed like any other python package. For example, to directly install it from the repository:

  pip install git+https://zivgitlab.uni-muenster.de/beutelf/pyPEC.git

  
Configuration
--------------

pyPEC needs to be able to find the *pencyl* executable and the material (.mat) files. By default, the paths are:
 - pencyl_path: ~/.local/share/pyPEC/pencyl
 - database directory: ~./local/share/pyPEC/database

These paths can be changed in a config file (located usually in ~/.config/pyPEC/config.ini) or by passing the corresponding command line arguments.


Run
--------------

Run the program by calling

  pypec stack.yml
  
where stack.yml is a YAML formatted file as follows:

    stack:
        - PMMA: 200nm
        - Si3N4: 350nm
        - SiO2: 200nm
        - Si: 800nm
    voltage: 100kV
    relative_z: 0.5
    
The last two lines are optional.
