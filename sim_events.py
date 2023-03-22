import pulse_profile
import simconfig
import sim_spec
import numpy as np
import matplotlib.pyplot as plt
import pickle as pkl

class event():

    # simulation configs
    def __init__(self,freq_high,bw,nchan,ntsamp,tres):

        self.freq_high = freq_high
        self.bw = bw
        self.nchan = nchan
        self.freq_res = self.bw/self.nchan
        self.ntsamp = ntsamp
        self.tres = tres

    # calculate frequency value for each channel
    def get_freq(self):
        freqs = []
        for i in range(self.nchan):
            freqs.append(self.freq_high - i*self.freq_res)
        return np.array(freqs)

    # randomize dspec property
    def get_ds(self,hmeans,lammeans,sigmrng,murng):

        # randomize property
        h = np.random.normal(hmeans[0],hmeans[1])
        lam = np.random.normal(lammeans[0],lammeans[1])
        sigm = np.random.uniform(sigmrng[0],sigmrng[1], self.nchan)
        mu = np.random.uniform(murng[0],murng[1])

        # get ds
        ds = sim_spec.dspec()
        ds = ds.noise_chan(self.nchan,self.ntsamp,h,lam,sigm,mu)

        return ds.transpose() # need to transpose

    # gaussian profile
    def gauss_prof(self,x, x0,sigma):

        # convert the desired width w.r.t depending on the time resolution
        sigma = (sigma)/2.3548 # the width is evaluated at 50%
        prof = np.exp(-(x-x0)**2/(2*sigma**2))

        return prof/prof.max()

    # inject bursts
    def inject_burst(self,frame,fluence_range,width_rng,dm_rng,peak_location,burst_bw):

        # copy frame
        img = frame.copy()

        # randomize property
        DM = np.random.uniform(dm_rng[0], dm_rng[1])
        width = np.exp(np.random.uniform(np.log(width_rng[0]),np.log(width_rng[1])))
        fluence = np.random.uniform(fluence_range[0],fluence_range[1])
        arrv = int(np.round(np.random.uniform(0,int(2*self.ntsamp/3))))
        tau = np.exp(np.random.uniform(np.log(0.1), np.log(width)))

        # spectral structure
        peakl = np.random.uniform(peak_location[0], peak_location[1])
        burstbw = np.random.uniform(burst_bw[0], burst_bw[1])

        # create frb object
        frb = pulse_profile.pulse_profile(fluence,width,tau,DM)

        # get frequency and delay
        freqs = self.get_freq()
        delays = frb.time_delay(self.freq_high,freqs,self.tres)
        print(DM)
        print(fluence)
        print(width)
        #print(delays)
        # Inject into the image
        positions = np.arange(img.shape[1])

        # gaussian in spectral behaviour
        fr_pos = np.arange(img.shape[0])
        spec_flux = self.gauss_prof(fr_pos,peakl,burstbw)

        for i in range(len(img)):

            # arrival of the burst
            shift = arrv + delays[i]

            # verify that the arrival is within the frame
            if shift < img.shape[1]:
                pulse = frb.pulseprofile(positions, shift, self.tres, freqs[i],self.freq_high)
                img[i] = img[i] + pulse*spec_flux[i]

        return img, DM, fluence, width

def simul():
    cr_event = event(simconfig.freq_high,simconfig.bw,simconfig.nchan,simconfig.ntsamp,simconfig.tres)
    tds = cr_event.get_ds(simconfig.hmeans,simconfig.lammeans,simconfig.sigmrng,simconfig.murng)
    burst = cr_event.inject_burst(tds,simconfig.fluence_rng,simconfig.width_rng,simconfig.dm_rng,simconfig.peak_location,simconfig.burst_bw)
    return burst

# perform simulation
simev = simul()
bursts = []
for i in range(simconfig.nsim):
    bursts.append(simev[0])
bursts = np.array(bursts)

# savings
if simconfig.nsim:
    frbdict = {}
    for i in range(len(bursts)):

        frbdict[i] = bursts[i]

    # open a file, where you ant to store the data
    file = open(simconfig.filename, 'wb')
    pkl.dump(frbdict, file)
    file.close()
'''
plt.figure()
mytitle = r'DM = '+ str(int(simev[1])) + ' pc $cm^{-3}$, '
mytitle = mytitle + 'Fluence = '+str(int(simev[2])) + ' a.u ms, '
mytitle = mytitle + 'Width = '+str(int(simev[3])) + ' ms'
plt.title(mytitle,fontsize=10)
plt.xlabel('Time (ms)',fontsize=10)
plt.ylabel('Frequency (MHz)',fontsize=10)
plt.yticks([0,46,95],['1518','1374','1230'])
plt.imshow(bursts[0],cmap='gray_r')
cbar = plt.colorbar()
cbar.set_label('Arbitrary unit')
plt.clim(0,4)
plt.show()
'''
