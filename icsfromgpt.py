from ics import Calendar, Event
from datetime import datetime, timedelta


# Function to create an event in the calendar
def create_event(calendar, summary, start_time, duration_minutes, location=None):
	event = Event()
	event.name = summary
	event.begin = start_time
	event.duration = timedelta(minutes=duration_minutes)
	if location:
		event.location = location
	calendar.events.add(event)


# Initialize the calendar
calendar = Calendar()

# Starting date
start_date = datetime(2025, 1, 13)

# Define the weekly schedule with days and times
schedule = {
	'Sunday': [
			('Wakeup/Workout/Shower', '9:00 AM', 90),
			('Work', '10:30 AM', 120),
			('Lunch Break', '12:30 PM', 60),
			('Study (MATH-308-507)', '1:30 PM', 120),
			('Study (AERO-212-500)', '3:30 PM', 120),
			('Study (MATH-304-510)', '8:30 PM', 120),
			('Wind-down', '10:30 PM', 45),
	],
	'Monday': [
		('Wakeup/Workout/Shower', '7:30 AM', 90),
		('AERO-214-506 (Class)', '11:30 AM', 120),
		('MATH-304-510 (Class)', '1:50 PM', 50),
		('Lunch Break', '2:40 PM', 60),
		('AERO-212-500 (Class)', '4:10 PM', 75),
		('Work', '5:30 PM', 120),
		('Study (AERO-214-506)', '7:30 PM', 120),
		('Wind-down', '10:30 PM', 45),
	],
	'Tuesday': [
		('Wakeup/Workout/Shower', '6:45 AM', 75),
		('AERO-222-502 (Class)', '8:00 AM', 75),
		('Lunch Break', '9:15 AM', 30),
		('Work (Walker Meeting)', '9:30 AM', 150),
		('AERO-214-506 (Class)', '12:45 PM', 75),
		('MATH-308-507 (Class)', '2:20 PM', 75),
		('AERO-212-500 (Class)', '5:30 PM', 50),
		('Study (AERO-222-502)', '6:20 PM', 120),
		('Wind-down', '10:30 PM', 45),
	],
	'Wednesday': [
		('Wakeup/Workout/Shower', '7:30 AM', 90),
		('Work', '9:00 AM', 180),
		('MATH-304-510 (Class)', '1:50 PM', 50),
		('Lunch Break', '2:40 PM', 60),
		('AERO-212-500 (Class)', '4:10 PM', 75),
		('Study (MATH-304-510)', '5:30 PM', 120),
		('Wind-down', '10:30 PM', 45),
	],
	'Thursday': [
		('Wakeup/Workout/Shower', '6:45 AM', 75),
		('AERO-222-502 (Class)', '8:00 AM', 75),
		('Lunch Break', '9:15 AM', 30),
		('AERO-214-506 (Class)', '12:45 PM', 75),
		('MATH-308-507 (Class)', '2:20 PM', 75),
		('Work', '3:40 PM', 120),
		('Study (AERO-222-502)', '5:40 PM', 120),
		('Study (AERO-212-500)', '7:40 PM', 120),
		('Wind-down', '10:30 PM', 45),
	],
	'Friday': [
		('Wakeup/Workout/Shower', '6:45 AM', 75),
		('AERO-222-502 (Class)', '8:00 AM', 100),
		('Lunch Break', '9:40 AM', 30),
		('MATH-304-510 (Class)', '1:50 PM', 50),
		('Study (MATH-304-510)', '2:40 PM', 80),
		('Study (AERO-212-500)', '4:00 PM', 120),
		('Wind-down', '11:00 PM', 120),
	],
	'Saturday': [
		('Wakeup/Workout/Shower', '9:00 AM', 90),
		('Work', '10:30 AM', 120),
		('Lunch Break', '12:30 PM', 60),
		('Study (MATH-308-507)', '1:30 PM', 120),
		('Study (AERO-212-500)', '3:30 PM', 120),
		('Study (AERO-214-506)', '9:30 PM', 90),
		('Wind-down', '11:00 PM', 120),
	]
}

# Add events to the calendar for each day of the week
for day, activities in schedule.items():
	for activity, start_str, duration in activities:
		start_time = datetime.strptime(start_str, '%I:%M %p').replace(year=2025, month=1, day=12) + timedelta(
			days=list(schedule.keys()).index(day))

		# Apply the 6-hour offset
		start_time += timedelta(hours=6)

		create_event(calendar, activity, start_time, duration)

# Save the calendar to an ICS file
with open('schedule_with_offset.ics', 'w') as f:
	f.writelines(calendar)
