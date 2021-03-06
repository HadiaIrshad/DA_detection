import glob
import random
import os

from torch.utils.data import Dataset
from PIL import Image
import torchvision.transforms as transforms

class ImageDataset(Dataset):
    def __init__(self, root, transforms_=None, unaligned=False, mode='train'):
        self.transform = transforms.Compose(transforms_)
        self.unaligned = unaligned

        #self.files_A = sorted(glob.glob(os.path.join(root, '%s/A' % mode) + '/*.*'))
        #self.files_B = sorted(glob.glob(os.path.join(root, '%s/B' % mode) + '/*.*'))
        kitti_mode = mode
        kitti_root = './data/KITTI/training/image_2/'
        
        with open('./data/KITTI/training/ImageSets/trainval.txt', 'r') as f:
            inds = f.readlines()
        
        self.files_A  = sorted([kitti_root + i.strip() + '.png' for i in inds])
        self.files_B = sorted(glob.glob('./data/CityScapes/leftImg8bit/val/*/*.*'))
        print(len(self.files_A), len(self.files_B)) 
    def __getitem__(self, index):
        item_A = self.transform(Image.open(self.files_A[index % len(self.files_A)]))

        if self.unaligned:
            item_B = self.transform(Image.open(self.files_B[random.randint(0, len(self.files_B) - 1)]))
        else:
            item_B = self.transform(Image.open(self.files_B[index % len(self.files_B)]))

        return {'A': item_A, 'B': item_B, 'A_path': self.files_A[index % len(self.files_A)], 'B_path': self.files_B[index % len(self.files_B)]}

    def __len__(self):
        return max(len(self.files_A), len(self.files_B))
