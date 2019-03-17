import sys
import random
import math

class Rand48(object):
    def __init__(self, seed):
        self.n = seed
    def seed(self, seed):
        self.n = seed
    def srand(self, seed):
        self.n = (seed << 16) + 0x330e
    def next(self):
        self.n = (25214903917 * self.n + 11) & (2**48 - 1)
        return self.n
    def drand(self):
        return self.next() / 2**48
    def lrand(self):
        return self.next() >> 17
    def mrand(self):
        n = self.next() >> 16
        if n & (1 << 31):
            n -= 1 << 32
        return n   

# Seed RNG
r = Rand48(0)
r.srand(int(sys.argv[1]))

# Simulate Processes
num_processes = int(sys.argv[4])
proc = [chr(ord('A') + x) for x in range(num_processes)]

init_time = {}
num_bursts = {}
cpu_bursts = {}
io_bursts = {}

def gen_exp():
	exp_distr = math.inf
	while(exp_distr > int(sys.argv[3])):
		unif_distr = r.drand()
		exp_distr = -1 * (math.log(unif_distr)) / float(sys.argv[2])
	return exp_distr

# initialize values
for i in range(num_processes):
	init_time[proc[i]] = math.floor(gen_exp())

	num_bursts[proc[i]] = int(r.drand() * 100) + 1
	cpu_bursts[proc[i]] = []
	io_bursts[proc[i]] = []
	for j in range(num_bursts[proc[i]]):
		cpu_bursts[proc[i]].append(math.ceil(gen_exp()))
		if (j != num_bursts[proc[i]]-1):
			io_bursts[proc[i]].append(math.ceil(gen_exp()))
def print_queue(queue):
	if (len(queue) == 0):
		return " <empty>"
	string = ""
	for process in queue:
		string = string + " " + process
	return string
# for i in range(len(proc)):
# 	process = proc[i]
# 	print("Process %s [NEW] (arrival time %d ms) %d CPU bursts" % (process, init_time[process], num_bursts[process]))
# 	for j in range(num_bursts[process] - 1):
# 		print("--> CPU burst %d ms --> I/O burst %d ms" % (cpu_bursts[process][j], io_bursts[process][j]))
# 	print("--> CPU burst %d ms" %(cpu_bursts[process][num_bursts[process]-1]))
def FCFS():
	queue = []
	for i in range(len(proc)):
		process = proc[i]
		print("Process %s [NEW] (arrival time %d ms) %d CPU bursts" % (process, init_time[process], num_bursts[process]))
	# 	for j in range(num_bursts[process] - 1):
	# 		print("--> CPU burst %d ms --> I/O burst %d ms" % (cpu_bursts[process][j], io_bursts[process][j]))
	# 	print("--> CPU burst %d ms" %(cpu_bursts[process][num_bursts[process]-1]))
	print("time 0ms: Simulator started for FCFS [Q%s]" % print_queue(queue))
	fin_processes = []
	cpu_burst_tracker = {}
	CPU_blocked_tracker = -1
	IO_blocked_tracker = {}
	CPU_used = False
	time = 0
	context_switch_time = -1
	context_switch_remove = -1
	while (len(fin_processes) < num_processes):
		# print(time)
		# check arrival
		for process in init_time:
			if time == init_time[process]:
				queue.append(process)
				cpu_burst_tracker[process] = 0
				print("time %dms: Process %s arrived; added to ready queue [Q%s]" %(time, process, print_queue(queue)))
				if (not CPU_used):
					head = queue[0]
					queue = queue[1:]
					context_switch_time = time + int(sys.argv[5])/2		
		# add process from queue
		if (time == context_switch_time):
			print("time %dms: Process %s started using the CPU for %dms burst [Q%s]" %(time, head, cpu_bursts[head][cpu_burst_tracker[head]], print_queue(queue)))
			CPU_blocked_tracker = time + cpu_bursts[head][cpu_burst_tracker[head]]
			cpu_burst_tracker[head] += 1
			CPU_used = True
		if (CPU_blocked_tracker == time):
			if (num_bursts[head] - cpu_burst_tracker[head] > 0):
				print("time %dms: Process %s completed a CPU burst; %d burst%s to go [Q%s]" % (time, head, num_bursts[head] - cpu_burst_tracker[head], "s" if (num_bursts[head] - cpu_burst_tracker[head] > 1) else "", print_queue(queue)))
				print("time %dms: Process %s switching out of CPU; will block on I/O until time %dms [Q%s]" % (time, head, time + io_bursts[head][cpu_burst_tracker[head]-1] + 2, print_queue(queue)))
				IO_blocked_tracker[head] = time + io_bursts[head][cpu_burst_tracker[head]-1] + 2
			else:
				print("time %dms: Process %s terminated [Q%s]" %(time, head, print_queue(queue)))
				fin_processes.append(head)
			context_switch_remove = time + int(sys.argv[5]) / 2
		for process in sorted(IO_blocked_tracker):
			if time == IO_blocked_tracker[process]:
				queue.append(process)
				print("time %dms: Process %s completed I/O; added to ready queue [Q%s]" %(time, process, print_queue(queue)))
				if (not CPU_used):
					head = queue[0]
					queue = queue[1:]
					context_switch_time = time + int(sys.argv[5])/2
					CPU_used = True
		if (time == context_switch_remove):
			if (len(queue) != 0):
				head = queue[0]
				queue = queue[1:]
				context_switch_time = time + int(sys.argv[5])/2
				CPU_used = True
			else:
				CPU_used = False
		time += 1
	print("time %dms: Simulator ended for FCFS [Q%s]" %(time+1, print_queue(queue)))
FCFS()

