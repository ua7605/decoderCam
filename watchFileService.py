import sys, os.path, time, logging
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

from FileConfigService import FileConfig
from Decoder import CamDecoder


class MyEventHandler(PatternMatchingEventHandler):
    config = FileConfig("f","d")
    print(config.get_output_file_json())
    print()

    def __init__(self, patterns, file_path_to_csv_file, output_file_json ):
        super(MyEventHandler, self).__init__(patterns)
        self.file_path_to_csv_file = file_path_to_csv_file
        self.output_file_json = output_file_json
        self.cam_decoder = CamDecoder(file_path=self.file_path_to_csv_file, output_file_path=self.output_file_json)

    def on_modified(self, event):
        super(MyEventHandler, self).on_modified(event)
        logging.info("File %s was just modified" % event.src_path)
        self.cam_decoder.encode()


def main(file_path=None, file_path_json=None):
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    watched_dir = os.path.split(file_path)[0]
    print('watched_dir = {watched_dir}'.format(watched_dir=watched_dir))
    patterns = [file_path]
    print('patterns = {patterns}'.format(patterns=', '.join(patterns)))
    event_handler = MyEventHandler(patterns=patterns,file_path_to_csv_file=file_path,output_file_json=file_path_json)
    observer = Observer()
    observer.schedule(event_handler, watched_dir, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main(file_path='/Users/vincentcharpentier/Downloads/username.csv', file_path_json='/Users/vincentcharpentier/School/Master/MAP/Decoder/CAMv1.json')

