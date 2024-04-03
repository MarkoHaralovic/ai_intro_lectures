from auxiliary import find_path 

def bfs(s0,succ,goal):
   if s0 in goal:
      return s0,True,0,1,0,s0
   open = [(s0, 0, 0)]
   parent = {s0: None}
   visited = set([s0])
   while open:
      x_state,x_depth,x_cost = open.pop(0)
      if x_state in goal:
         path = find_path(x_state,parent)
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
