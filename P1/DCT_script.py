# Import functions and libraries
import numpy as np
import matplotlib.pyplot as plt
import scipy
from numpy import r_
from scipy import signal
from scipy import misc
import matplotlib.pylab as pylab


# we define a 2D DCT function
def dct2(a):
    dct_1D = scipy.fftpack.dct(a, axis=0, norm='ortho')
    return scipy.fftpack.dct(dct_1D, axis=1, norm='ortho')


# we define a 2D inverse DCT function
def idct2(a):
    idct_1D = scipy.fftpack.idct(a, axis=0, norm='ortho')
    return scipy.fftpack.idct(idct_1D, axis=1, norm='ortho')


im = plt.imread("B.png").astype(float)  # we load a png image

# We perform a blockwise DCT
dct = np.zeros(im.shape)


# input parameters from terminal
bloc_size = int(input("Enter bloc size N (NxN): "))

for i in r_[:im.shape[0]:bloc_size]:
    for j in r_[:im.shape[1]:bloc_size]:
        dct[i:(i+bloc_size), j:(j+bloc_size)] = dct2(im[i:(i+bloc_size), j:(j+bloc_size)])
        

# Display entire DCT
plt.figure()
plt.imshow(dct, cmap='gray', vmax=np.max(dct)*0.01, vmin=0)
plt.title("DCTs of the image")
plt.show()

# Threshold
thresh = 0.012
dct_thresh = dct * (abs(dct) > (thresh*np.max(dct)))

percent_nonzeros = np.sum(dct_thresh != 0.0) / (im.shape[0]*im.shape[1]*1.0)

print("Keeping only %f%% of the DCT coefficients" % (percent_nonzeros*100.0))

# We perform a blockwise IDCT
im_dct = np.zeros(im.shape)

# Do 8x8 inverse DCT on image (in-place)
for i in r_[:im.shape[0]:bloc_size]:
    for j in r_[:im.shape[1]:bloc_size]:
        im_dct[i:(i+bloc_size), j:(j+bloc_size)] = idct2(dct_thresh[i:(i+bloc_size), j:(j+bloc_size)])
        
plt.figure()
# Compare DCT compressed image with original
plt.imshow(np.hstack((im, im_dct)), cmap='gray')
plt.title("Comparison between original and DCT compressed images")
plt.show()


