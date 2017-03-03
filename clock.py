import time
x = time.time()
print(time.time(), time.clock())
time.sleep(.99)
print(time.time(), time.clock())
print(time.time() - x)
time.sleep(4.95)
print(time.time(), time.clock())
print(time.time() - x)
