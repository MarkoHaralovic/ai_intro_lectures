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


def find_path(state,parent):
   path = [state]
   while state in parent:
      state = parent[state]
      path.append(state)
   path.reverse()
   path.pop(0)
   return path