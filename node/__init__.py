from . import tx_input_node as tip
from . import random_prompt as rp
from . import save_image as si

NODE_CLASS_MAPPINGS = {
  **tip.NODE_CLASS_MAPPINGS,
  **rp.NODE_CLASS_MAPPINGS,
  **si.NODE_CLASS_MAPPINGS
}

NODE_DISPLAY_NAME_MAPPINGS= {
  **tip.NODE_DISPLAY_NAME_MAPPINGS,
  **rp.NODE_DISPLAY_NAME_MAPPINGS,
  **si.NODE_DISPLAY_NAME_MAPPINGS
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]