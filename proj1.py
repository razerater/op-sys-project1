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
	while(exp_distr > 3000):
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

def FCFS():
	queue = []
	for i in range(len(proc)):
		process = proc[i]
		print("Process %s [NEW] (arrival time %d ms) %d CPU bursts" % (process, init_time[process], num_bursts[process]))
	# 	for j in range(num_bursts[process] - 1):
	# 		print("--> CPU burst %d ms --> I/O burst %d ms" % (cpu_bursts[process][j], io_bursts[process][j]))
	# 	print("--> CPU burst %d ms" %(cpu_bursts[process][num_bursts[process]-1]))
	print("time 0ms: Simulator arrived for SJF [Q%s]" % print_queue(queue))
	fin_processes = []
	used = False
	burst_done = 0
	time = 0
	while (len(fin_processes) != num_processes):
		# check arrival
		for process in init_time:
			if time == init_time[process]:
				queue.append(process)
				print("time %dms: Process %s arrived; added to ready queue [Q%s]" %(time, process, print_queue(queue)))



		time += 1
		if (time == 2000):
			 break
FCFS()

