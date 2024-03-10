import getopt
import sys
import os

algorithms = ['bfs','ucs','astar']
# --ss: path to state space descriptor file,
# --h: path to heuristic descriptor file,
# --check-optimistic: flag for checking if given heuristic is optimistic,
# --check-consistent: flag for checking if given heuristic is consistent

argumentList = sys.argv[1:]

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
               h = argumentList[argumentList.index('--h') + 1]
         ss = argumentList[argumentList.index('--ss') + 1]
elif '--ss' and '--h'  and 'check-optimistic' in argumentList:
   ss = argumentList[argumentList.index('--ss') + 1]
   h = argumentList[argumentList.index('--h') + 1]
   check_optimistic = True
elif '--ss' and '--h'  and 'check-consistent' in argumentList:
   ss= argumentList[argumentList.index('--ss') + 1]
   h = argumentList[argumentList.index('--h') + 1]
   check_consistent = True

#Got the code fromhttps://stackoverflow.com/questions/10487563/unicode-error-handling-with-python-3s-readlines
state_space_file = open(ss, 'r', encoding='utf-8', errors='ignore')
ss_lines = state_space_file.readlines()

if alg =='astar':
   heuristics_file = open(h, 'r', encoding='utf-8', errors='ignore')
   h_lines = heuristics_file.readlines()
   
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
            state_transitions[state][transitions.split(",")[0]] = int(transitions.split(",")[1])
   return initial_state, goal_states, state_transitions

initial_state, goal_states, state_transitions = init_state_space(ss_lines)

def find_path_bfs(state, parent):
    path = []
    while state is not None:
        path.append(state)
        state = parent[state]
    return path[::-1]

def find_path_ucs(state,parent):
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
   visited = set([s0])
   
   while open:
      x_state,x_depth,x_cost = open.pop(0)

      if x_state in goal:
         path = find_path_bfs(x_state,parent)
         return x_state,True,x_depth+1,len(visited),x_cost,path
      
      for m_state,m_cost in succ[x_state].items():
         if m_state not in visited:
               visited.add(m_state)
               parent[m_state] = x_state
               open.append((m_state, x_depth + 1, m_cost + x_cost))
   return None,False,None,len(visited),None

def ucs(s0,succ,goal):
   if s0 in goal:
      return s0,True,0,1,0,s0
   open = [(s0,0,0)]
   parent = {s0:None}
   visited = set([s0])
   
   while open:
      x_state,x_depth,x_cost = open.pop(0)
      visited.add(x_state)
      if x_state in goal:
         path = find_path_ucs(x_state,parent)
         return x_state,True,x_depth+1,len(visited),x_cost,path
      for m_state,m_cost in succ[x_state].items():
         if m_state:
            if m_state not in parent:
               parent[m_state] = x_state
            else:
               if x_cost + m_cost < x_cost:
                  parent[m_state] = x_state
            open.append((m_state, x_depth + 1, m_cost + x_cost))
            open.sort(key=lambda x:x[2])
   return None,False,None,len(visited),None

if alg == 'bfs':
   x_state,found,x_depth,visited,x_cost,path = bfs(initial_state,state_transitions,goal_states)
   output = f"# BFS {ss.split('/')[-1]}\n"
   output+= f"[FOUND_SOLUTION]: {found}\n"
   output+= f"[STATES_VISITED]: {visited}\n"
   output+= f"[PATH_LENGTH]: {x_depth}\n"
   output+= f"[TOTAL_COST]: {x_cost}\n"
   output+= f"[PATH]: {' => '.join(path)}\n"
elif alg == 'ucs':
   x_state,found,x_depth,visited,x_cost,path = ucs(initial_state,state_transitions,goal_states)
   output = f"# UCS {ss.split('/')[-1]}\n"
   output+= f"[FOUND_SOLUTION]: {found}\n"
   output+= f"[STATES_VISITED]: {visited}\n"
   output+= f"[PATH_LENGTH]: {x_depth}\n"
   output+= f"[TOTAL_COST]: {x_cost}\n"
   output+= f"[PATH]: {' => '.join(path)}\n"
   
#BFS
#AI fail_course True  3 6 21  enroll_artificial_intelligence => fail_lab => fail_course
#ISTRA Buzet True 5 11(17) 100 Pula => Barban => Labin => Lupoglav => Buzet

#ucs
#AI pass_course True  4 7 17  enroll_artificial_intelligence => complete_lab => pass_continuous =>pass_course
#Istra Buzet True 5 17 (16) 100 Pula => Barban => Labin => Lupoglav => Buzet