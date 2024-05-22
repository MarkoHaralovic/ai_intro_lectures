import argparse
import itertools

def parse_command_line():
   parser = argparse.ArgumentParser()
   parser.add_argument('task',type=str,choices=['resolution','cooking'],help="Type of task to run")
   parser.add_argument('path_to_clause_file',type=str,help="Path to the file with the list of clauses")
   parser.add_argument('path_to_user_commands_file',type=str,nargs='?',help="Path to the file with a list of user commands")
   args = parser.parse_args()
   return args

def parse_user_commands_file(path_to_user_commands_file):
   pass

def negate(clause):
    return tuple(el.strip("~") if "~" in el else f"~{el}" for el in clause)
 
def is_tautology(clause):
    for literal in clause:
        if literal.startswith("~"):
            if literal[1:] in clause:
                return True
        else:
            if f"~{literal}" in clause:
                return True
    return False

def remove_redundant_clauses(clauses):
    non_redundant_clauses = set()
    for clause in clauses:
        clause_set = set(clause)
        if not any(clause_set != set(other_clause) and clause_set.issubset(set(other_clause)) for other_clause in clauses):
            non_redundant_clauses.add(clause)
    return non_redundant_clauses

def parse_clause_file(path_to_clause_file):
    clauses = {}
    file = open(path_to_clause_file, 'r')
    line_number = 0
    flag = False
    while True:
        line = file.readline()
        if not line:
            file.close()
            break
        if line.startswith("#"):
            continue
        line_number += 1
        line_elements = line.strip().split(" ")
        line_tuple = tuple(sorted(element.lower() for element in line_elements if element.lower() != "v"))
        if is_tautology(line_tuple):
            line_number -= 1
            continue
        if line_tuple in clauses.keys():
            flag=True
        clauses[line_tuple] = line_number
        target_clause = line_tuple
    orig = target_clause
    if not flag:
        del clauses[target_clause]
    target_clause_negated = {}
    for clause in negate(target_clause):
        negated_clause_tuple = (clause,)
        target_clause_negated[negated_clause_tuple] = line_number
        line_number += 1
    sorted_clauses = {key: clauses[key] for key in sorted(clauses)}
    return sorted_clauses, target_clause_negated, line_number,orig

def plResolve(clause_1, clause_2,clauses):
    clause1_set = set(clause_1)
    clause2_set = set(clause_2)
    resolvents = set()

    for element in clause1_set:
        complementary_element = element[1:] if element.startswith("~") else f"~{element}"
        if complementary_element in clause2_set:
            new_clause = clause1_set.union(clause2_set) - {element, complementary_element}
            if not new_clause: 
               return ("NIL",)
            if is_tautology(new_clause):
               continue
            if tuple(sorted(new_clause)) not in clauses.keys():
                resolvents.add(tuple(sorted(new_clause)))
    return sorted(resolvents, key=len)

def resolution(clauses, target_clause_negated, line_num,verbose=False):
    sos = set(target_clause_negated.keys())
    new = set()
    step_count = 1 
    
    while True:
        for clause1 in sos:
            #gotten from https://www.geeksforgeeks.org/python-itertools-chain/
            for clause2 in itertools.chain(clauses.keys(), sos):
                if clause1 != clause2:
                    resolvents = plResolve(clause1, clause2, clauses)
                    if resolvents:
                        if verbose:
                            print(f"{step_count}. Resolving {clause1} and {clause2}: {resolvents}")
                        step_count += 1
                    if "NIL" in resolvents:
                        return True, clause1, clause2, None, None
                    new.update(resolvents) 
                    # remove_redundant_clauses(new)
        new = remove_redundant_clauses(new - sos)
        if not new:
            return False, None, None, None, None

        sos.update(new)
        
def addition(clause,clauses):
    if clause not in clauses:
        clauses[clause] = max(clauses.values())+1
    print(f"Added {clause}")
    return clauses

def subtraction(clause,clauses):
    line_num = None
    if clause in clauses:
        line_num = clauses[clause]
        del clauses[clause]
        for cl,line_no in clauses.items():
            if line_no > line_num:
                clauses[cl] = line_no-1
    print(f"Removed {clause}")
    return clauses

def inquiry(clause,clauses):
    clause_dict= {
        negate(clause) :  max(clauses.values())
    }
    return resolution(clauses, clause_dict, max(clauses.values()))

def cooking(path_to_clause_file,path_to_user_commands_file):
   clauses, target_clause_negated, line_number,target_clause = parse_clause_file(path_to_clause_file)
   file = open(path_to_user_commands_file, 'r')
   clauses[target_clause] = line_number
   
   print("Constructed with knowledge:")
   for clause in clauses:
       print(' v '.join(clause))
   print()
    
   while True:
        line = file.readline()
        if not line:
           break
        print(f"User's command : {line.strip()}") 
        line_elements = line.strip().split(" ")
        line_tuple = tuple(sorted(element.lower() for element in line_elements if element.lower() != "v"))
        if line_tuple[0] == '+':
            clauses = addition(line_tuple[1:],clauses)
        elif line_tuple[0] == '-':
            clauses = subtraction(line_tuple[1:],clauses)
        elif line_tuple[0] == '?':
            found, _, _, _, _ = inquiry(line_tuple[1:],clauses)
            target_clause_f = ""
            i = 0 
            for el in (line_tuple[1],):
                if i == 0:
                    target_clause_f = target_clause_f + str(el)
                    i+=1
                else:
                    target_clause_f+=" v " + str(el)
            if found:
                print(f"[CONCLUSION]: {target_clause_f} is true")
            else:
                print(f"[CONCLUSION]: {target_clause_f} is unknown")     
                
def resolute(path_to_clause_file):
   clauses,target_clause_negated,line_num,target_clause = parse_clause_file(path_to_clause_file)
   found, _ , _, _, _ =  resolution(clauses,target_clause_negated,line_num,verbose=True)
   target_clause_f = ""
   i = 0 
   for el in target_clause:
      if i == 0:
         target_clause_f = target_clause_f + str(el)
         i+=1
      else:
         target_clause_f+=" v " + str(el)
   if found:
      print(f"[CONCLUSION]: {target_clause_f} is true")
   else:
      print(f"[CONCLUSION]: {target_clause_f} is unknown")
      
def main():
   args = parse_command_line()
   if args.task=='resolution':
      resolute(args.path_to_clause_file)
   elif args.task=='cooking':
      cooking(args.path_to_clause_file,args.path_to_user_commands_file)
   
if __name__ == '__main__':
   main()