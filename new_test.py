from ortools.sat.python import cp_model


def update_solver():
    solver = cp_model.CpSolver()
    solver.parameters.linearization_level = 0
    # Enumerate all solutions
    solver.parameters.enumerate_all_solutions = True


class EmployeeScheduleModel(object):
    def __init__(self, num_employees, num_shifts, num_days):
        self.num_employees = num_employees
        self.num_shifts = num_shifts
        self.num_days = num_days
        self.all_employees = range(self.num_employees)
        self.all_shifts = range(self.num_shifts)
        self.all_days = range(self.num_days)
        self.model = cp_model.CpModel()
        self.shifts = dict()

    def create_variables(self):
        """
        assignments for shifts to employees are defined as:
        shifts[(n, d, s)] = 1 if shift s is assigned to employee n, on day d; else 0
        """
        for n in self.all_employees:
            for d in self.all_days:
                for s in self.all_shifts:
                    self.shifts[(n, d, s)] = self.model.NewBoolVar(
                        name=f"shift_{n}_{d}_{s}")

    def assign_employees_to_shifts(self):
        """
        To assign employees to shifts, subject to the following constraints:
            - each shift is assigned to a single employee per day
            - each employee works at most one shift per day
        """
        for day in self.all_days:
            for shift in self.all_shifts:
                # for each shift, the sum of employees assigned to that shift = 1
                self.model.Add(
                    sum(self.shifts[(e, day, shift)] for e in self.all_employees) == 1)

        for e in self.all_employees:
            for day in self.all_days:
                # each employee works at most one shift per day
                self.model.Add(
                    sum(self.shifts[(e, day, shift)] for shift in self.all_shifts) <= 1)

    def assign_shifts_evenly(self):
        """
        try to distribute the shifts evenly, so that each employee works
        min_shifts_per_employee shifts. If not possible (total number of shifts is not
        divisible by number of employees), some employees will be assigned an extra shift.
        """
        total_shifts = self.num_shifts * self.num_days
        min_shifts_per_employee = total_shifts // self.num_employees
        if total_shifts % self.num_employees == 0:
            max_shifts_per_employee = min_shifts_per_employee
        else:
            max_shifts_per_employee = min_shifts_per_employee + 1
        for e in self.all_employees:
            num_shifts_worked = list()
            for day in self.all_days:
                for shift in self.all_shifts:
                    num_shifts_worked.append(self.shifts[(e, day, shift)])
            # ensures that each employee is assigned at least the minimum number of
            # shifts per employee
            self.model.Add(min_shifts_per_employee <= sum(num_shifts_worked))
            # ensures that no employee is assigned more than one extra shift
            self.model.Add(max_shifts_per_employee >= sum(num_shifts_worked))
