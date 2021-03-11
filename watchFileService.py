import sys, os.path, time, logging
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

from Decoder import CamDecoder


class MyEventHandler(PatternMatchingEventHandler):

    decoder = CamDecoder()

    def on_modified(self, event):
        super(MyEventHandler, self).on_modified(event)
        logging.info("File %s was just modified" % event.src_path)
        self.decoder.encode()

def main(file_path=None):
    logging.basicConfig(level=logging.INFO,
        format='%(asctime)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')
    watched_dir = os.path.split(file_path)[0]
    print ('watched_dir = {watched_dir}'.format(watched_dir=watched_dir))
    patterns = [file_path]
    print ('patterns = {patterns}'.format(patterns=', '.join(patterns)))
    event_handler = MyEventHandler(patterns=patterns)
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

    main(file_path='/Users/vincentcharpentier/School/Master/Testfoldere/Testbestand.txt')
