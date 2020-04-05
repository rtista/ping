import os
import signal
import time

import multiprocessing
import subprocess
import threading

import inotify.adapters


BJOERN_CMD_START = tuple("python3 ping-api-ctl.py start".split())
BJOERN_CMD_RESTART = tuple("python3 ping-api-ctl.py restart".split())
CHANGE_EVENTS = ("IN_MODIFY", "IN_ATTRIB", "IN_DELETE")
WATCH_EXTENSIONS = (".py",)


def watch_tree(stop, path, event):
    path = os.path.abspath(path)

    for e in inotify.adapters.InotifyTree(path).event_gen():
        if stop.is_set():
            break

        if e is not None:
            _, attrs, path, filename = e

            if filename is None:
                continue

            if any(filename.endswith(ename) for ename in WATCH_EXTENSIONS):
                continue

            if any(ename in attrs for ename in CHANGE_EVENTS):
                event.set()


class Watcher(threading.Thread):
    def __init__(self, path):
        super(Watcher, self).__init__()
        self.bjoern = subprocess.Popen(BJOERN_CMD_START)
        self.stop_event_wtree = multiprocessing.Event()
        self.event_triggered_wtree = multiprocessing.Event()
        self.wtree = multiprocessing.Process(target=watch_tree,
                                             args=(self.stop_event_wtree, path, self.event_triggered_wtree))
        self.wtree.start()
        self.running = True

    def run(self):
        while self.running:
            if self.event_triggered_wtree.is_set():
                self.event_triggered_wtree.clear()
                self.restart_bjoern()
            time.sleep(5)

    def join(self, timeout=None):
        self.running = False
        self.stop_event_wtree.set()
        self.bjoern.terminate()
        self.wtree.join()
        self.bjoern.wait()
        super(Watcher, self).join(timeout=timeout)

    def restart_bjoern(self):
        # Isto devia de ter terminate e wait mas como a gestão está no ping-api deixo apenas o comando para o restart
        self.bjoern = subprocess.Popen(BJOERN_CMD_RESTART)


if __name__ == '__main__':
    watcher = Watcher("./")
    watcher.start()

    signal.signal(signal.SIGINT, lambda signal, frame: watcher.join())
    signal.pause()