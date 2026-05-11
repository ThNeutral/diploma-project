import torch
from typing import Callable

Transform = Callable[[torch.Tensor], torch.Tensor]