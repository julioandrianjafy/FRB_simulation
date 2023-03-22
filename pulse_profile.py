# generate normalized FRB pulse profile with scattering effects #
import numpy as np

class pulse_profile():

    def __init__(self,fluence,width,tau_0,dm):

        self.fluence = fluence
        self.width = width
        self.tau_0 = tau_0
        self.dm = dm

    # create the normalized gaussian function
     # create the normalized gaussian function
    def gauss_prof(self, x, x0, t_res):

        # convert the desired width w.r.t depending on the time resolution
        sigma = (self.width/t_res)/2.3548 # the width is evaluated at 50%
        prof = np.exp(-(x-x0)**2/(2*sigma**2))

        return prof/prof.max()

        # create scattering profile
    def scatt_prof(self,x, f, f_ref, t_res):

        if self.tau_0 != 0: # avoid division of 0
            t_scat = self.tau_0*(f/f_ref)**-4

            #  convert t_scat wrt to time resolution
            t_scat = t_scat/t_res

            s_prof = (1/t_scat)*np.exp(-x/t_scat)
            return s_prof/s_prof.max()

        else:
            print('tau_0 cannot be zero')

       # Calculate time delays in the image
    def time_delay(self, fref, f,t_res):

        # convert to Ghz
        lo = f*1e-3
        hi = fref*1e-3

        # calculate delay
        dt = 4.15*(lo**(-2) - hi**(-2))*self.dm
        return np.int32(np.round(dt/t_res))

    # convolve the signals
    def pulseprofile(self,x, x0, t_res, f, f_ref):

        amp = self.fluence/self.width

        # calculate gauss profile and scat profile
        gauss = self.gauss_prof(x, x0, t_res)
        scat = self.scatt_prof(x, f, f_ref, t_res)

        # convolve the two signals
        pulse = np.convolve(gauss, scat)[:len(x)] # Only up to half of the convoled signal

        return amp*(pulse/pulse.max()) # return the normalized pulse
