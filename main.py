from models.course import Course
from models.lecturer import Lecturer
from models.room import Room
from models.student_group import StudentGroup
from models.timetable_slot import TimetableSlot
import json
import csv

def load_input_data(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def extract_start_time(timeslot):
    """Extract the start time from the timeslot string."""
    return timeslot.split("-")[0]

def check_constraints(course, lecturer, room, student_group):
    # Check room capacity constraint
    if student_group.students > room.capacity:
        print(f"Room {room.room_id} capacity exceeded for group {student_group.group_id} ({student_group.students} students, capacity: {room.capacity}).")
        return False  # Room capacity exceeded

    # Check lecturer daily workload
    if lecturer.workload + course.duration > 6:
        print(f"Lecturer {lecturer.name}'s workload exceeds limit with new course {course.course_name} (current: {lecturer.workload}, adding: {course.duration}).")
        return False  # Exceeds lecturer daily workload

    # Check if the room and lecturer are available for the course's timeslot
    if course.timeslot not in room.available_timeslots:
        print(f"Room {room.room_id} not available for course {course.course_name} at {course.timeslot}. Available: {room.available_timeslots}.")
        return False

    if course.timeslot not in lecturer.available_timeslots:
        print(f"Lecturer {lecturer.name} not available for course {course.course_name} at {course.timeslot}. Available: {lecturer.available_timeslots}.")
        return False

    return True

def schedule_course(course, lecturers, rooms, student_groups, timetable):
    for group_id in course.student_groups:
        group_info = next((g for g in student_groups if g.group_id == group_id), None)
        if group_info:
            for room in rooms:
                if check_constraints(course, next(l for l in lecturers if l.name == course.lecturer), room, group_info):
                    print(f"Scheduling {course.course_name} for {group_id} in {room.room_id}.")
                    start_time = extract_start_time(course.timeslot)
                    end_time = course.timeslot.split("-")[1]

                    slot = TimetableSlot(
                        course=course,
                        lecturer=next(l for l in lecturers if l.name == course.lecturer),
                        room=room,
                        start_time=start_time,
                        end_time=end_time
                    )
                    timetable.append(slot)
                    # Update the lecturer's workload
                    next(l for l in lecturers if l.name == course.lecturer).workload += course.duration
                    # Remove the used timeslot from availability
                    room.available_timeslots.remove(course.timeslot)
                    next(l for l in lecturers if l.name == course.lecturer).available_timeslots.remove(course.timeslot)
                    print(f"Scheduled {course.course_name} for {group_id} in {room.room_id} from {start_time} to {end_time}.")
                    return True  # Successfully scheduled
    print(f"Failed to schedule {course.course_name} due to constraints.")
    return False  # Failed to schedule

def generate_timetable(courses, lecturers, rooms, student_groups):
    timetable = []  # Initialize an empty timetable list
    
    # Example scheduling logic (this should be replaced with your actual scheduling logic)
    for course in courses:
        for lecturer in lecturers:
            # Here you would implement your scheduling logic
            # For simplicity, we are using placeholder values for room and times
            timetable.append({
                'course': course.course_code,
                'lecturer': lecturer.name,
                'room': "Room 101",  # Replace with actual room assignment logic
                'start_time': course.timeslot.split('-')[0].strip(),
                'end_time': course.timeslot.split('-')[1].strip(),
            })
    
    return timetable



import csv

def save_timetable_to_csv(timetable, filename='output/timetable.csv'):
    # Create output directory if it doesn't exist
    import os
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Write the timetable to a CSV file
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write the headers
        writer.writerow(['Course', 'Lecturer', 'Room', 'Start Time', 'End Time'])
        
        # Write the course data
        for entry in timetable:
            writer.writerow([
                entry['course'],
                entry['lecturer'],
                entry['room'],
                entry['start_time'],
                entry['end_time']
            ])

    print("Timetable generated and saved to output/timetable.csv")

def main():
    input_data = load_input_data('input_data/input.json')

    # Initialize data structures
    courses = [
        Course(course_code="CS101", title="Introduction to Programming", lecturer="Dr. Smith", student_groups=["Group A", "Group B"], duration=2, timeslot="Monday 9:00-11:00"),
        Course(course_code="CS201", title="Data Structures", lecturer="Dr. Johnson", student_groups=["Group A"], duration=3, timeslot="Monday 11:00-14:00"),
        Course(course_code="MATH101", title="Calculus I", lecturer="Prof. Adams", student_groups=["Group B"], duration=1, timeslot="Tuesday 9:00-10:00")
    ]

    lecturers = [
        Lecturer(lecturer_id="1", name="Dr. Smith", workload=40, available_timeslots=["Monday 9:00-11:00", "Wednesday 9:00-11:00"]),
        Lecturer(lecturer_id="2", name="Dr. Johnson", workload=40, available_timeslots=["Monday 11:00-14:00", "Thursday 10:00-13:00"]),
        Lecturer(lecturer_id="3", name="Prof. Adams", workload=40, available_timeslots=["Tuesday 9:00-10:00", "Thursday 9:00-10:00"])
    ]

    # Initialize rooms list
    rooms = [
        Room(room_id="Room 101", capacity=50, available_timeslots=["Monday 9:00-11:00"]),
        Room(room_id="Room 102", capacity=50, available_timeslots=["Monday 11:00-14:00"]),
        Room(room_id="Room 103", capacity=50, available_timeslots=["Tuesday 9:00-10:00"])
    ]

    # Convert input data to objects
    courses.extend([Course(**course) for course in input_data['courses']])
    lecturers.extend([Lecturer(**lecturer) for lecturer in input_data['lecturers']])
    rooms.extend([Room(**room) for room in input_data['rooms']])
    student_groups = [
        StudentGroup("Group A", students=40, courses=["CS101", "CS201"]),
        StudentGroup("Group B", students=35, courses=["CS101", "MATH101"])
    ]
    student_groups.extend([StudentGroup(**group) for group in input_data['student_groups']])
    
    timetable = generate_timetable(courses, lecturers, rooms, student_groups)
    save_timetable_to_csv(timetable) 

if __name__ == '__main__':
    main()
