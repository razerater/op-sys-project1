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

def gen_exp():
	exp_distr = math.inf
	while(exp_distr > int(sys.argv[3])):
		unif_distr = r.drand()
		exp_distr = -1 * (math.log(unif_distr)) / float(sys.argv[2])
	return exp_distr
def init_vals(seed, proc):
	# Seed RNG
	r.srand(seed)

	proc+=[chr(ord('A') + x) for x in range(num_processes)]

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
	print("time 0ms: Simulator started for FCFS [Q%s]" % print_queue(queue))
	cpu_burst_tracker = {}
	CPU_blocked_tracker = -1
	IO_blocked_tracker = {}
	CPU_free = True
	time = 0
	context_add = -1
	context_remove = -1
	turnaround_tracker = {}
	tot_turnaround = 0
	tot_wait = 0
	while (1):
		# print(time)
		# add process from queue
		if (time == context_add):
			print("time %dms: Process %s started using the CPU for %dms burst [Q%s]" %(time, head, cpu_bursts[head][cpu_burst_tracker[head]], print_queue(queue)))
			CPU_blocked_tracker = time + cpu_bursts[head][cpu_burst_tracker[head]]
			cpu_burst_tracker[head] += 1
			CPU_free = False
		# check arrival
		for process in init_time:
			if time == init_time[process]:
				queue.append(process)
				cpu_burst_tracker[process] = 0
				print("time %dms: Process %s arrived; added to ready queue [Q%s]" %(time, process, print_queue(queue)))
				turnaround_tracker[process] = time
				if (CPU_free):
					head = queue[0]
					queue = queue[1:]
					context_add = time + int(sys.argv[5])/2
					tot_wait += time - turnaround_tracker[head]
		if (CPU_blocked_tracker == time):
			if (num_bursts[head] - cpu_burst_tracker[head] > 0):
				print("time %dms: Process %s completed a CPU burst; %d burst%s to go [Q%s]" % (time, head, num_bursts[head] - cpu_burst_tracker[head], "s" if (num_bursts[head] - cpu_burst_tracker[head] > 1) else "", print_queue(queue)))
				print("time %dms: Process %s switching out of CPU; will block on I/O until time %dms [Q%s]" % (time, head, time + io_bursts[head][cpu_burst_tracker[head]-1] + 2, print_queue(queue)))
				IO_blocked_tracker[head] = time + io_bursts[head][cpu_burst_tracker[head]-1] + 2
			else:
				print("time %dms: Process %s terminated [Q%s]" %(time, head, print_queue(queue)))
				proc.remove(head)
				if (len(proc) == 0):
					tot_turnaround += (time - turnaround_tracker[head] + int(sys.argv[5]) / 2)
					break
			context_remove = time + int(sys.argv[5]) / 2
		for process in sorted(IO_blocked_tracker):
			if time == IO_blocked_tracker[process]:
				queue.append(process)
				print("time %dms: Process %s completed I/O; added to ready queue [Q%s]" %(time, process, print_queue(queue)))
				turnaround_tracker[process] = time
				if (CPU_free):
					head = queue[0]
					queue = queue[1:]
					context_add = time + int(sys.argv[5])/2
					tot_wait += time - turnaround_tracker[head]
					CPU_free = False
					# print(turnaround_tracker)
		if (time == context_remove):
			tot_turnaround += time - turnaround_tracker[head]
			if (len(queue) != 0):
				head = queue[0]
				queue = queue[1:]
				context_add = time + int(sys.argv[5])/2
				tot_wait += time - turnaround_tracker[head]
				CPU_free = False
			else:
				CPU_free = True
		time += 1
	print("time %dms: Simulator ended for FCFS [Q%s]" %(time+int(sys.argv[5])/2, print_queue(queue)))
	return (tot_wait, tot_turnaround)

