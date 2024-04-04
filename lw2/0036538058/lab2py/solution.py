import sys
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
   while True:
      line = file.readline()
      if not line:
         file.close()
         break
      if line.startswith("#"):continue
      line_number+=1
      line_elements = line.strip().split(" ")
      line_tuple = tuple(element.lower() for element in line_elements if element.lower()!="v")   
      clauses[line_tuple] = line_number
      target_clause = line_tuple
   del clauses[target_clause]
   return clauses,target_clause,line_number

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
            if tuple(new_clause) not in clauses.keys():
                 resolvents.add(tuple(new_clause))
   #  print(resolvents) if len(resolvents) > 0 else None
    return sorted(resolvents, key=len)

def resolution(clauses, target_clause, line_num):
    new = set()
    
    sos = set([negate(target_clause)])   
    while True:
        for clause_1 in sos:
            for clause_2 in clauses.keys():
                if clause_1!=clause_2: resolvents = plResolve(clause_1, clause_2,clauses)
                if "NIL" in resolvents: 
                    return True, clause_1, clause_2, None, None
                new.update(resolvents)
            for previous_clause in sos:
                if previous_clause == clause_1:
                    break  
                resolvents = plResolve(clause_1, previous_clause,clauses)
                if "NIL" in resolvents: 
                    return True, clause_1, previous_clause, None, None
                new.update(resolvents)
        if new.issubset(clauses.keys()):
            return False, None, None, None, None
        sos.update(new)
        new = set()

def cooking(path_to_clause_file,path_to_user_commands_file):
   pass

def main():
   args = parse_command_line()
   if args.task=='resolution':
      clauses,target_clause,line_num = parse_clause_file(args.path_to_clause_file)
      found,cl1,cl2,ln1,ln2 = resolution(clauses,target_clause,line_num)
      target_clause_f = ""
      i = 0 
      for el in target_clause:
         if i == 0:
            target_clause_f = target_clause_f + str(el)
            i+=1
         else:
            target_clause_f+=" " + str(el)
      if found:
         print(f"[CONCLUSION]: {target_clause_f} is true")
      else:
         print(f"[CONCLUSION]: {target_clause_f} is unknown")
   elif args.task=='cooking':
      cooking(args.path_to_clause_file,args.path_to_user_commands_file)
   
if __name__ == '__main__':
   main()