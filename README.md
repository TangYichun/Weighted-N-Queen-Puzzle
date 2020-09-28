# CS534 Homework Assignment - N-Queen Problem


## Initial state define:

The program ask the user to provide the chess board input from csv file, the method (1 or 2), and the heuristic function (H1, H2 or H3) to use the solve the problem. For example, the input “nqueen.csv 1 H1” means solve the n-queen problem with A* method and heuristic function H1. Each input should be separated by space.

The program will print the initial (start) state as a list of numbers. For example, [4, 3, 0, 2, 1] means a 5*5 board with: 

[0, 0, Q, 0, 0]<br />
[0, 0, 0, 0, Q]<br />
[0, 0, 0, Q, 0]<br />
[0, Q, 0, 0, 0]<br />
[Q, 0, 0, 0, 0]

The weight will store in a separate list. 

## Parameter:

1. len(pq_list) (A*), step (Simulated Annealing)= number of node that were expanded
2. interval (A*), time (Simulated Annealing) = total time to solve the n queen puzzle
3. len(close_list) (A*) = effective branch
	effective (Simulated Annealing) — 
	Since simulated annealing always expand node randomly and the effective branch is always 1 (whether 	it choose to move or not), so for Simulated Annealing, the effective branch = 1
4. g_x (A*), final_cost (Simulated Annealing) = the cost for moving the queen to the solution
5. Sequence of move: <br />
a. list_minus(state, pos) (A*): since a* has to expand every node, we don't want to output every single move sequence, but we can visualize it by print(next_state.state).
	Also, since the output of move might contain negative number. In the program, negative number means the queen goes up, positive means queen goes down.<br />
b. print("current pos and hvalue", pos, choice_heuristic(pos, weight, hchoice)) — Simulated Annealing (output every move that it choose to go, dismiss if it choose to stay in the current position)


## Heuristic:

In this problem we use three different heuristic function to determine the move of queens.

H1: the square of the lightest queen across all pairs of queens attacking each other.

H2: sum across every pair of attacking queens the squared weight of the lightest queen.

H3: minimum of number of attacking pairs and the square of the lightest queen across of all pairs of attacking queens.

Both H1 and H3 are admissible, H2 is not admissible. The reason is that the cost could be lower than the heuristic value. Counterexample: the start state is [4, 3, 0, 2, 1], and the start weight is [9, 3, 1, 4, 2], H2, in this case is 2^2+3^2 = 13, but moving the lightest queen (position 1 and weight 2) down with one grid (position 1) will cost 4, which is less than H2.

H3: since we already know that H1 is admissible, and ‘# of pairs of attacking queens’ is not admissible only if for example, the start state is [4, 3, 0, 2, 1], and the start weight is [9, 3, 1, 4, 2], H2, in this case is 2, but moving the lightest queen (position 0 and weight 1) down with one grid (position 1) will cost 1, which is less than the # of attacking pairs, but since we are choosing the minimum, so we can guarantee the heuristic function is admissible.




## Approach: 

### A*: 
expend every node and keep them in the open list, move all the visited nodes to the close list. Use priority queen to put the smallest h+g value node in the first of the queue. Also, updating the cost and heuristic value for every changing node.

### Simulated Annealing: 
since the assignment said we are free to make use of simulated annealing, I choose to use simulated annealing. In the program, I choose the initial temperature = n*3, where n = the size of the chess board, and the decrease rate of the temperature = 1 - 0.90 = 0.10. The reason is that I want the temperature as high as possible so it can move all states across the board to avoid stuck in the local maximum, and the decrease rate as slow as possible (as long as it is reasonable) to allow the temperature to decrease slowly. The lowest temperature is 0.001 (close to 0, as it will become greedy hill climbing when temperature = 0). As the temperature is relatively high, the program does not really need to do a restart to find the since the move under a high temperature is relatively random, which already give a sense of ‘restart’ for the algorithm.
