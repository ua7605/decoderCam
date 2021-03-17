import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO,
#                         format='%(asctime)s - %(message)s',
#                         datefmt='%Y-%m-%d %H:%M:%S')
#     #path = sys.argv[1] if len(sys.argv) > 1 else '.'
#     path = '/Users/vincentcharpentier/School/Master/MAP/DirToWatch'
#     event_handler = LoggingEventHandler()
#     observer = Observer()
#     observer.schedule(event_handler, path, recursive=True)
#     observer.start()
#     try:
#         while True:
#             time.sleep(1)
#     finally:
#         observer.stop()
#         observer.join()

import sys, os.path, time, logging
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


class MyEventHandler(PatternMatchingEventHandler):
    def on_moved(self, event):
        super(MyEventHandler, self).on_moved(event)
        logging.info("File %s was just moved" % event.src_path)

    def on_created(self, event):
        super(MyEventHandler, self).on_created(event)
        logging.info("File %s was just created" % event.src_path)

    def on_deleted(self, event):
        super(MyEventHandler, self).on_deleted(event)
        logging.info("File %s was just deleted" % event.src_path)

    def on_modified(self, event):
        super(MyEventHandler, self).on_modified(event)
        logging.info("File %s was just modified" % event.src_path)

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

    main(file_path='/Users/vincentcharpentier/School/Master/MAP/DirToWatch')
