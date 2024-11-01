# models/lecturer.py

class Lecturer:
    def __init__(self, lecturer_id, name, workload, available_timeslots):
        self.lecturer_id = lecturer_id
        self.name = name
        self.workload = workload
        self.available_timeslots = available_timeslots

    # You can add other methods or properties here if needed
