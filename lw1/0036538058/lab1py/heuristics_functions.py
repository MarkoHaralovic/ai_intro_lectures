from algorithms import ucs 

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
          output += f"[CONDITION]: [OK] h({state}) <= h*: {format(h[state], '.1f')} <= {format(real_value, '.1f')}\n"
       else:
          output += f"[CONDITION]: [ERR] h({state}) <= h*: {format(h[state], '.1f')} <= {format(real_value, '.1f')}\n"
          optimistic=False
    if optimistic is True:
         output += f"[CONCLUSION]: Heuristic is optimistic."
    else:
         output += f"[CONCLUSION]: Heuristic is not optimistic."

    return output


def f_check_consistent(initial_state,state_transitions,goal_states,h):
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
         output += f"[CONCLUSION]: Heuristic is consistent."
    else:
         output += f"[CONCLUSION]: Heuristic is not consistent."

    return output