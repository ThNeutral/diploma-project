import torch
from dataclasses import dataclass

@dataclass
class StepResult:
  avg_loss: float
  confusion_matrix: torch.Tensor

  def accuracy(self) -> float:
    sum_, true_positive, _, _, _ = self._parts_from_cm()
    return (true_positive.sum() / sum_).item()

  def precision(self) -> float:
    _, true_positive, false_positive, _, _ = self._parts_from_cm()
    return (true_positive / (true_positive + false_positive).clamp(min=1e-8)).mean().item()

  def recall(self) -> float:
    _, true_positive, _, _, false_negative = self._parts_from_cm()
    return (true_positive / (true_positive + false_negative).clamp(min=1e-8)).mean().item()

  def f1(self) -> float:
    p, r = self.precision(), self.recall()
    return 2 * p * r / max(p + r, 1e-8)

  def _parts_from_cm(self):
    sum_ = self.confusion_matrix.sum()

    true_positive = self.confusion_matrix.diag()
    false_positive = self.confusion_matrix.sum(dim=0) - true_positive

    false_negative = self.confusion_matrix.sum(dim=1) - true_positive
    true_negative = sum_ - (true_positive + false_positive + false_negative)

    return (sum_, true_positive, false_positive, true_negative, false_negative)

  def __repr__(self) -> str:
    return (
			f"StepResult("
      f"loss={self.avg_loss:.4f}, "
      f"accuracy={self.accuracy():.4f}, "
      f"precision={self.precision():.4f}, "
      f"recall={self.recall():.4f}, "
      f"f1={self.f1():.4f})"
    )