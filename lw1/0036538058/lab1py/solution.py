import getopt
import sys
import os
from queue import PriorityQueue

algorithms = ['bfs','ucs','astar']
# --ss: path to state space descriptor file,
# --h: path to heuristic descriptor file,
# --check-optimistic: flag for checking if given heuristic is optimistic,
# --check-consistent: flag for checking if given heuristic is consistent

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
   # print(h_lines)  
   h = {line.split(": ")[0]:float(line.split(": ")[1]) for line in h_lines}

def init_state_space(ss_lines):
   state_transitions = {}
   initial_state, goal_states= None, None
   for idx,line in enumerate(ss_lines):
      line = line.strip()
      if line.startswith('#') or line == "\n" or line == " ":
         continue
      if initial_state is None:
         initial_state = line
         continue
      if goal_states is None:
         goal_states = [goal_state for goal_state in line.split()]
         continue
      state, actions = line.split(":")[0],line.split(":")[1]
      actions = actions.strip()
      state_transitions[state] = {}
      for transitions in actions.split(" "):
         if transitions.split(",")[0] and transitions.split(",")[1]:
            state_transitions[state][transitions.split(",")[0]] = float(transitions.split(",")[1])
   return initial_state, goal_states, state_transitions

initial_state, goal_states, state_transitions = init_state_space(ss_lines)


def find_path_bfs(state, parent):
    path = []
    while state is not None:
        path.append(state)
        state = parent[state]
    return path[::-1]

def find_path(state,parent):
   path = [state]
   while state in parent:
      state = parent[state]
      path.append(state)
   path.reverse()
   path.pop(0)
   return path

   
def bfs(s0,succ,goal):
   if s0 in goal:
      return s0,True,0,1,0,s0
   open = [(s0, 0, 0)]
   parent = {s0: None}
   #depth_dict = {0 : [s0]}
   visited = set([s0])
   while open:
      x_state,x_depth,x_cost = open.pop(0)
      # if x_depth not in depth_dict:
      #    depth_dict[x_depth] = []
      # depth_dict[x_depth].append(x_state)
      # print(x_state,x_depth,x_cost)
      if x_state in goal:
         #total_states_before_current_depth = sum(len(depth_dict[d]) for d in depth_dict if d < x_depth)
         path = find_path_bfs(x_state,parent)
         return x_state,True,len(path),len(visited),x_cost,path

      for m_state,m_cost in succ[x_state].items():
         if m_state not in visited:
            visited.add(m_state)
            parent[m_state] = x_state
            open.append((m_state, x_depth + 1, m_cost + x_cost))
      open.sort(key=lambda x:x[1])
   return None,False,None,len(visited),None

def ucs(s0, succ, goal):
    if s0 in goal:
        return s0, True, 0, 1, 0, [s0]

    open_set = [(s0, 0)]
    parent = {s0: None}
    cost_to_state = {s0: 0}
    visited = set()

    while open_set:
        open_set.sort(key=lambda x: x[1])  
        x_state, x_cost = open_set.pop(0)
        visited.add(x_state)

        if x_state in goal:
            path = find_path(x_state, parent)
            return x_state, True, len(path), len(visited), x_cost, path

        for m_state, m_cost in succ[x_state].items():
            new_cost = x_cost + m_cost
            if m_state not in visited:
                  open_set.append((m_state, new_cost))
            if m_state not in cost_to_state or new_cost < cost_to_state[m_state]:
                parent[m_state] = x_state
                cost_to_state[m_state] = new_cost

    return None, False, None, len(visited), None, None
 
def a_star(s0,succ,goal,h):
   if s0 in goal:
      return s0, True, 0, 1, 0, [s0]

   open = [(s0, 0, 0)]
   closed = {}
   parent = {s0: None}

   while open:
      state,g,f = open.pop(0)
      if state in goal:
         path = find_path(state, parent)
         return state, True, len(path), len(closed.keys()), g, path 
      if state not in closed.keys():
         closed[state] = g
      for m_state,g_cost in succ[state].items():
         h_cost = h[m_state] if m_state in h else None
         
         total_g = g + g_cost
         if any(m_state == x[0] and total_g < x[1] for x in open):
            open = [x for x in open if x[0] != m_state]
            open.append((m_state, total_g, h_cost))
            del closed[m_state] 
            del parent[m_state]
         if m_state in closed.keys():
            if closed[m_state] <= total_g:
               continue
            else:
               del closed[m_state] 
               del parent[m_state]
               
         closed[m_state] = total_g
         parent[m_state] = state
         open.append((m_state,total_g,total_g+h_cost))
         open.sort(key=lambda x: x[2])  
   return 

def f_check_optimistic(initial_state, state_transitions, goal_states, h):
    cost_to_goal_state = {state: 0 for state in goal_states}

    checked = set(goal_states)

    next_states = [initial_state]
    checked.add(initial_state)

    while next_states:
        current_state = next_states.pop(0)
        _,_,_,_,cost,_ = ucs(current_state, state_transitions, goal_states)
        cost_to_goal_state[current_state] = cost

        for next_state in state_transitions.get(current_state, {}):
            if next_state not in checked:
                checked.add(next_state)
                next_states.append(next_state)
    output = ''
    optimistic=True
    for state, real_value in cost_to_goal_state.items():
       if h[state] <= real_value:
          output += f"[CONDITION]: [OK] h({state}) <= h*: {h[state]} <= {real_value}\n"
       else:
          output += f"[CONDITION]: [ERR] h({state}) <= h*: {h[state]} <= {real_value}\n"
          optimistic=False
    if optimistic is True:
         output += f"[CONCLUSION]: Heuristic is optimistic.\n"
    else:
         output += f"[CONCLUSION]: Heuristic is not optimistic.\n"

    return output


def f_check_consistent(initial_state,state_transitions,goal_state,h):
    cost_to_goal_state = {state: 0 for state in goal_states}

    checked = set(goal_states)

    next_states = [initial_state]
    checked.add(initial_state)

    while next_states:
        current_state = next_states.pop(0)
        _,_,_,_,cost,_ = ucs(current_state, state_transitions, goal_states)
        cost_to_goal_state[current_state] = cost

        for next_state in state_transitions.get(current_state, {}):
            if next_state not in checked:
                checked.add(next_state)
                next_states.append(next_state)
    output = ''
    consistent=True
    for state, real_value in cost_to_goal_state.items():
        for next_state, step_cost in state_transitions[state].items():
          if h[state] <= h[next_state] + step_cost:
             output += f"[CONDITION]: [OK] h({state}) <= h({next_state}) + c: {h[state]} <= {h[next_state] } + {step_cost}\n"
          else:
             output += f"[CONDITION]: [ERR] h({state}) <= h({next_state}) + c: {h[state]} <= {h[next_state] } + {step_cost}\n"
             consistent = False
    if consistent is True:
         output += f"[CONCLUSION]: Heuristic is consistent.\n"
    else:
         output += f"[CONCLUSION]: Heuristic is not consistent.\n"

    return output


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

   
#todo : values should be float