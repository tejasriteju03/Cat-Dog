import os
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
import matplotlib.pyplot as plt
import numpy
from torch.utils.data import Dataset, DataLoader
import glob
from PIL import Image


class datasetloader(Dataset):
    def __init__(self, path, transform=None):
        self.classes = os.listdir(path)
        self.classes = [i for i in self.classes if not i.startswith('.')]
        self.path = [f"{path}/{className}" for className in self.classes]
        self.file_list = [glob.glob(f"{x}/*") for x in self.path]
        self.transform = transform
        
        files = []
        for i, className in enumerate(self.classes):
            for fileName in self.file_list[i]:
                if not fileName.startswith('.'):  # Exclude hidden files
                    try:
                        im = Image.open(fileName)
                        files.append([i, className, fileName])
                    except:
                        print(f"Skipping {fileName} as it's not a valid image file.")
        self.file_list = files
        files = None
        
    def __len__(self):
        return len(self.file_list)

    def __getitem__(self, idx):
        fileName = self.file_list[idx][2]
        classCategory = self.file_list[idx][0]
        im = Image.open(fileName)
        if self.transform:
            im = self.transform(im)
        return im, classCategory