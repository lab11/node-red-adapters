import sys
from time import sleep

test_string = "1435127671.660: X 6.15 X X X X X X X 4.78 !"

try:
	while(True):
		print test_string
		sys.stdout.flush()
		sleep(1)
except KeyboardInterrupt:
	sys.exit()