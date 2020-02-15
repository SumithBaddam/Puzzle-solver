#!/usr/local/bin/python3
# solve_luddy.py : Sliding tile puzzle solver
#
# Code by: Sumith Reddy Baddam (srbaddam), Sai Swapna Gollapudi (sagoll)
#
# Based on skeleton code by D. Crandall, September 2019
#
import queue as Q
import heapq
goal_state = list(range(1,16))
goal_state
import sys

MOVES = { "R": (0, -1), "L": (0, 1), "D": (-1, 0), "U": (1,0) }
C_MOVES = { "R": ((0, -1),(0,3)), "L": ((0, 1),(0,-3)), "D": ((-1, 0),(3,0)), "U": ((1,0),(-3,0)) }
L_MOVES = { "A": (2, 1), "B": (2, -1), "C": (-2, 1), "D": (-2, -1), "E": (1, 2), "F": (1, -2), "G": (-1, 2), "H": (-1, -2)}

def rowcol2ind(row, col):
    return row*4 + col

def ind2rowcol(ind):
    return (int(ind/4), ind % 4)

def valid_index(row, col):
    return 0 <= row <= 3 and 0 <= col <= 3

def swap_ind(list, ind1, ind2):
    return list[0:ind1] + (list[ind2],) + list[ind1+1:ind2] + (list[ind1],) + list[ind2+1:]

def swap_tiles(state, row1, col1, row2, col2):
    return swap_ind(state, *(sorted((rowcol2ind(row1,col1), rowcol2ind(row2,col2)))))

def printable_board(row):
    return [ '%3d %3d %3d %3d'  % (row[j:(j+4)]) for j in range(0, 16, 4) ]

def heuristic_fun(a):
    h_cost = 0
    for i in range(len(goal_state)):
        if goal_state[i] != a[i]:
            h_cost += 1
    return h_cost
def l_heuristic_fun(a):
    h_cost = 0
    for i in range(len(goal_state)):
        if goal_state[i] != a[i]:
            h_cost += 1
    for i in range(1,len(goal_state)+1):
        (x,y) = ind2rowcol(a.index(i))
        (c,d) = ind2rowcol(i-1)
        h_cost += (abs(x-c) + abs(y-d)) % 3
        num = (abs(x-c) + abs(y-d)) / 3
        if num >= 1:
            h_cost += num - 1
    return h_cost

# return a list of possible successor states
def successors(state, closed):
    (empty_row, empty_col) = ind2rowcol(state.index(0))
    succ_states = list()
    if solve_for == "original":
        for (c, (i, j)) in MOVES.items():
            if valid_index(empty_row+i, empty_col+j):
                b = swap_tiles(state, empty_row, empty_col, empty_row+i, empty_col+j)
                h_cost = heuristic_fun(b)
                #print("Successor states: heusristic cost, state, route, cost to move:", (h_cost, b, c, 3))
                #if b not in closed:
                succ_states.append((h_cost, b, c, 1))
        return succ_states
    elif solve_for == "circular":
        for (c, (x,y)) in C_MOVES.items():
            for (i,j) in (x,y):
                if valid_index(empty_row+i, empty_col+j):
                    b = swap_tiles(state, empty_row, empty_col, empty_row+i, empty_col+j)
                    h_cost = heuristic_fun(b)
                    #print("Successor states: heusristic cost, state, route, cost to move:", (h_cost, b, c, 3))
                    #if b not in closed:
                    succ_states.append((h_cost, b, c, 1))
        return succ_states
    else:
        for (c, (i, j)) in L_MOVES.items():
            if valid_index(empty_row+i, empty_col+j):
                b = swap_tiles(state, empty_row, empty_col, empty_row+i, empty_col+j)
                h_cost = l_heuristic_fun(b)
                #print("Successor states: heusristic cost, state, route, cost to move:", (h_cost, b, c, 3))
                #if b not in closed:
                succ_states.append((h_cost, b, c, 1))
        return succ_states
        # check if we've reached the goal
def is_goal(state):
    return sorted(state[:-1]) == list(state[:-1]) and state[-1]==0
