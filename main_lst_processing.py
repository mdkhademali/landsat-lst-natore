import rasterio
import numpy as np
import os

# ---------------------------
# 1. Paths
# ---------------------------
input_file = 'data/landsat_band10.tif'
output_file = 'results/LST_Map.tif'

# Create results folder if it doesn't exist
os.makedirs('results', exist_ok=True)

# ---------------------------
# 2. Read Landsat Band 10
# ---------------------------
with rasterio.open(input_file) as src:
    DN = src.read(1).astype(float)
    profile = src.profile

# ---------------------------
# 3. Radiance → Brightness Temperature → LST
# ---------------------------
# Example constants (same as MATLAB version)
ML = 3.3420E-04
AL = 0.1
K1 = 774.8853
K2 = 1321.0789

# Radiance
radiance = ML * DN + AL

# Brightness Temperature
BT = K2 / np.log((K1 / radiance) + 1)

# LST (Celsius)
LST = BT - 273.15

# ---------------------------
# 4. Save LST map
# ---------------------------
profile.update(dtype=rasterio.float32, count=1)

with rasterio.open(output_file, 'w', **profile) as dst:
    dst.write(LST.astype(rasterio.float32), 1)

print(f"LST map saved to {output_file}")