from subprocess import Popen, PIPE

POLL_SEC = 1 #send updates to MQTT topic every second

#using anchors A2, A6, and A10
A2_MIN = 4.9
A2_MAX = 7.4
A6_MIN = 0.2
A6_MAX = 1.5
A10_MIN = 3.0
A10_MAX = 5.5

# run the PolyPoint hack program as a subprocess
p = Popen(['python', 'fake-pphack.py'],
        stdin = PIPE, stdout = PIPE, stderr = PIPE, shell = False)

while True:
    output = p.stdout.readline()
    fields = output.split(" ")
    if len(fields) == 12: # valid distance msg, not error
    	try:
		    a2_dist = float(fields[2])
		    a6_dist = float(fields[6])
		    a10_dist = float(fields[10])
		    distances = (a2_dist, a6_dist, a10_dist)
		    is_at_desk = True
		    if (a2_dist < A2_MIN or a2_dist > A2_MAX) or (a6_dist < A6_MIN or a6_dist > A6_MAX) or (a10_dist < A10_MIN or a10_dist > A10_MAX):
		    	is_at_desk = False
		    else:
		    	is_at_desk = True
		    print(is_at_desk)
		except ValueError: # at least one of the distances isn't known
			pass
