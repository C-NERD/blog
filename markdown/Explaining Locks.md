# Explaining Locks 🔒

Imagine you have the global variable **count** that is being accessed by multiple threads in parallel. This variable is dangerous because at any point in time 2 or more threads may try to access the variable at once which may lead to memory corruption.

```nim
import std / [threadpool]
from std / strformat import fmt
from std / math import pow

var count : float64 = 2.0 ## the global variable
proc powAndPrint(threadid : int) : FlowVarBase =
    ## perform some pow opt and print to stdout

    for pos in 0..100:

        count = pow(count, 2.0)
        echo fmt"ThreadId :: {threadid}, Count :: {count}"

        count = 2.0

var threads : array[2, FlowVarBase] 
threads[0] = spawn powAndPrint(1)
threads[1] = spawn powAndPrint(2)

discard blockUntilAny(threads) ## wait for both threads
```

In order to avoid multiple threads from reading the same global variable **count** at once you can employ the use of locks. A lock has 2 states **Acquire** and **Release**. If a lock is set to guard a variable from access, a thread must acquire the lock before accessing the variable. Once the lock has been acquired it cannot be acquired by another thread unless it is released by the thread that acquired it. Which means that once a lock guarding a variable is acquired by a thread, other threads cannot access the variable unless the lock is released.

```nim
import std / [threadpool, locks]
from std / strformat import fmt
from std / math import pow

var 
    countLock : Lock
    count : float64 = 2.0 ## the global variable

initLock(countLock)
proc powAndPrint(threadid : int) : FlowVarBase =
    ## perform some pow opt and print to stdout

    for pos in 0..100:

        acquire(countLock)
        count = pow(count, 2.0)
        echo fmt"ThreadId :: {threadid}, Count :: {count}"

        count = 2.0
        release(countLock)

var threads : array[2, FlowVarBase] 
threads[0] = spawn powAndPrint(1)
threads[1] = spawn powAndPrint(2)

discard blockUntilAny(threads) ## wait for both threads
deinitLock(countLock)
```

This way we have ensured that only 1 thread can access the global variable **count** at a time.
