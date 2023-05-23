
class constants:
    dataset_type = {
            'csv': 'pandas.CSVDataSet',
            'json': 'pandas.JSONDataSet',
            'xls': 'pandas.ExcelDataSet',
            'pickle': 'pickle.PickleDataSet',
            'parquet': 'pandas.ParquetDataSet',
            'memory': 'MemoryDataSet',
        }
    
    data_catalog_path = "conf/base/catalog.yml"
