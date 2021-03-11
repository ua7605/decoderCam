import csv


class CsvReader:

    def __init__(self, file_paht):
        self.file_paht = file_paht

    def read_csv_file(self):
        # With this I can retrive from the last line the most right element
        ans1_cam_data = None
        with open(self.file_paht, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)

            for line in csv_reader:
                ans1_cam_data = line['asn1data']

            print(ans1_cam_data)

        return ans1_cam_data