def solve(initial_board):
    closed = list()
    #fringe = Q.PriorityQueue()
    fringe = []
    heapq.heappush(fringe, (heuristic_fun(initial_board),initial_board, "", 0))
    #fringe.put((heusristic_fun(initial_board),(initial_board, "", 0)))
    #while not fringe.empty():
    while len(fringe) != 0:
        #(total_cost, (state, route_so_far, cost_so_far)) = fringe.get()
        (total_cost, state, route_so_far, cost_so_far) = heapq.heappop(fringe)
        closed.append(state)
        if is_goal(state):
            return( route_so_far, cost_so_far)
        for ( heuristic_cost, succ, move, cost) in successors( state,closed ):
            if succ in closed:
                continue
            else:
                if len(fringe) != 0 and succ not in list(zip(*fringe))[1]:
                    heapq.heappush(fringe,(heuristic_cost + cost_so_far + cost, succ, route_so_far + move, cost_so_far + cost ) )
                    #print("fringe after push is,", fringe)
                if len(fringe) == 0:
                    heapq.heappush(fringe,(heuristic_cost + cost_so_far + cost, succ, route_so_far + move, cost_so_far + cost ) )
                if len(fringe) != 0 and succ in list(zip(*fringe))[1]:
                    a = list(zip(*fringe))[1]
                    #print("a is ",list(a))
                    if succ in list(a):
                        idx = list(a).index(succ)
                        prev_cost = fringe[idx][0]
                        if prev_cost > (cost_so_far + heuristic_cost + cost) :
                            b = [(cost_so_far + heuristic_cost + cost,fringe[idx][1],fringe[idx][2],fringe[idx][3])]
                            fringe = fringe[0:idx]+ b +fringe[idx+1:]
    return Inf,Inf
def solve_luddy(initial_board):
  closed = list()
  #fringe = Q.PriorityQueue()
  fringe = []
  heapq.heappush(fringe, (l_heuristic_fun(initial_board),initial_board, "", 0))
  #fringe.put((l_heuristic_fun(initial_board),(initial_board, "", 0)))
  #while not fringe.empty():
  while len(fringe) != 0:
      #(total_cost, (state, route_so_far, cost_so_far)) = fringe.get()
      (total_cost, state, route_so_far, cost_so_far) = heapq.heappop(fringe)
      closed.append(state)
      if is_goal(state):
          return( route_so_far, cost_so_far)
      for ( heuristic_cost, succ, move, cost) in successors( state,closed ):
        ind = succ.index(0)
        p_inv = 0
        p_inv = ind2rowcol(ind)[0] + 1
        for i in succ:
            for j in range(succ.index(i)+1,len(succ)):
                if(i > succ[j] and succ[j] != 0 and i != 0):
                    p_inv += 1
        #print("P inv is ",p_inv)
        if succ in closed or p_inv%2 != 0:
            continue
        else:
          if len(fringe) != 0 and succ not in list(zip(*fringe))[1]:
              #if p_inv%2 == 0:
              heapq.heappush(fringe,(heuristic_cost + cost_so_far + cost, succ, route_so_far + move, cost_so_far + cost))
              #print("fringe after push is,", fringe)
          if len(fringe) == 0:
              heapq.heappush(fringe,(heuristic_cost + cost_so_far + cost , succ, route_so_far + move, cost_so_far + cost ) )
          if len(fringe) != 0 and succ in list(zip(*fringe))[1]:
              a = list(zip(*fringe))[1]
              #print("a is ",list(a))
              if succ in list(a):
                  idx = list(a).index(succ)
                  prev_cost = fringe[idx][0]
                  if prev_cost > (cost_so_far + heuristic_cost + cost) :
                      b = [(cost_so_far + heuristic_cost + cost,fringe[idx][1],fringe[idx][2],fringe[idx][3])]
                      fringe = fringe[0:idx]+ b +fringe[idx+1:]
  return Inf,Inf

if __name__ == "__main__":
  import heapq
  if(len(sys.argv) != 3):
      raise(Exception("Error: expected 2 arguments"))
  start_state = []
  solve_for = sys.argv[2]
  with open(sys.argv[1], 'r') as file:
  #with open("boardn.txt", 'r') as file:
      for line in file:
          start_state += [ int(i) for i in line.split() ]

  if len(start_state) != 16:
      raise(Exception("Error: couldn't parse start state file"))
  print("Start state: \n" +"\n".join(printable_board(tuple(start_state))))

  print("Solving...")
  ind = start_state.index(0)
  p_inv = ind2rowcol(ind)[0] + 1
  for i in start_state:
      for j in range(start_state.index(i)+1,len(start_state)):
          if(i > start_state[j] and start_state[j] != 0 and i != 0):
              p_inv += 1
      #print("P inv is ",p_inv)
  if p_inv%2 == 0:
      if solve_for != 'luddy':
        route,cost_final = solve(tuple(start_state))
      else:
        route,cost_final = solve_luddy(tuple(start_state))
      if route != "Inf":
        print("Solution found in " + str(len(route)) + " moves:" + "\n" + route)
      else:
        print("Inf")
  else:
      print("Inf")
