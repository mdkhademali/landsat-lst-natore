
% =========================================================
% Main Script: Land Surface Temperature (LST) Mapping
% =========================================================
clc; clear;

% Input thermal band (example name)
thermalBand = 'data/landsat_band10.tif';

% Radiometric calibration constants (example values)
ML = 3.3420E-04;
AL = 0.1;
K1 = 774.8853;
K2 = 1321.0789;

% Read raster
[DN, R] = readgeoraster(thermalBand);
DN = double(DN);

% Step 1: DN to Radiance
radiance = ML .* DN + AL;

% Step 2: Radiance to Brightness Temperature
BT = K2 ./ log((K1 ./ radiance) + 1);

% Step 3: Simple LST estimation (Kelvin to Celsius)
LST = BT - 273.15;

% Save output
outputFile = 'results/LST_Map.tif';
geotiffwrite(outputFile, LST, R);

fprintf('LST processing completed successfully!\n');
