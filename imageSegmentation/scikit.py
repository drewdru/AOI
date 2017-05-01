import numpy as np
from scipy.cluster.vq import kmeans2
from scipy import ndimage as ndi
import matplotlib.pyplot as plt

from skimage import data
from skimage import color
from skimage.util.shape import view_as_windows
from skimage.util.montage import montage2d
from PIL import Image
np.random.seed(42)

patch_shape = 8, 8
n_filters = 49

def load_image( infilename ) :
    img = Image.open( infilename )
    img.load()
    data = np.asarray( img, dtype="int32" )
    return data

def save_image( npdata, outfilename ) :
    img = Image.fromarray( np.asarray( np.clip(npdata,0,255), dtype="uint8"), "L" )
    img.save( outfilename )

img = load_image("paramount.jpg")

astro = color.rgb2hsv(img)
astro = color.rgb2gray(img)

# -- filterbank1 on original image
patches1 = view_as_windows(astro, patch_shape)
patches1 = patches1.reshape(-1, patch_shape[0] * patch_shape[1])[::8]
fb1, _ = kmeans2(patches1, n_filters, minit='points')
fb1 = fb1.reshape((-1,) + patch_shape)
fb1_montage = montage2d(fb1, rescale_intensity=True)

# -- filterbank2 LGN-like image
astro_dog = ndi.gaussian_filter(astro, .5) - ndi.gaussian_filter(astro, 1)
patches2 = view_as_windows(astro_dog, patch_shape)
patches2 = patches2.reshape(-1, patch_shape[0] * patch_shape[1])[::8]
fb2, _ = kmeans2(patches2, n_filters, minit='points')
fb2 = fb2.reshape((-1,) + patch_shape)
fb2_montage = montage2d(fb2, rescale_intensity=True)

# --
fig, axes = plt.subplots(2, 2, figsize=(7, 6))
ax0, ax1, ax2, ax3 = axes.ravel()

ax0.imshow(astro, cmap=plt.cm.gray)
ax0.set_title("Image (original)")

ax1.imshow(fb1_montage, cmap=plt.cm.gray, interpolation='nearest')
ax1.set_title("K-means filterbank (codebook)\non original image")

ax2.imshow(astro_dog, cmap=plt.cm.gray)
ax2.set_title("Image (LGN-like DoG)")

ax3.imshow(fb2_montage, cmap=plt.cm.gray, interpolation='nearest')
ax3.set_title("K-means filterbank (codebook)\non LGN-like DoG image")

for ax in axes.ravel():
    ax.axis('off')

fig.subplots_adjust(hspace=0.3)
plt.show()
