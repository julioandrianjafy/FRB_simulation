# FRB_simulation
## Simulation of frb pulses in simulated dynamic spectrum
The initial purpose of this project is to create samples of FRB data to train machine learning classifier. Although some FRB might exhibit more complex structure, the simulated features implemented here could be sufficient for a baseline model to identify FRB in real observations.   

## 1) Dynamic spectrum simulation 
In the absence of spectrogram templates from real observations, we created simulated data cubes to inject the simulated bursts. This provides flexibility in adopting different telescope configurations (nfreq, integration time, etc) which could be modified in simconfig.py. For now, the simulated spectrogram is built with multivariate normal distribution and a squared exponential covariance kernel whose paramters range can also be modified in simconfig.py. Changing the kernel or even adding some RFI-like signal could be introduced in the future.

## 2) Injecting the burst 
The burst feature is parameterized by its fluence, dispersion measure, width, scattering timescale ranges (check simconfig.py). The spectral behaviour is regulated by a normalized gaussian profile across the frequency with the peak situated randomly at different frequency location. The final simulation could be saved in a pickle file.  

## 3) Running the script
The simulation parameters could be modified in simconfig.py and the final simulation could be performed simply with **Python3 sim_events.py**

## 4) Examples
The figures below plot example of the simulated burts using telescope configurations similar to the Parkes radio telescope FRB search mode 
Example 1                  |  Example 2
:-------------------------:|:-------------------------:
![](https://github.com/julioandrianjafy/FRB_simulation/blob/main/im0.png)  |  ![](https://github.com/julioandrianjafy/FRB_simulation/blob/main/im1.png)
