from ortools.sat.python import cp_model


class EmployeeSchedulerSolutionCallback(cp_model.CpSolverSolutionCallback):
    def __init__(self, shifts, num_employees, num_days, num_shifts, limit):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.shifts = shifts
        self.num_employees = num_employees
        self.num_days = num_days
        self.num_shifts = num_shifts
        self.solution_limit = limit
        self.solution_count = 0

    def on_solution_callback(self):
        self.solution_count += 1
        print(f"Solution {self.solution_count}")
        for d in range(self.num_days):
            print(f"Day: {d+1}")
            for n in range(self.num_employees):
                is_working = False
                for s in range(self.num_shifts):
                    if self.Value(self.shifts[(n, d, s)]):
                        is_working = True
                        print(f"\tEmployee {n+1} works shift {s+1}")
                if not is_working:
                    print(f"\tEmployee {n+1} does not work")
        if self.solution_count >= self.solution_limit:
            print(f"Stopping search after {self.solution_limit} solutions")
            self.StopSearch()

    def solution_count(self):
        return self.solution_count
