import pandas as pd
import numpy as np
import os

"""
ratings.csv ist 877MB gross, es muss in mehrere gleiche Teile gesplittet werden
"""

# Anzahl der Zeilen in einer CSV Datei
n = 1_000_000


for i, segment in enumerate(pd.read_csv('../Data/ratings.csv', chunksize = n)):
    # erstelle neue Dateien
    segment.to_csv(f'../Data/ratings/ratings_{i}.csv')

