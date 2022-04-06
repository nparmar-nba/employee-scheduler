import EmployeeScheduleModel as scheduler


def prepare_model(params: dict):
    scheduler_model = scheduler.EmployeeScheduleModel(**params)
    scheduler_model.create_variables()
    scheduler_model.assign_employees_to_shifts()
    scheduler_model.assign_shifts_evenly()
    scheduler_model.update_solver_params()
    return scheduler_model


def print_stats(_solver, solution_count):
    print(f"\nScheduling Statistics\n{'-'*35}")
    print(f"{'-' * 4}> number of conflicts: {_solver.NumConflicts()}")
    print(f"{'-' * 4}> number of branches: {_solver.NumBranches()}")
    print(f"{'-' * 4}> wall time: {round(_solver.WallTime(), 6)} sec")
    print(f"{'-' * 4}> number of solutions found: {solution_count}")


def schedule_employees_simple(params: dict):
    _model = prepare_model(params)
    solution_record = _model.register_solutions_callback()

    # Invoke the solver:
    _model.solver.Solve(_model.model, solution_record)
    print_stats(_model.solver, solution_record.solution_count)


def schedule_employees_requests(params: dict):
    _model = prepare_model(params)
    solution_record = _model.register_solutions_callback()

    # Invoke the solver:
    _model.solver.Solve(_model.model, solution_record)
    print_stats(_model.solver, solution_record.solution_count)


def main():
    model_params = {
        "num_employees": 4,
        "num_shifts": 3,
        "num_days": 3
    }
    schedule_employees_simple(model_params)


if __name__ == "__main__":
    main()
