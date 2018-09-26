import threading
import time
import sys

from pcp.thr.mailbox import Mailbox


class RingThread(threading.Thread):
    def __init__(self, number: int, input_mailbox: Mailbox, output_mailbox: Mailbox):
        super().__init__(name=f"Thread: {number}")
        self.input_mailbox = input_mailbox
        self.output_mailbox = output_mailbox

    def run(self):
        item = self.input_mailbox.pull()
        print(f"Thread {self.name} received item {item}")
        self.output_mailbox.push(f"Greetings from thread {self.name}")


def thread_ring(n: int):
    # Create a set of mailboxes
    mailboxes = [Mailbox() for _ in range(n)]

    mailbox_list = zip(mailboxes, mailboxes[1:])

    for idx, (input_mailbox, output_mailbox) in enumerate(mailbox_list, 1):
        RingThread(idx, input_mailbox, output_mailbox).start()

    main_output_mailbox = mailboxes[0]
    main_input_maibox = mailboxes[-1]

    main_output_mailbox.push(f"Greetings from Main thread")
    item = main_input_maibox.pull()

    print(f"Main thread received: {item}")
    print("Done.")


def main():
    assert len(sys.argv) >= 2
    n = int(sys.argv[1])
    print(f"N={n}")
    start_time = time.clock()
    thread_ring(n)
    end_time = time.clock()

    print("Time elapsed: {:.3f}s".format(end_time - start_time))


if __name__ == '__main__':
    main()
