# =============================================================================
# # -*- coding: utf-8 -*-
# """
# Created on Mon Sep 25 11:35:19 2023
# 
# @author: Lasse
# """
# 
import circadapt
import circadapt.plot
from circadapt.model import Model
from circadapt.adapt import ModelAdapt
from circadapt.plot import triseg2022, mmode
import matplotlib.pyplot as plt
import numpy as np

# %% Testing_Section
from PPV_Model import PPV_Model as ppv

model = ppv()

    