# Python Concurrency Playground

Small repository of python concurrency exercises

### Standard library concurrency toolbox

- threading
  - Thread class
  - Lock objects
  - RLock (reentrant lock)
  - Condition variable
  - Semaphore
  - Event objects -
  This is one of the simplest mechanisms for communication between threads: one thread signals an event and other threads wait for it.
  An event object manages an internal flag that can be set to true with the set() method and reset to false with the clear() method. The wait() method blocks until the flag is true.
  - Barrier objects
- multiprocessing
- asyncio


### Useful links:
- https://docs.python.org/3/library/concurrency.html