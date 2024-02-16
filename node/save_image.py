import json
from PIL import Image, ImageOps, ImageSequence
from PIL.PngImagePlugin import PngInfo
import numpy as np
import os

def get_save_image_path(filename_prefix, output_dir, image_width=0, image_height=0):
    def map_filename(filename):
        prefix_len = len(os.path.basename(filename_prefix))
        prefix = filename[:prefix_len + 1]
        try:
            digits = int(filename[prefix_len + 1:].split('_')[0])
        except:
            digits = 0
        return (digits, prefix)

    def compute_vars(input, image_width, image_height):
        input = input.replace("%width%", str(image_width))
        input = input.replace("%height%", str(image_height))
        return input

    filename_prefix = compute_vars(filename_prefix, image_width, image_height)

    subfolder = os.path.dirname(os.path.normpath(filename_prefix))
    filename = os.path.basename(os.path.normpath(filename_prefix))

    full_output_folder = os.path.join(output_dir, subfolder)

    if os.path.commonpath((output_dir, os.path.abspath(full_output_folder))) != output_dir:
        err = "**** ERROR: Saving image outside the output folder is not allowed." + \
              "\n full_output_folder: " + os.path.abspath(full_output_folder) + \
              "\n         output_dir: " + output_dir + \
              "\n         commonpath: " + os.path.commonpath((output_dir, os.path.abspath(full_output_folder))) 
        print(err)
        raise Exception(err)

    try:
        counter = max(filter(lambda a: a[1][:-1] == filename and a[1][-1] == "_", map(map_filename, os.listdir(full_output_folder))))[0] + 1
    except ValueError:
        counter = 1
    except FileNotFoundError:
        os.makedirs(full_output_folder, exist_ok=True)
        counter = 1
    return full_output_folder, filename, counter, subfolder, filename_prefix


class TxSaveImage:
  def __init__(self):
    # 获取当前文件的绝对路径
    curr_file_path = os.path.abspath(__file__)
    print(f"Current file path: {curr_file_path}")
    # 使用os.path.dirname获取当前文件的上级目录
    parent_dir = os.path.dirname(curr_file_path)
    
    self.type = 'output'
    self.prefix_append = ""
    self.compress_level = 4
    self.output_dir = os.path.join(os.path.dirname(parent_dir), 'output')
    self.parent_dir = parent_dir
  
  @classmethod
  def INPUT_TYPES(s):
    return {
      "required": {
        "images": ("IMAGE", ),
        "filename_prefix": ("STRING", {"default": "ComfyUI"}),
      },
      "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
    }

  RETURN_TYPES = ()
  
  RETURN_NAMES = ()
  
  FUNCTION = "save_images"

  OUTPUT_NODE = True
  
  CATEGORY = "tx_nodes"
  
  def save_images_to_preview(self, images, filename_prefix="ComfyUI", prompt=None, extra_pnginfo=None):
    filename_prefix += self.prefix_append
    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(self.parent_dir))), 'output')
    full_output_folder, filename, counter, subfolder, filename_prefix = get_save_image_path(filename_prefix, output_dir, images[0].shape[1], images[0].shape[0])
    results = list()
    for image in images:
        i = 255. * image.cpu().numpy()
        img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
        
        metadata = PngInfo()
        
        if prompt is not None:
            metadata.add_text("prompt", json.dumps(prompt))
        if extra_pnginfo is not None:
            for x in extra_pnginfo:
                metadata.add_text(x, json.dumps(extra_pnginfo[x]))

        file = f"{filename}_{counter:05}_.png"
        img.save(os.path.join(full_output_folder, file), pnginfo=metadata, compress_level=self.compress_level)
        results.append({
            "filename": file,
            "subfolder": subfolder,
            "type": self.type
        })
        print("-----------------tx save image to preview---------------", full_output_folder, subfolder)
        counter += 1
    return { "ui": { "images": results } }
  
  def save_images(self, images, filename_prefix="ComfyUI", prompt=None, extra_pnginfo=None):
    filename_prefix += self.prefix_append
    full_output_folder, filename, counter, subfolder, filename_prefix = get_save_image_path(filename_prefix, self.output_dir, images[0].shape[1], images[0].shape[0])
    # results = list()
    for image in images:
        i = 255. * image.cpu().numpy()
        img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
        
        metadata = PngInfo()
        
        if prompt is not None:
            metadata.add_text("prompt", json.dumps(prompt))
        if extra_pnginfo is not None:
            for x in extra_pnginfo:
                metadata.add_text(x, json.dumps(extra_pnginfo[x]))

        file = f"{filename}_{counter:05}_.png"
        img.save(os.path.join(full_output_folder, file), pnginfo=metadata, compress_level=self.compress_level)
        # results.append({
        #     "filename": file,
        #     "subfolder": subfolder,
        #     "type": self.type
        # })
        print("-----------------tx save image---------------", full_output_folder, subfolder)
        counter += 1
    # return { "ui": { "images": [] } }
    return self.save_images_to_preview(images, filename_prefix="ComfyUI", prompt=None, extra_pnginfo=None)
  
NODE_CLASS_MAPPINGS = {
  "TxSaveImage": TxSaveImage
}

NODE_DISPLAY_NAME_MAPPINGS = {
  "TxSaveImage": "Tx Save Image"
}
  
