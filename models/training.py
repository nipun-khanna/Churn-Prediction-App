from transformers import LayoutLMv3FeatureExtractor, LayoutLMv3TokenizerFast, LayoutLMv3Processor, LayoutLMv3ForSequenceClassification
from tqdm import tqdm
import torch
from torch.utils.data import Dataset, DataLoader
import pytorch_lightning as pl
from pytorch_lightning.callbacks import ModelCheckpoint
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from sklearn.model_selection import train_test_split
import imgkit
import easyocr
import torchvision.transforms as T
from pathlib import Path
import matplotlib.pyplot as plt
import os
import cv2
from typing import List
import json
from torchmetrics import Accuracy
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
WKPATH = os.getenv("WKPATH")
config = imgkit.config(wkhtmltoimage=WKPATH)

# Setup
pl.seed_everything(42)

def convert_to_image(file_path: Path, images_dir: Path, scale: float = 1.0) -> Path:
    file_name = file_path.with_suffix(".jpg").name
    save_path = images_dir / f"{file_name}"
    imgkit.from_file(str(file_path), save_path, options={"quiet": "", "format": "jpeg"})

    image = Image.open(save_path)
    width, height = image.size
    image = image.resize((int(width * scale), int(height * scale)))
    image.save(str(save_path))
    return save_path