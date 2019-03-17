import sys
import random

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
def checkarrival(time, added,check_process,queue,prior_process,end):
	if not end:
		if check_process not in queue:
			to_add=init_time[check_process]-init_time[prior_process]
			if time+added>init_time[check_process]:
				queue.append(check_process)
				print("time %.3fms: Process arrival [Q" % (time+to_add), end='')
				for j in queue:
					print(" %s" % j, end='')
				print("]")
				return time+to_add
			else:
				return time
		else:
			return time
	else:
		return time
def SJF():
	time = 0.000
	guess=1/int(sys.argv[2])
	estimated={}
	total_estimated={}
	alpha=float(sys.argv[6])
	for i in range(num_processes):
		estimated[proc[i]]=[]
		for burst in cpu_bursts[proc[i]]:
			tau=alpha*burst+(1-alpha)*guess
			estimated[proc[i]].append(tau)
			guess=tau
		total_estimated[proc[i]]=sum(estimated[proc[i]])
	arrival = [k for k in sorted(init_time, key = init_time.get)]
	queue=[]
	priority = [k for k in sorted(total_estimated, key = total_estimated.get)]
	print(arrival)
	print("time %.3fms: Start of simulation [Q" % time, end = '')
	for process in queue:
		print(" %s" % process, end='')
	print("]")
	queue=[]
	queue.append(arrival[0])
	time+=init_time[queue[0]]
	
	print("time %.3fms: Process arrival [Q" % time, end='')
	for j in queue:
		print(" %s" % j, end='')
	print("]")
	arrival_num=1
	end=False
	while queue!=[]:
		newqueue=[]
		for pro in priority:
			if pro in queue:
				newqueue.append(pro)
		queue=newqueue
		process=queue[0]
		queue=queue[1:]
		
		oldtime=time
		time=checkarrival(time,int(sys.argv[5])/2,arrival[arrival_num],queue,arrival[arrival_num-1],end)
		if oldtime!=time:
			if arrival_num!=len(arrival)-1:
				arrival_num=arrival_num+1
			else:
				end=True
		time += int(sys.argv[5])/2
		#checkarrival
		for burst in range(num_bursts[process] - 1):
			# print("time %fms: Process start using the CPU [Q" % time, end='')
			# for j in queue:
			# 	print(" %s" % j, end='')
			oldtime=time
			time=checkarrival(time,cpu_bursts[process][burst],arrival[arrival_num],queue,arrival[arrival_num-1],end)
			if oldtime!=time:
				if arrival_num!=len(arrival)-1:
					arrival_num=arrival_num+1
				else:
					end=True
			time += cpu_bursts[process][burst]
			
			#check
			# print("time %fms: Process finish using the CPU [Q" % time, end='')
			# for j in queue:
			# 	print(" %s" % j, end='')
			# print("]")

			# print("time %fms: Process starts performing I/O [Q" % time, end='')
			# for j in queue:
			# 	print(" %s" % j, end='')
			# print("]")
			oldtime=time
			time=checkarrival(time,io_bursts[process][burst],arrival[arrival_num],queue,arrival[arrival_num-1],end)
			if oldtime!=time:
				if arrival_num!=len(arrival)-1:
					arrival_num=arrival_num+1
				else:
					end=True
			time += io_bursts[process][burst]
			#check
			# print("time %fms: Process finishes performing I/O [Q" % time, end='')
			# for j in queue:
			# 	print(" %s" % j, end='')
			# print("]")

		# Last CPU Burst
		# print("time %fms: Process start using the CPU [Q" % time, end='')
		# for j in queue:
		# 	print(" %s" % j, end='')
		# print("]")
		oldtime=time
		time=checkarrival(time,cpu_bursts[process][num_bursts[process]-1],arrival[arrival_num],queue,arrival[arrival_num-1],end)
		if oldtime!=time:
			if arrival_num!=len(arrival)-1:
				arrival_num=arrival_num+1
			else:
				end=True
		time += cpu_bursts[process][num_bursts[process]-1]
		#check
		# print("time %.3fms: Process terminates by finishing its last CPU burst [Q" % time, end='')
		# for j in queue:
		# 	print(" %s" % j, end='')
		# print("]")
		oldtime=time
		time=checkarrival(time,int(sys.argv[5])/2,arrival[arrival_num],queue,arrival[arrival_num-1],end)
		if oldtime!=time:
			if arrival_num!=len(arrival)-1:
				arrival_num=arrival_num+1
			else:
				end=True
		time += int(sys.argv[5])/2
		
		#check
	print("time %.3fms: Simulator ended for SJF [Q]" % time)