def SJF():
	queue = []
	for i in range(len(proc)):
		process = proc[i]
		print("Process %s [NEW] (arrival time %d ms) %d CPU bursts" % (process, init_time[process], num_bursts[process]))
	# 	for j in range(num_bursts[process] - 1):
	# 		print("--> CPU burst %d ms --> I/O burst %d ms" % (cpu_bursts[process][j], io_bursts[process][j]))
	# 	print("--> CPU burst %d ms" %(cpu_bursts[process][num_bursts[process]-1]))
	print("time 0ms: Simulator started for SJF [Q%s]" % print_queue(queue))
	cpu_burst_tracker = {}
	CPU_blocked_tracker = -1
	IO_blocked_tracker = {}
	turnaround_tracker = {}
	tau_tracker = {}
	CPU_free = True
	time = 0
	tot_turnaround = 0
	tot_wait = 0
	context_add = -1
	context_remove = -1
	while (1):
		# print(time)
		# add process from queue
		if (time == context_add):
			print("time %dms: Process %s started using the CPU for %dms burst [Q%s]" %(time, head, cpu_bursts[head][cpu_burst_tracker[head]], print_queue(queue)))
			CPU_blocked_tracker = time + cpu_bursts[head][cpu_burst_tracker[head]]
			cpu_burst_tracker[head] += 1
			CPU_free = False
		# check arrival
		for process in init_time:
			if time == init_time[process]:
				queue.append(process)
				cpu_burst_tracker[process] = 0
				tau_tracker[process] = int(1 / float(sys.argv[2]))
				queue = sorted(queue)
				queue = sorted(queue, key = lambda x: tau_tracker[x])
				print("time %dms: Process %s (tau %dms) arrived; added to ready queue [Q%s]" %(time, process, tau_tracker[process], print_queue(queue)))
				turnaround_tracker[process] = time
				if (CPU_free):
					head = queue[0]
					queue = queue[1:]
					context_add = time + int(sys.argv[5])/2	
					tot_wait += time - turnaround_tracker[head]	
		
		if (CPU_blocked_tracker == time):
			if (num_bursts[head] - cpu_burst_tracker[head] > 0):
				print("time %dms: Process %s completed a CPU burst; %d burst%s to go [Q%s]" % (time, head, num_bursts[head] - cpu_burst_tracker[head], "s" if (num_bursts[head] - cpu_burst_tracker[head] > 1) else "", print_queue(queue)))
				tau_tracker[head] = math.ceil(float(sys.argv[6])*cpu_bursts[head][cpu_burst_tracker[head] - 1]+(1 - float(sys.argv[6])) * tau_tracker[head])
				print("time %dms: Recalculated tau = %dms for process %s [Q%s]" % (time, tau_tracker[head], head, print_queue(queue)))
				print("time %dms: Process %s switching out of CPU; will block on I/O until time %dms [Q%s]" % (time, head, time + io_bursts[head][cpu_burst_tracker[head]-1] + 2, print_queue(queue)))
				IO_blocked_tracker[head] = time + io_bursts[head][cpu_burst_tracker[head]-1] + 2
			else:
				print("time %dms: Process %s terminated [Q%s]" %(time, head, print_queue(queue)))
				proc.remove(head)
				if (len(proc) == 0):
					tot_turnaround += (time - turnaround_tracker[head] + int(sys.argv[5]) / 2)
					break
			context_remove = time + int(sys.argv[5]) / 2
		for process in sorted(IO_blocked_tracker):
			if time == IO_blocked_tracker[process]:
				queue.append(process)
				queue = sorted(queue)
				queue = sorted(queue, key = lambda x: tau_tracker[x])
				print("time %dms: Process %s (tau %dms) completed I/O; added to ready queue [Q%s]" %(time, process, tau_tracker[process], 	print_queue(queue)))
				turnaround_tracker[process] = time
				if (CPU_free):
					head = queue[0]
					queue = queue[1:]
					context_add = time + int(sys.argv[5])/2
					tot_wait += time - turnaround_tracker[head]
					CPU_free = False
		if (time == context_remove):
			tot_turnaround += time - turnaround_tracker[head]
			if (len(queue) != 0):
				head = queue[0]
				queue = queue[1:]
				context_add = time + int(sys.argv[5])/2
				CPU_free = False
				tot_wait += time - turnaround_tracker[head]
			else:
				CPU_free = True
		time += 1
	print("time %dms: Simulator ended for SJF [Q%s]" %(time+1, print_queue(queue)))
	return (tot_wait, tot_turnaround)
	

def avg_cpu_burst():
	tot = 0
	count = 0
	for lt in cpu_bursts:
		for burst in cpu_bursts[lt]:
			count += 1
			tot += burst
	return float(tot)/count

r = Rand48(0)
num_processes = int(sys.argv[4])
proc = []
init_time = {}
num_bursts = {}
cpu_bursts = {}
io_bursts = {}

init_vals(int(sys.argv[1]), proc)
x = FCFS()

init_vals(int(sys.argv[1]), proc)
y = SJF()

print ("Algorithm FCFS")
print ("-- average CPU burst time: %.3f ms" % avg_cpu_burst())
print ("-- average wait time: %.3f ms" % (float(x[0])/sum(num_bursts.values())))
print ("-- average turnaround time: %.3f ms" % (float(x[1])/sum(num_bursts.values())))
print ("-- total number of context switches: %d" % sum(num_bursts.values()))
print ("-- total number of preemptions: 0")

print ("Algorithm SJF")
print ("-- average CPU burst time: %.3f ms" % avg_cpu_burst())
print ("-- average wait time: %.3f ms" % (float(y[0])/sum(num_bursts.values())))
print ("-- average turnaround time: %.3f ms" % (float(y[1])/sum(num_bursts.values())))
print ("-- total number of context switches: %d" % sum(num_bursts.values()))
print ("-- total number of preemptions: 0")