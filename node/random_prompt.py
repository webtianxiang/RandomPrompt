class RandomPrompt:
  def __init__(self):
    self.count = 0
  
  @classmethod
  def INPUT_TYPES(s):
    return {
      "required": {
        "clip": ("CLIP", ),
        "prompt_text_0": ("STRING",{"multiline": True}),
        "prompt_text_1": ("STRING",{"multiline": True}),
        "prompt_text_2": ("STRING",{"multiline": True}),
      },
      # "optional":{
      #   "prompt_text_0": ("STRING", ),
      #   "prompt_text_1": ("STRING",),
      #   "prompt_text_2": ("STRING",),
      # }
    }
  
  # RETURN_TYPES = ("STRING")
  RETURN_TYPES = ("CONDITIONING", "STRING")
  
  RETURN_NAMES = ("conditioning", "prompt")
  
  FUNCTION = "execution"
  
  CATEGORY = "tx_nodes"
  
  ALWAYS_EXECUTE = True
  
  def execution(self,clip,prompt_text_0,prompt_text_1,prompt_text_2):
    my_dict = {0:prompt_text_0, 1:prompt_text_1, 2:prompt_text_2}
    
    key = self.count % 3
    
    print("--------------[tx random prompt: key]-------------", key)
    print("--------------[tx random prompt: self.count]-------------", self.count)
    print("--------------[tx random prompt: my_dict]-------------", my_dict)
    
    self.count +=1
    
    tokens = clip.tokenize(my_dict[key])
    
    cond, pooled = clip.encode_from_tokens(tokens, return_pooled=True)
    
    return ([[cond, {"pooled_output": pooled}]],my_dict[key],)
  
  def IS_CHANGED(self):
    self.count += 1
    return True
    
  
NODE_CLASS_MAPPINGS = {
  "RandomPrompt": RandomPrompt
}

NODE_DISPLAY_NAME_MAPPINGS = {
  "RandomPrompt": "Tx Random Prompt"
}
  
