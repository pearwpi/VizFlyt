import numpy as np
import cv2
from PIL import Image

import torch
import torch.nn.functional as F
from torchvision import transforms
from torchvision.transforms import functional as TF

from drone_stack.window_seg import WindowSegmentationModel

"""This is a Placeholder perception module"""
class StudentPerception:
    
    def __init__(self, model_path):
        
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = WindowSegmentationModel(3, 1)
        
        self.model.to(self.device)
        
        # Load the pre-trained model
        self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.model.eval()
        
        self.i = 0
        
        print("Perception Module Initialized with model:", model_path)
    
    """
    Placeholder Perception Module.
    """
    def process_images(self, rgb_image, depth_image):
        """
        Dummy function to process images.
        Args:
            rgb_image: RGB Image from drone.
            depth_image: Depth Image from drone.
        Returns:
            Processed data (unused in this simple trajectory)
        """
        h, w = rgb_image.shape[:2]
        print(f"Processing images of size: {h}x{w}")
        
        # rgb_frame = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2RGB)
        im_pil = Image.fromarray(rgb_image)

        # convert them to tensors
        rgb = transforms.ToTensor()(im_pil).to(self.device) # (3, H, W)
        rgb = TF.resize(rgb, [256, 256], interpolation= TF.InterpolationMode.NEAREST_EXACT).unsqueeze(0)
        print('pre-model')
        pred = self.model(rgb).detach().squeeze()
        print('post-model')
        # print(torch.max(pred))
        new_pred = F.sigmoid(pred)
        # print(torch.max(new_pred), torch.min(new_pred))
        new_pred[new_pred > 0.5] = 1
        new_pred[new_pred <= 0.5] = 0
        
        new_pred = new_pred.cpu().numpy().astype(np.uint8) * 255
        new_pred = cv2.resize(new_pred, (w, h), interpolation=cv2.INTER_NEAREST)
        new_pred = cv2.cvtColor(new_pred, cv2.COLOR_GRAY2BGR)
        
        # apply colormap to depth im (currently grayscale)
        depth_image = cv2.applyColorMap(depth_image.astype(np.uint8), cv2.COLORMAP_JET)
        
        # print(rgb_image.shape, depth_image.shape, new_pred.shape)
        
        # save concatenated image
        concat_image = np.concatenate((rgb_image, depth_image, new_pred), axis=1)
        cv2.imwrite(f"debug/output_image_{self.i}.png", concat_image)
        self.i += 1
        print(f"Processed images and saved output_image_{self.i}.png")
        return new_pred
