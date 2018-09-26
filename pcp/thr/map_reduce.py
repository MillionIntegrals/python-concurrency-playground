import collections
import sys
import threading
import time

from pcp.thr.mailbox import Mailbox


class MRData:
    def __init__(self, num_threads: int, notification_mailbox: Mailbox):
        self.num_threads = num_threads
        self.barrier = threading.Barrier(parties=num_threads)

        self.shuffle_lock = threading.Lock()
        self.shuffle_data = collections.defaultdict(list)

        self.reduce_lock = threading.Lock()
        self.reduce_data = []

        self.notification_mailbox = notification_mailbox

    def push_map_output(self, key, value):
        with self.shuffle_lock:
            self.shuffle_data[key].append(value)

    def pull_reduce_input(self, thread_no: int):
        with self.reduce_lock:
            return self.shuffle_data[thread_no]

    def push_reduce_output(self, value):
        with self.reduce_lock:
            self.reduce_data.append(value)

            if len(self.reduce_data) == self.num_threads:
                self.notification_mailbox.push(self.reduce_data)

    def wait_for_reduce(self):
        self.barrier.wait()


class MRThread(threading.Thread):
    def __init__(self, number: int, num_threads: int, start_map: int, stop_map: int, mr_data: MRData):
        super().__init__(name=f"Thread: {number}")

        self.mr_data = mr_data

        self.number = number
        self.num_threads = num_threads
        self.start_map = start_map
        self.stop_map = stop_map

    def run(self):
        for i in range(self.start_map, self.stop_map):
            self.mr_data.push_map_output(i % self.num_threads, i)

        self.mr_data.wait_for_reduce()

        data = self.mr_data.pull_reduce_input(self.number)

        self.mr_data.push_reduce_output(sum(data))


def map_reduce_job(maxnum: int, threads: int):
    low = 0
    high = maxnum // threads

    mailbox = Mailbox()
    mr_data = MRData(threads, mailbox)

    for i in range(threads):
        MRThread(i, threads, low, high, mr_data).start()

        low = high
        high = min(high + maxnum // threads + 1, maxnum)

    result = mailbox.pull()
    print(f"Sum of numbers from 0 to {maxnum} is {sum(result)}")


def main():
    assert len(sys.argv) >= 3
    m = int(sys.argv[1])
    n = int(sys.argv[2])

    print(f"M={m}")
    print(f"N={n}")

    start_time = time.clock()
    map_reduce_job(m, n)
    end_time = time.clock()

    print("Time elapsed: {:.3f}s".format(end_time - start_time))


if __name__ == '__main__':
    main()
