
class constants:
    dataset_type = {
            'csv': 'pandas.CSVDataSet',
            'json': 'pandas.JSONDataSet',
            'spark': 'spark.SparkDataSet',
            'xls': 'pandas.ExcelDataSet',
            'pickle': 'pickle.PickleDataSet',
            'parquet': 'pandas.ParquetDataSet',
        }
    
    data_catalog_path = "conf/base/catalog.yml"
