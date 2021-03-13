import csv


class CsvReader:

    def __init__(self, file_paht):
        self.file_paht = file_paht

    def read_csv_file(self):
        # With this I can retrive from the last line the most right element
        ans1_cam_data = None

        with open(self.file_paht, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            teller =0
            received_message = False
            for line in csv_reader:

                ans1_cam_data = line['asn1data']
                if line[' log_action'] == 'RECEIVED':
                    print("It is a RECEIVED message type")
                    received_message = True
                else:
                    print("It is a sent message")
                    received_message = False

            print(ans1_cam_data)

        return ans1_cam_data, received_message

    def optimized_csv_read_file(self):
        # With this I can retrive from the last line the most right element
        ans1_cam_data = None

        with open(self.file_paht, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            received_message = False
            teller = 0
            for line in reversed(list(csv_reader)):
                ans1_cam_data = line['asn1data']
                teller = teller+1
                if line[' log_action'] == 'RECEIVED':
                    print("It is a RECEIVED message type")
                    received_message = True
                    break
                else:
                    received_message = False
                    break

        return ans1_cam_data, received_message
