import os
from PIL import Image
from torch.utils.data import Dataset

class HexTypeDataset(Dataset):
    def __init__(self, root_dir, transform=None):
        self.root_dir = root_dir
        self.transform = transform
        self.classes = sorted(os.listdir(root_dir))
        self.class_to_idx = {cls: i for i, cls in enumerate(self.classes)}
        self.samples = self.load_samples()

    def load_samples(self):
        samples = []
        for cls in self.classes:
            cls_dir = os.path.join(self.root_dir, cls)
            for filename in os.listdir(cls_dir):
                if filename.endswith(".png"):
                    image_path = os.path.join(cls_dir, filename)
                    class_idx = self.class_to_idx[cls]
                    samples.append((image_path, class_idx))
        return samples

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        image_path, class_idx = self.samples[idx]
        image = Image.open(image_path).convert("RGB")
        if self.transform:
            image = self.transform(image)
        return image, class_idx, 0  # Assuming hex map labels are not used during training

