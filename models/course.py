class Course:
    def __init__(self, course_code, lecturer, student_groups, duration, timeslot, title=None, course_name=None):
        self.course_code = course_code
        self.course_name = title if title else course_name  # Allow title as an alias
        self.lecturer = lecturer
        self.student_groups = student_groups
        self.duration = duration
        self.timeslot = timeslot
