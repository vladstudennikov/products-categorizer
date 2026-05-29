import pandas as pd
from typing import Optional, Any
from core.abstractions.reader import BaseReader


class ExcelReader(BaseReader):
    def __init__(self, path: str):
        self.path = path
        self._has_read = False

    def read(self) -> Optional[pd.DataFrame]:
        """Reads the full Excel file. Returns None on subsequent calls."""
        if self._has_read:
            return None
        
        self._has_read = True
        return pd.read_excel(self.path)
