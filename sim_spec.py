import numpy as np
#import simconfig as sm

# the plan is to create spectrogram with multivariate gaussian
# The noise for each freq channel will be correlated added with some independent random components
class dspec():

    # step1: create covariance kernel
    def cov_kernel(self,x1,x2,h,lam):

        ''' squared-exponential covariance kernel '''

        return h**2*np.exp(-(x1-x2)**2/lam**2)
    # lam determine the smoothness of the function (width of the covariance)
    # large value will increase the correlation btw 2 distant points

    # step2: create covariance matrix
    def make_K(self,x,h,lam):

        K = np.zeros((len(x),len(x)))

        for i in range(len(x)):
            for j in range(len(x)):
                K[i][j] = self.cov_kernel(x[i],x[j],h,lam)
        return K

    # step3: add the independent noise (create a diagonal matrix with the noise)
    # the diagonal elements are the variances of each channel
    def noise_chan(self,nchan,ntime, h, lam, sigm, mu):

        # create the position
        pos = np.arange(nchan)

        # make the covariance
        cov = self.make_K(pos, h, lam) + np.diag(sigm)

        # vary the mean for each spec
        meann = mu*np.ones_like(pos)

        return np.random.multivariate_normal(meann, cov, size=ntime)
