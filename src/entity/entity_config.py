from datetime import datetime
from dataclasses import dataclass

@dataclass
class TrainingPipelineConfig:
    timestamp = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")