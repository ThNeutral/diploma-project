import torch
import matplotlib.pyplot as plt
import numpy as np
from torch.utils.tensorboard import SummaryWriter

from dto.training import StepResult
from dto.training import StepName

class ExperimentTracker:
  _inner: SummaryWriter
  _is_closed: bool

  def __init__(self, log_dir: str) -> None:
    self._is_closed = False
    self._inner = SummaryWriter(log_dir=log_dir)

  def track_epoch(
    self,
    step_result_dict: dict[StepName, StepResult],
    global_step: int
  ):
    loss_dict = {name: result.avg_loss for name, result in step_result_dict.items()}
    accuracy_dict = {name: result.accuracy() for name, result in step_result_dict.items()}
    precision_dict = {name: result.precision() for name, result in step_result_dict.items()}
    recall_dict = {name: result.recall() for name, result in step_result_dict.items()}
    f1_dict = {name: result.f1() for name, result in step_result_dict.items()}

    self._inner.add_scalars("Loss", loss_dict, global_step)
    self._inner.add_scalars("Accuracy", accuracy_dict, global_step)
    self._inner.add_scalars("Precision", precision_dict, global_step)
    self._inner.add_scalars("Recall", recall_dict, global_step)
    self._inner.add_scalars("F1", f1_dict, global_step)

    for name, result in step_result_dict.items():
      fig = self._make_cm_figure(result.confusion_matrix)
      self._inner.add_figure(f"ConfusionMatrix/{name}", fig, global_step)
      plt.close(fig)

  def _make_cm_figure(self, cm: torch.Tensor) -> plt.Figure:
    matrix = cm.cpu().numpy()
    normalized = matrix / matrix.sum(axis=1, keepdims=True).clip(min=1e-8)

    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(normalized, interpolation="nearest", cmap="Blues")
    fig.colorbar(im, ax=ax)

    thresh = normalized.max() / 2
    for i, j in np.ndindex(matrix.shape):
      ax.text(j, i, str(matrix[i, j]),
				ha="center", va="center",
 				color="white" if normalized[i, j] > thresh else "black")

    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    fig.tight_layout()
    return fig

  def flush(self):
    self._inner.flush()

  def close(self):
    if self._is_closed:
      raise Exception("ExperimentTracker was already closed")

    self._inner.close()
    self._is_closed = True