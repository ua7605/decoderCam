class FileConfig:

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls,'instance'):
            cls.instance = super(FileConfig, cls).__new__(cls)
        return cls.instance

    def __init__(self, file_path_to_csv_file, output_file_json):
        self.file_path_to_csv_file = file_path_to_csv_file
        self.output_file_json = output_file_json


    def get_file_path_to_csv_file(self):
        return self.file_path_to_csv_file

    def get_output_file_json(self):
        return self.output_file_json