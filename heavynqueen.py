import csv
import numpy as np
import random
import time
import math
import copy
from queue import PriorityQueue



def processstate(initial_list):
	boardn = len(initial_list)
	weight = [0]*len(initial_list)
	pos = [0]*len(initial_list)
	nl = 0
	for row in range(len(initial_list)):
		for col in range(len(initial_list)):
			if initial_list[row][col] == '':
				initial_list[row][col] = '0'
	for i in initial_list:
		initial = list(map(int,i))
		length = len(initial)
		for j in range(length):
			if initial[j] != 0:
				weight[j] = initial[j]
				pos[j] = nl
		nl += 1
	inistate = [pos, weight]
	return inistate

def choice_heuristic(pos, weight, hcoice):
	if hchoice == 'H2':
		hvalue = 0
		for i in range(len(pos)):
			for j in range(i+1, len(pos)):
				diag = j-i
				if pos[i] == pos[j] or abs(pos[j]-pos[i]) == diag:
					hvalue += min(weight[i], weight[j])**2
	elif hchoice == 'H3' or hchoice == 'H1':
		count = 0
		for i in range(len(pos)):
			for j in range(i+1, len(pos)):
				diag = j-i
				if pos[i] == pos[j] or abs(pos[j]-pos[i]) == diag:
					count += 1
		alter_h = 0
		attack = [0]*len(pos)
		atweight = [10]*len(weight)
		for i in range(len(pos)):
			for j in range(i+1, len(pos)):
				diag = j-i
				if pos[i] == pos[j] or abs(pos[j]-pos[i]) == diag:
					attack[i] = 1
					attack[j] = 1

		for queen in range(len(attack)):
			if attack[queen] == 1:
				atweight[queen] = weight[queen]

		alter_h = min(atweight) ** 2

		if all(i == 0 for i in attack):
			alter_h = 0

		if hchoice == 'H1':
			hvalue = alter_h
		else:
			hvalue = min(alter_h, count)
	return hvalue


def final_cost_hc(pos, weight, initial_pos):
	cost = 0
	for i in range(len(pos)):
		cost += abs(initial_pos[i]-pos[i])*(weight[i]**2)
	return cost



def simulated_move(pos, weight, heuristic, temp, hchoice):
	move = False
	cost_cur = heuristic
	while move is False:
		## find the new grid to move:
		new_state = list(pos)
		row = random.randint(0, len(pos)-1)
		col = random.randint(0, len(pos)-1)
		new_state[col] = row
		cost_new = choice_heuristic(new_state, weight, hchoice)
		if cost_new > cost_cur:
			prob = math.exp((cost_cur-cost_new)/temp)
			move = random.random() <= prob
		else:
			move = True
	if move is True:
		pos = new_state
	return pos

def simulated_annealing(pos, weight, start, hchoice):
	step = 0
	effective = 0
	temperature = len(pos)**3
	annealing = 0.90
	cost_start_initial = choice_heuristic(pos, weight, hchoice)
	while choice_heuristic(pos, weight, hchoice) > 0 and time.time()-start <= 10.0:
		state = simulated_move(pos, weight, choice_heuristic(pos, weight, hchoice), temperature, hchoice)
		t = max(temperature*annealing, 0.001) # if 0, then greedy hc
		temperature = t
		if state != pos:
			step += 1
			print("State Updated:", pos)
		pos = state
	effective += 1
	print("Effective Branching Factor: ", effective)
	return pos




file_name, method, hchoice = input("Enter the filename, method（1: A*, 2: Simulated Annealing） and choice of heuristic function for the problem, seperate with space:").split()
with open(file_name, newline='', encoding='utf-8-sig') as csvfile:
    initial_list = list(csv.reader(csvfile))

initial_state = processstate(initial_list)

pos = initial_state[0]
weight = initial_state[1]

if method == '1':
	pq=PriorityQueue()
	pq_list=[]
	close_list=[]

	start_time = time.time()

	N = len(pos)

	class Node:
	    def __init__(self,N=0):
	        self.state=[0]*N
	        #self.g_x=0
	        #self.h_x=0
	        #self.parent= None

	def cost(state, weight):
	    cost_value = 0
	    for i in range(len(weight)):
	        cost_value += abs(list_minus(pos, state)[i]) * weight[i]**2 
	    return(cost_value)

	def list_minus(a, b):
	    c = []
	    for i in range(len(a)):
	        c.append(a[i] -b[i])
	    return (c)

	def populate(x):
	    temp = Node()
	    for col in range(N):
	        for row in range(N):
	            state = x.state[:]
	            state[col] = row
	            temp.state = state
	            g_x = cost(state, weight)
	            h_x = choice_heuristic(state, weight, hchoice)
	            temp.f_x = g_x + h_x
	            #temp.g_x = cost(state, weight)
	            #temp.h_x = heuristic1(state, weight)
	            #temp.parent = x
	            if not temp.state in close_list:
	                a=copy.deepcopy(temp)
	                pq_list.append(a)
	                #pq.put((temp.g_x + temp.h_x, len(pq_list)-1))
	                pq.put((temp.f_x, len(pq_list)-1))
	            if h_x == 0:
	                print("Find result astar:", state)
	                print("Num of nodes were expanded astar:", len(pq_list))
	                print("Length of the solution path astar:", len(close_list))
	                print("Solution cost astar:", g_x)
	                print('Sequence of moves astar:', list_minus(state, pos))
	                return False
	    return True


	begin = Node()
	begin.state = pos
	close_list.append(begin.state)

	result = True

	while(result):
		result &= populate(begin)
		next_indice = pq.get()
		print(next_indice)
		next_state = pq_list[next_indice[1]]
		begin = next_state
		close_list.append(next_state.state)
		print(next_state.state)

		if (time.time()-start_time > 10):
			break


	end_time = time.time()
	interval = (end_time-start_time)
	print(interval, 's astar')

if method == '2':
	pos = initial_state[0]
	weight = initial_state[1]
	print("Start State:", pos)
	final_hvalue = choice_heuristic(pos, weight, hchoice)
	start = time.time()
	result = pos
	#node_expand = 0
	result = simulated_annealing(pos, weight, start, hchoice)
	final_hvalue = choice_heuristic(result, weight, hchoice)
	print(result, final_hvalue)
	final_cost = final_cost_hc(result, weight, pos)
	print("results:", result)
	print("total time:", time.time()-start)
	print("total cost:", final_cost)








