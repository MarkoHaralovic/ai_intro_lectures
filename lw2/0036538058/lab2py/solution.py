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
      line_tuple = tuple(element.lower() for element in line_elements if element!="v")   
      clauses[line_tuple] = line_number
      target_clause = line_tuple
   return clauses,target_clause,line_number

def plResolve(clause_1, clause_2):
    clause1_set = set(clause_1)
    clause2_set = set(clause_2)
    resolvents = set()

    for element in clause1_set:
        complementary_element = element[1:] if element.startswith("~") else f"~{element}"
        if complementary_element in clause2_set:
            new_clause = clause1_set.union(clause2_set) - {element, complementary_element}
            if not new_clause: 
               return "NIL"
            resolvents.add(tuple(sorted(new_clause)))
   #  print(resolvents) if len(resolvents) > 0 else None
    return sorted(resolvents, key=len)


def selectClauses(clauses,new,line_num=None):
   if len(new)==0:
      clause_list = list(clauses.items()) 
      #https://www.geeksforgeeks.org/python-itertools-combinations-function/
      clause_pairs_with_lines = []
      for (clause1, line1), (clause2, line2) in itertools.combinations(clause_list, 2):
         clause_pairs_with_lines.append(((clause1, clause2), (line1, line2)))
      # for oho in clause_pairs_with_lines:
      #    print(oho)
         # print(clause_pairs_with_lines)
      return clause_pairs_with_lines
   else:
      # print(new)
      clause_list = list(clauses.items()) 
      # print("----------")
      # print(clause_list)
      # print("----------")
      clause_pairs_with_lines = []
      for (clause1, line1) in clause_list:
         for clause2 in new:
            if clause1!=clause2:
               clause_pairs_with_lines.append(((clause1, clause2), (line1,line_num)))
      # for oho in clause_pairs_with_lines:
      #    print(oho)
      # import sys
      # sys.exit(1)
      return clause_pairs_with_lines


def resolution(clauses,target_clause,line_num):
   # for k,v in clauses.items():
   #    print(k,v)
   new = set()
   sos = set(target_clause)
   clause_combs = selectClauses(clauses,sos,line_num)
   while True:
      # print(clause_combs)
      for (clause_1,clause_2),lines in clause_combs:
         resolvents = plResolve(clause_1,clause_2)
         if "NIL" in resolvents: return True, clause_1,clause_2,clauses[clause_1],clauses[clause_2]
         new.update(resolvents)
         sos.update(resolvents)
      if new.issubset(clauses.keys()):return False ,None,None,None,None
      for res in new:
            if res not in clauses.keys():
                clauses[res] = line_num
                line_num+=1 
      new = set()
      clause_combs = selectClauses(clauses,new,line_num)
      # for k in clause_combs:
      #    print(k)
      # break 
   
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
            target_clause_f+=" v " + str(el)
      if found:
         print(f"[CONCLUSION]: {target_clause_f} is true")
      else:
         print(f"[CONCLUSION]: {target_clause_f} is unknown")
      # print(found)
      # print(cl1,cl2,ln1,ln2)
   elif args.task=='cooking':
      cooking(args.path_to_clause_file,args.path_to_user_commands_file)
   
if __name__ == '__main__':
   main()