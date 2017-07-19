#!/usr/bin/env python

# pyPEC 0.x by Fabian Beutel (fabian.beutel@uni-muenster.de)
# Based on scripts by Silvia Diewald (silvia.diewald@kit.edu) 

import yaml
from pec_params import PecParams
import sys


simulation_directory = "simulation" # path to directory where all stack_directories are located
database_directory = "database" # path to database directory (contains PENELOPE material (.mat) files)
stack_directory = "" # name of subdirectory where all files needed for a simulation run are located
path_input_file = "" # path to the PENELOPE input file
path_stack_file = "" # path to stack file
path_layer_file = "" # path to layer file
path_pencyl_binary = "" # path to pencyl binary

"""if len(sys.argv) < 2:
    # todo: display usage
    raise Exception("Please provide input yaml file")

infile = sys.argv[1]"""

with open("../examples/stack1.yml") as f:
    data = yaml.load(f)
    
params = PecParams()

def read_number(s, unit):
    # todo: read other units
    if len(s) <= len(unit) or not s.endswith(unit):
        raise Exception("Invalid number {0}. Expected format '123{1}'.".format(s, unit))
    return int(s[:-len(unit)].strip())

if not "stack" in data:
    raise Exception("No stack defined in yaml file.")
elif type(data["stack"]) is list:
    for d in data["stack"]:
        mat, thick = d.items()[0]
        params.stack_material.append(mat)
        try:
            params.layer_thickness.append(read_number(thick, "nm"))
        except Exception as e:
            raise Exception("{0}: {1}".format(mat, e))
# todo: else: if type is string, read from .stack file

if "voltage" in data:
    params.acceleration_voltage = read_number(data['voltage'], "kV")