import pandas as pd
from typing import Optional, Any
from core.abstractions.reader import BaseReader


class CSVReader(BaseReader):
    def __init__(self, path: str, **kwargs):
        self.path = path
        self.kwargs = kwargs
        self._has_read = False

    def read(self) -> Optional[pd.DataFrame]:
        """Reads the full CSV file. Returns None on subsequent calls."""
        if self._has_read:
            return None
        
        self._has_read = True
        return pd.read_csv(self.path, **self.kwargs)
