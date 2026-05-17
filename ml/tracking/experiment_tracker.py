import torch
from torch.utils.tensorboard import SummaryWriter

from dto.training import StepResult
from dto.training import StepName

class ExperimentTracker:
	_inner: SummaryWriter

	_is_closed: bool

	def __init__(self, log_dir: str) -> None:
		self._is_closed = False

		self._inner = SummaryWriter(log_dir=log_dir)

	# TODO: add confusion matrix
	# TODO: add accuracy
	def track_step(
		self,
		step_result_dict: dict[StepName, StepResult],
		global_step: int
	):
		loss_dict = {name: result.avg_loss for name, result in step_result_dict.items()}
		self._inner.add_scalar(
			main_tag = "Loss",
			tag_scalar_dict = loss_dict,
			global_step=global_step
		) # type: ignore

	def flush(self):
		self._inner.flush()

	def close(self):
		if self._is_closed:
			raise Exception("ExperimentTracker was already closed")
		
		self._inner.close()
		self._is_closed = True