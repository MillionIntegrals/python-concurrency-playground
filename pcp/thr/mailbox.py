import threading


class Mailbox:
    def __init__(self):
        self.box = []
        self.cv = threading.Condition()

    def push(self, item):
        with self.cv:
            self.box.append(item)
            self.cv.notify()

    def pull(self):
        with self.cv:
            self.cv.wait_for(predicate=self._is_item_available)
        return self.box.pop()

    def _is_item_available(self):
        return bool(self.box)
