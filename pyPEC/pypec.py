#!/usr/bin/env python

# pyPEC 0.x by Fabian Beutel (fabian.beutel@uni-muenster.de)
# Based on scripts by Silvia Diewald (silvia.diewald@kit.edu) 

import yaml
import sys
import os
import pen_generators
from pec_params import PecParams
from pen_extractor import extract_xrz

simulation_directory = "simulation" # path to directory where all stack_directories are located
database_directory = "/mnt/fabianlaptop1/users/fabian/data/studium/Promotion/Software/pyPEC/database" # path to database directory (contains PENELOPE material (.mat) files)
pencyl_path = "/mnt/fabianlaptop1/users/fabian/data/studium/Promotion/Software/penelope/silvia/bin/pencyl"

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
    params.layer_max_number = len(data["stack"])
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

if "target_z" in data:
    params.target_z = read_number(data['target_z'], "nm")
elif "relative_z" in data:
    params.relative_z = float(data['relative_z'])
    

# Generate files
params.make_bodies()
params.make_title()

stack_directory = os.path.join(simulation_directory, params.title)
if not os.path.isdir(stack_directory):
    os.makedirs(stack_directory)

pen_in = pen_generators.generate_in_file(params, os.path.join(stack_directory, params.title + ".in"))
pen_generators.generate_layer_file(params, os.path.join(stack_directory, params.title.rstrip("_" + str(params.acceleration_voltage) + "keV") + ".layer" + ".layer"))
pen_generators.generate_stack_file(params, os.path.join(stack_directory, params.title + ".stack"))

# Link material files
for mat in params.stack_material:
    p = os.path.join(stack_directory, mat+".mat")
    if not os.path.exists(p):
        os.symlink(os.path.join(database_directory, mat+".mat"), p)

# Run pencyl simulation
os.chdir(stack_directory)
from subprocess import Popen, PIPE, STDOUT

p = Popen([pencyl_path], stdout=PIPE, stdin=PIPE, stderr=STDOUT)    
grep_stdout = p.communicate(input=pen_in)[0]
print(grep_stdout.decode())


extract_xrz(params.target_z)