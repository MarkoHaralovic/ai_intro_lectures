def negate(clause):
    return tuple(el.strip("~") if "~" in el else f"~{el}" for el in clause)

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
    # print(f"Clause 1 {clause_1}")
    # print(f"Clause 2 {clause_2}")
    for element in clause1_set:
        complementary_element = element[1:] if element.startswith("~") else f"~{element}"
        # print(f"complementary elemet : {complementary_element}")
        if complementary_element in clause2_set:
            # print(f"Found")
            new_clause = clause1_set.union(clause2_set) - {element, complementary_element}
            if not new_clause: 
               return ("NIL",)
            if tuple(new_clause) not in clauses.keys():
                 resolvents.add(tuple(new_clause))
    # print(resolvents) if len(resolvents) > 0 else None
    return sorted(resolvents, key=len)
 
clauses,target_clause,line_number = parse_clause_file(r'C:\FER\6TH SEMESTER\INTRO_TO_AI\autograder\data\lab2\files\resolution_coffee_noheater.txt')

def resolution(clauses, target_clause, line_num):
    new = set()
    sos = set([negate(target_clause)])   
    while True:
        for clause_1 in sos:
            for clause_2 in clauses.keys():
                # print(f"SOS: {sos},clauses : {clauses.keys()}")
                if clause_1!=clause_2: resolvents = plResolve(clause_1, clause_2,clauses)
                if "NIL" in resolvents: 
                    return True, clause_1, clause_2, None, None,sos
                new.update(resolvents)
            for previous_clause in sos:
                if previous_clause == clause_1:
                    break  
                resolvents = plResolve(clause_1, previous_clause,clauses)
                if "NIL" in resolvents: 
                    return True, clause_1, previous_clause, None, None
                new.update(resolvents)
        if new.issubset(clauses.keys()):
            # print(f"New : {new}")
            # print(f"Sos : {sos}")
            return False, None, None, None, None
        sos.update(new)
        new = set()

found,cl1,cl2,ln1,ln2,state = resolution(clauses,target_clause,line_number)
print(found)
print(cl1)
print(cl2)
print(ln1)
print(ln2)