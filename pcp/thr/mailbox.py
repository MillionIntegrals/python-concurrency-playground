import threading


class Mailbox:
    def __init__(self):
        self._box = []
        self._cv = threading.Condition()

    def push(self, item):
        with self._cv:
            self._box.append(item)
            self._cv.notify()

    def pull(self):
        with self._cv:
            self._cv.wait_for(predicate=self._is_item_available)
            return self._box.pop()

    def _is_item_available(self):
        return bool(self._box)