def FCFS():
	time = 0.0
	arrival = [k for k in sorted(init_time, key = init_time.get)]
	queue=[]
	print("time %.3fms: Start of simulation [Q" % time, end = '')
	for process in queue:
		print(" %s" % process, end='')
	print("]")
	queue.append(arrival[0])
	time+=init_time[queue[0]]
	
	print("time %.3fms: Process arrival [Q" % time, end='')
	for j in queue:
		print(" %s" % j, end='')
	print("]")
	arrival_num=1
	end=False
	while queue!=[]:
		process=queue[0]
		queue = queue[1:]
		
		oldtime=time
		time=checkarrival(time,int(sys.argv[5])/2,arrival[arrival_num],queue,arrival[arrival_num-1],end)
		if oldtime!=time:
			if arrival_num!=len(arrival)-1:
				arrival_num=arrival_num+1
			else:
				end=True
		time += int(sys.argv[5])/2
		for burst in range(num_bursts[process] - 1):
			# print("time %fms: Process start using the CPU [Q" % time, end='')
			# for j in queue:
			# 	print(" %s" % j, end='')
			# print("]")
			oldtime=time
			time=checkarrival(time,cpu_bursts[process][burst],arrival[arrival_num],queue,arrival[arrival_num-1],end)
			if oldtime!=time:
				if arrival_num!=len(arrival)-1:
					arrival_num=arrival_num+1
				else:
					end=True
			time += cpu_bursts[process][burst]
			# print("time %fms: Process finish using the CPU [Q" % time, end='')
			# for j in queue:
			# 	print(" %s" % j, end='')
			# print("]")

			# print("time %fms: Process starts performing I/O [Q" % time, end='')
			# for j in queue:
			# 	print(" %s" % j, end='')
			# print("]")
			oldtime=time
			time=checkarrival(time,cpu_bursts[process][burst],arrival[arrival_num],queue,arrival[arrival_num-1],end)
			if oldtime!=time:
				if arrival_num!=len(arrival)-1:
					arrival_num=arrival_num+1
				else:
					end=True
			time += io_bursts[process][burst]
			# print("time %fms: Process finishes performing I/O [Q" % time, end='')
			# for j in queue:
			# 	print(" %s" % j, end='')
			# print("]")

		# Last CPU Burst
		# print("time %fms: Process start using the CPU [Q" % time, end='')
		# for j in queue:
		# 	print(" %s" % j, end='')
		# print("]")
		oldtime=time
		time=checkarrival(time,cpu_bursts[process][num_bursts[process]-1],arrival[arrival_num],queue,arrival[arrival_num-1],end)
		if oldtime!=time:
			if arrival_num!=len(arrival)-1:
				arrival_num=arrival_num+1
			else:
				end=True
		time += cpu_bursts[process][num_bursts[process]-1]
		# print("time %.3fms: Process terminates by finishing its last CPU burst [Q" % time, end='')
		# for j in queue:
		# 	print(" %s" % j, end='')
		# print("]")
		oldtime=time
		time=checkarrival(time,int(sys.argv[5])/2,arrival[arrival_num],queue,arrival[arrival_num-1],end)
		if oldtime!=time:
			if arrival_num!=len(arrival)-1:
				arrival_num=arrival_num+1
			else:
				end=True
		time += int(sys.argv[5])/2
		
	print("time %.3fms: Simulator ended for FCFS [Q]" % time)

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

for i in range(num_processes):
	init_time[proc[i]] = r.drand() * 1000
	num_bursts[proc[i]] = int(r.drand() * 100) + 1
	cpu_bursts[proc[i]] = []
	io_bursts[proc[i]] = []
	for j in range(num_bursts[proc[i]]):
		cpu_bursts[proc[i]].append(r.drand() * 1000)
		
		if (j != num_bursts[proc[i]]-1):
			
			io_bursts[proc[i]].append(r.drand() * 1000)
print(init_time)
SJF()
FCFS()
