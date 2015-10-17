class CNF:
  clauses = list()

  def __init__(self, cnf_file):
    with open(cnf_file) as f:
      cnf_content = f.readlines()

    for line in cnf_content:
      if(line[0] == 'c'):
        continue
      if(line[0] == 'p'):
        problem_arguments = line.rstrip().split(" ")
        self.problem_type = problem_arguments[1]
        self.num_variables = int(problem_arguments[2])
        self.num_clauses = problem_arguments[3]
        continue
      self.clauses.append(line.rstrip().split(" "))