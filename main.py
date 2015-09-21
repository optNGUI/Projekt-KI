#!/usr/bin/env python3
# coding: utf8

"""
Entry point to opt_neuron package. Will pass the given arguments.
"""

import opt_neuron.run
import sys

if __name__ == "__main__":
    opt_neuron.run.run(sys.argv[1:])
