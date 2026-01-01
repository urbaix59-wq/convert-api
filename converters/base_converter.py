from pathlib import Path
from abc import ABC, abstractmethod


class BaseConverter(ABC):
    @abstractmethod
    def convert(self, input_path: Path, output_path: Path):
        pass
