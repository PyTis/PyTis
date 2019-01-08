#!/usr/bin/env python
# https://stackoverflow.com/questions/2148888/python-trap-all-signals
import os
import sys
import time
import signal

SIGNALS_TO_NAMES_DICT = dict((getattr(signal, n), n) \
	for n in dir(signal) if n.startswith('SIG') and '_' not in n )


def receive_signal(signum, stack):
	if signum in [1,2,3,15]:
		print 'Caught signal %s (%s), exiting.' % (SIGNALS_TO_NAMES_DICT[signum], str(signum))
		main()
		sys.exit()
	else:
		print 'Caught signal %s (%s), ignoring.' % (SIGNALS_TO_NAMES_DICT[signum], str(signum))

def main():
	uncatchable = ['SIG_DFL','SIGSTOP','SIGKILL']
	for i in [x for x in dir(signal) if x.startswith("SIG")]:
		if not i in uncatchable:
			signum = getattr(signal,i)
			signal.signal(signum,receive_signal)
	print('My PID: %s' % os.getpid())
	while True:
		time.sleep(1)

if __name__ == '__main__':
	sys.exit(main())


