import sys, os, time, atexit, signal

class Daemon:
    def __init__(self, pidfile):
        self.pidfile = pidfile # pid file to control process

    def daemonize(self):
        try:
            pid = os.fork() #fork a child process
            if pid > 0:
                sys.exit(0)  #exit parent process
        except OSError as err:
            sys.stderr.write('fork #1 failed: {0}\n'.format(err))
            sys.exit(1)
        os.chdir('/') #change working dir for child process
        os.setsid()  #create new session from parent session
        os.umask(0)  # umask will disable the wx for file created by default 
        try:
            pid = os.fork() # second fork, to disable process open a terminal by mistake
            if pid > 0:
                sys.exit(0)  # child process exist

        except OSError as err:
            sys.stderr.write(f'fork #2 failed: {err}\n')
            sys.exit(1)    
        sys.stdout.flush()
        sys.stderr.flush()
        si = open(os.devnull, 'r')
        so = open(os.devnull, 'a+')
        se = open(os.devnull, 'a+')

        #dup2函数原子化关闭和复制文件描述符
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        atexit.register(self.delpid)
        # chck if process exists
        pid = str(os.getpid())
        # write pidfile
        with open(self.pidfile, 'w+') as f:
            f.write(pid + '\n')

    def delpid(self): # delete pid
        os.remove(self.pidfile)

    def start(self):
        '''
        start deamon
        '''
        # check by pid in file, if deamon is runing
        try:
            with open(self.pidfile, 'r') as pf:
                pid = int(pf.read().strip())
        except IOError:
            pid = None

        if pid: # pid exists, Daemon is running
            message = "pidfile {0} already exist. " + \
                        "Daemon already running?\n"
            sys.stderr.write(message.format(self.pidfile))
            sys.exit(1)

        # Daemon not running then run it
        self.daemonize()
        self.run()

    def stop(self):
        '''
        turn off daemon
        '''
        # get pid from pid file
        try:
            with open(self.pidfile, 'r') as pf:
                pid = int(pf.read().strip())
        except IOError:
            pid = None

        if not pid:  # no daemon running
            message = "pidfile {0} does not exist. " + \
                      "Daemon not running?\n"
            sys.stderr.write(message.format(self.pidfile))
            return  # not an error in a restart

        # kill process by os kill
        try:
            while 1:
                os.kill(pid, signal.SIGTERM) # signal
                time.sleep(0.1)
        except OSError as err:
            e = str(err.args)
            if e.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                print(str(err.args))
                sys.exit(1)
    def restart(self):
        self.stop() # turn off 
        self.start() # start daemon


    def run(self):
        raise NotImplementedError("implement run function please")