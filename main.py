#!/usr/bin/env python3
# coding: utf8

### Calls the opt_neuron package. ###

import opt_neuron.run
import sys

if __name__ == "__main__":
    opt_neuron.run.run(sys.argv[1:])
