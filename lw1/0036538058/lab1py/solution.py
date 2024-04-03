import sys
from auxiliary import init_state_space,find_path
from algorithms import bfs,ucs,a_star
from heuristics_functions import f_check_consistent,f_check_optimistic
algorithms = ['bfs','ucs','astar']

argumentList = sys.argv[1:]

alg,check_optimistic,check_consistent = None,False,False

if '--alg' in argumentList:
   alg = argumentList[argumentList.index('--alg') + 1]
   if alg in algorithms:
      if '--ss' not in argumentList:
         print('Error: --ss is missing')
         sys.exit()
      if 'check-optimistic' in argumentList or 'check-consistent' in argumentList:
         print('Error: --check-optimistic or --check-consistent improperly used')
         sys.exit()
      else:
         if alg == 'astar':
            if '--h' not in argumentList:
               print('Error: --h is missing')
               sys.exit()
            else:
               h_file = argumentList[argumentList.index('--h') + 1]
         ss = argumentList[argumentList.index('--ss') + 1]
elif '--ss' in argumentList and '--h' in argumentList and '--check-optimistic' in argumentList:
    ss = argumentList[argumentList.index('--ss') + 1]
    h_file = argumentList[argumentList.index('--h') + 1]
    check_optimistic = True
elif '--ss' in argumentList and '--h' in argumentList and '--check-consistent' in argumentList:
    ss= argumentList[argumentList.index('--ss') + 1]
    h_file= argumentList[argumentList.index('--h') + 1]
    check_consistent = True


#Got the code from https://stackoverflow.com/questions/10487563/unicode-error-handling-with-python-3s-readlines
state_space_file = open(ss, 'r', encoding='utf-8', errors='ignore')
ss_lines = state_space_file.readlines()

if alg =='astar' or check_consistent or check_optimistic:
   heuristics_file = open(h_file, 'r', encoding='utf-8', errors='ignore')
   h_lines = heuristics_file.readlines()
   h_lines = [line.strip("\n") for line in h_lines]
   h = {line.split(": ")[0]:float(line.split(": ")[1]) for line in h_lines}

initial_state, goal_states, state_transitions = init_state_space(ss_lines)
   
if alg == 'bfs':
   x_state,found,x_depth,visited,x_cost,path = bfs(initial_state,state_transitions,goal_states)
   response = 'yes' if found else 'no'
   output = f"# BFS {ss.split('/')[-1]}\n"
   output+= f"[FOUND_SOLUTION]: {response}\n"
   output+= f"[STATES_VISITED]: {visited}\n"
   output+= f"[PATH_LENGTH]: {x_depth}\n"
   output+= f"[TOTAL_COST]: {x_cost}\n"
   output+= f"[PATH]: {' => '.join(path)}"
   print(output)
elif alg == 'ucs':
   x_state,found,x_depth,visited,x_cost,path = ucs(initial_state,state_transitions,goal_states)
   response = 'yes' if found else 'no'
   output = f"# UCS {ss.split('/')[-1]}\n"
   output+= f"[FOUND_SOLUTION]: {response}\n"
   output+= f"[STATES_VISITED]: {visited}\n"
   output+= f"[PATH_LENGTH]: {x_depth}\n"
   output+= f"[TOTAL_COST]: {x_cost}\n"
   output+= f"[PATH]: {' => '.join(path)}"
   print(output)
elif alg =='astar':
   x_state,found,x_depth,visited,x_cost,path = a_star(initial_state,state_transitions,goal_states,h)
   response = 'yes' if found else 'no'
   output = f"# A-STAR {h_file.split('/')[-1]}\n"
   output+= f"[FOUND_SOLUTION]: {response}\n"
   output+= f"[STATES_VISITED]: {visited}\n"
   output+= f"[PATH_LENGTH]: {x_depth}\n"
   output+= f"[TOTAL_COST]: {x_cost}\n"
   output+= f"[PATH]: {' => '.join(path)}"
   print(output)
elif check_optimistic:
   output = f"# HEURISTIC-OPTIMISTIC {h_file.split('/')[-1]}\n"
   output += f_check_optimistic(initial_state,state_transitions,goal_states,h)
   print(output)
elif check_consistent:
   output = f"# HEURISTIC-CONSISTENT {h_file.split('/')[-1]}\n"
   output += f_check_consistent(initial_state,state_transitions,goal_states,h)
   print(output)
