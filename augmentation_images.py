import numpy as np
import torch
import torchvision
from PIL import Image
import glob

from matplotlib import pyplot as plt
from torchvision import transforms


def show(img):
    npimg = img.numpy()
    plt.imshow(np.transpose(npimg, (1, 2, 0)), interpolation='nearest')

none = []
for filename in sorted(glob.glob('image_comp/none*.png')):
    im=Image.open(filename)
    none.append(im)

full = []
for filename in sorted(glob.glob('image_comp/full*.png')):
    im=Image.open(filename)
    full.append(im)

reduced = []
for filename in sorted(glob.glob('image_comp/reduced*.png')):
    im=Image.open(filename)
    reduced.append(im)

noaa = []
for filename in sorted(glob.glob('image_comp/noaa*.png')):
    im=Image.open(filename)
    noaa.append(im)

images = np.concatenate((none, full, reduced, noaa))
images = np.array(list(map(transforms.ToTensor(), images)))
images = torch.from_numpy(images)
grid = torchvision.utils.make_grid(images, nrow=5, normalize=True)
show(grid)
plt.tight_layout()
plt.savefig("image_transforms.png", dpi=300)