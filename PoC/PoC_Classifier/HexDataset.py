import torch
from torch.utils.data import Dataset
import torch.optim as optim
from torchvision import transforms
from torch.utils.data import DataLoader
from PIL import Image
import os

class HexagonDataset(Dataset):
    def __init__(self, root_dir, transform=None):
        self.root_dir = root_dir
        self.transform = transform
        self.hexagon_types = os.listdir(root_dir)

    def __len__(self):
        return sum(len(os.listdir(os.path.join(self.root_dir, hexagon_type))) for hexagon_type in self.hexagon_types)

    def __getitem__(self, idx):
        hexagon_type_idx = 0
        while idx >= len(os.listdir(os.path.join(self.root_dir, self.hexagon_types[hexagon_type_idx]))):
            idx -= len(os.listdir(os.path.join(self.root_dir, self.hexagon_types[hexagon_type_idx])))
            hexagon_type_idx += 1

        hexagon_type = self.hexagon_types[hexagon_type_idx]
        hexagon_images = os.listdir(os.path.join(self.root_dir, hexagon_type))
        image_name = hexagon_images[idx]
        image_path = os.path.join(self.root_dir, hexagon_type, image_name)
        image = Image.open(image_path).convert('RGB')

        if self.transform:
            image = self.transform(image)

        return image, hexagon_type

