import os
from PIL import Image, ImageOps, ImageSequence
import numpy as np
import torch


class TxInputNode:
  def __init__(self):
      self.count  = 0
      print('------------tx __init__-------------', self)

  @classmethod
  def INPUT_TYPES(s):
    # input_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input")
    input_dir = os.path.abspath("/Users/bytedance/tianxiang/projectTry/ComfyUI/input")
    files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
    
    return {
      "required": {
        "prompt_text": ("STRING", {"default": "tx_test_prompt"}),
      },
      "optional": {
        "image": (sorted(files), { "image_upload": True }),
        # 内置
        "model": ("MODEL",),
        "clip": ("CLIP", ),
        # "clip_vision": ("CLIP_VISION",),
        # "control_net": ("CONTROL_NET", ),
        "conditioning": ("CONDITIONING", ),
        # "mask": ("MASK", ),
        "samples": ("LATENT", ),
        "vae": ("VAE", ),
        # "pixels": (sorted(files), { "image_upload": True }),
        # "prompt": "PROMPT", 
        # "extra_pnginfo": "EXTRA_PNGINFO",
        # "style_model": ("STYLE_MODEL", ),
        # "clip_vision_output": ("CLIP_VISION_OUTPUT", ),
        # "gligen_textbox_model": ("GLIGEN", ),
        # "test_bool": ("BOOL", { "default": False}),
        "multiple_prompt": ("STRING", { "default": "tx_test__muli_prompt", "multiline": True}),
        "test_array": (["a", "b"], { "default": "a"}),
        "conditioning_to_strength": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
        "x": ("INT", {"default": 0, "min": 0, "max": 100, "step": 8}),
        "y": ("INT", {"default": 0, "min": 0, "max": 100, "step": 8}),
      }
    }
    
  RETURN_TYPES = ("STRING", "IMAGE")
  
  RETURN_NAMES = ("文字", "图片")
  
  FUNCTION = "test"
  
  OUTPUT_NODE = False
  
  CATEGORY = "tx_nodes"

  # def test(self, prompt_text,image,model,clip,clip_vision,control_net,conditioning,mask,samples,vae,prompt,extra_pnginfo,style_model,clip_vision_output,
  #   gligen_textbox_model,multiple_prompt,test_array,conditioning_to_strength,x,y):
  #   self.count += 1
  #   print('------------tx params-------------',prompt_text,image,model,clip,clip_vision,control_net,conditioning,mask,samples,vae,prompt,extra_pnginfo,style_model,clip_vision_output,
  #   gligen_textbox_model,multiple_prompt,test_array,conditioning_to_strength,x,y)
  #   print('------------tx self.count-------------', self.count)
  #   return "tx-return-type"
  
  def test(self, prompt_text,image,model,clip,conditioning,samples,vae,multiple_prompt,test_array,conditioning_to_strength,x,y):
    self.count += 1
    print('------------tx params-------------',prompt_text,image,model,clip,conditioning,samples,vae,multiple_prompt,test_array,conditioning_to_strength,x,y)
    print('------------tx self.count-------------', self.count)
    
    image_path = os.path.join(os.path.abspath("/Users/bytedance/tianxiang/projectTry/ComfyUI/input"), image)
    img = Image.open(image_path)
    output_images = []
    for i in ImageSequence.Iterator(img):
        i = ImageOps.exif_transpose(i)
        if i.mode == 'I':
            i = i.point(lambda i: i * (1 / 255))
        image = i.convert("RGB")
        image = np.array(image).astype(np.float32) / 255.0
        image = torch.from_numpy(image)[None,]
        if 'A' in i.getbands():
            mask = np.array(i.getchannel('A')).astype(np.float32) / 255.0
            mask = 1. - torch.from_numpy(mask)
        else:
            mask = torch.zeros((64,64), dtype=torch.float32, device="cpu")
        output_images.append(image)

    if len(output_images) > 1:
        output_image = torch.cat(output_images, dim=0)
    else:
        output_image = output_images[0]
    return (prompt_text + multiple_prompt, output_image)

NODE_CLASS_MAPPINGS = {
  "TxInputNode": TxInputNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
  "TxInputNode": "Tx Input Node"
}