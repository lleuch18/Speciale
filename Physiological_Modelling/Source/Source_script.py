# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 03:03:13 2023

@author: Lasse
"""

import circadapt
import inspect


with open("circadapt.components" + ".txt","a") as f:
        print(inspect.getsource(circadapt.components),file=f)
