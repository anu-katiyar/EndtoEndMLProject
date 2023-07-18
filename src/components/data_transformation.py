import sys
import numpy as np
import pandas as pd

from src.logger import logging
from src.exception import CustomException
from dataclasses import dataclass

@dataclass
class DataTransformationConfig :
