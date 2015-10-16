class CNF:
  clauses = []

  def __init__(self, clauses, num_clauses, num_variables):
    self.clauses = clauses
    self.num_clauses = num_clauses
    self.num_variables = num_variables