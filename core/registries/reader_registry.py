from core.registries.component_registry import ComponentRegistry


READERS = ComponentRegistry("reader")
READERS.register("csv", "implementations.readers.csv_reader:CSVReader")
READERS.register("excel", "implementations.readers.excel_reader:ExcelReader")
