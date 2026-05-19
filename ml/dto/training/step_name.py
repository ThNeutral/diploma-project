from enum import Enum

class StepName(str, Enum):
	Train = 'train'
	Test = 'test'
	Validation = 'val'