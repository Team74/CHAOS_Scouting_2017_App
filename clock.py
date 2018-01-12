import time
x = time.time()
print(time.time(), time.clock())
time.sleep(.999)
print(time.time(), time.clock())
print(time.time() - x)
time.sleep(4.96)
print(time.time(), time.clock())
print(time.time() - x)

'''
    def signal_handler(self, signal, frame):
        debug('this is working out')
        self.running = 0
        sys.exit(0)

    def Hi(self):
        self.yes = time.time()

    def runtime(self):
        while self.running:
            print('yes it is working')
            if not self.timeLbl == None:
                if self.yes == 'start':
                    pass
                else:
                    self.can=time.time() - self.yes
                    self.timeLbl.text = str(self.can)
            time.sleep(1)'''
'''
    def __init__(self, **kwargs):
        signal.signal(signal.SIGHUP, self.signal_handler)
        signal.signal(signal.SIGINT, self.signal_handler) #IMPORTANT save
        signal.signal(signal.SIGQUIT, self.signal_handler)
        signal.signal(signal.SIGILL, self.signal_handler)
        signal.signal(signal.SIGTRAP, self.signal_handler)
        signal.signal(signal.SIGIOT, self.signal_handler)
        signal.signal(signal.SIGBUS, self.signal_handler)
        signal.signal(signal.SIGFPE, self.signal_handler)
        #signal.signal(signal.SIGKILL, self.signal_handler)
        signal.signal(signal.SIGUSR1, self.signal_handler)
        signal.signal(signal.SIGSEGV, self.signal_handler)
        signal.signal(signal.SIGUSR2, self.signal_handler)
        signal.signal(signal.SIGPIPE, self.signal_handler)
        signal.signal(signal.SIGALRM, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        #signal.signal(signal.SIGSTKFLT, self.signal_handler)
        #signal.signal(signal.SIGCHLD, self.signal_handler) #killing it before it starts
        signal.signal(signal.SIGCONT, self.signal_handler)
        #signal.signal(signal.SIGSTOP, self.signal_handler)
        signal.signal(signal.SIGTSTP, self.signal_handler)
        signal.signal(signal.SIGTTIN, self.signal_handler)
        signal.signal(signal.SIGTTOU, self.signal_handler)
        signal.signal(signal.SIGURG, self.signal_handler)
        signal.signal(signal.SIGXCPU, self.signal_handler)
        signal.signal(signal.SIGXFSZ, self.signal_handler)
        signal.signal(signal.SIGVTALRM, self.signal_handler)
        signal.signal(signal.SIGPROF, self.signal_handler)
        signal.signal(signal.SIGWINCH, self.signal_handler)
        signal.signal(signal.SIGIO, self.signal_handler)
        signal.signal(signal.SIGPWR, self.signal_handler)

        super(Screen, self).__init__(**kwargs)
        self.timeth = threading.Thread(target=self.runtime)
        self.daemon = True
        self.timeth.start()
        self.lastLowVal = 0
        self.choose()'''
