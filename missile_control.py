import math


class Missile(object):
	"""docstring for Missile"""
	def __init__(self):
		super(Missile, self).__init__()
		self.g = 9.81
		self.theta = 0 
		self.up_shifts = {}
		self.has_been_launched = False
	
	def pre_launch(function):
		def wrapper(self, *args):
			if self.has_been_launched:
				raise LaunchException("This operation cannot be performed after launch")
			function(self, *args)
		return wrapper

	@pre_launch
	def set_initial_position(self, x, y):
		self.x0 = x
		self.y0 = y 

	@pre_launch
	def increase_angle(self, degree):
		self.theta = (degree+self.theta)%360

	@pre_launch
	def launch(self, velocity):
		self._pre_launch_check()
		self.has_been_started = True
		self.v0 = velocity
		self.v0x = self.v0*math.cos(self.theta*math.pi/180)
		self.v0y = self.v0*math.sin(self.theta*math.pi/180)
	
	def _pre_launch_check(self):
		required_attributes = ['y0','x0']
		for attribute in required_attributes:
			if not hasattr(self, attribute):
				raise LaunchException("Missile has not been initialized")
		if self.theta >=180:
			raise LaunchException("Launch angle greater than or equal to 180 is not supported")
		if self.theta == 0:
			raise LaunchException("Launch angle equal to 0 is not supported")
		if self.y0 <0:
			raise LaunchException("Negative y-coordinate is not supported")

	@pre_launch		
	def shift_up(self, distance, time):
		self.up_shifts[time]=distance 
	
	def apply_upshifts_and_get_range(self):
		up_shift_timestamps = sorted(self.up_shifts.keys())
		time_elapsed = 0
		py_coordinate_at_timestamp = y_coordinate = self.y0
		for timestamp in up_shift_timestamps:
			vy = self.v0y - self.g * time_elapsed
			flight_time = timestamp - time_elapsed
			y_coordinate_at_timestamp = vy * flight_time + 0.5 * - self.g * flight_time**2 + y_coordinate
			if y_coordinate_at_timestamp<0:
				break
			time_elapsed = timestamp 
			y_coordinate = y_coordinate_at_timestamp + self.up_shifts[timestamp]
		vy = self.v0y - self.g * time_elapsed
		flight_range = self.v0x * (time_elapsed + (vy + math.sqrt(vy**2 + 2*self.g*y_coordinate))/self.g)
		return flight_range
	
	def get_range(self):
		if self.y0:
			flight_range = self.v0x * (self.v0y + math.sqrt(self.v0y**2 + 2*self.g*self.y0))/self.g
		else:
			flight_range = 2 * self.v0x * self.v0y / self.g
		return flight_range

	def get_landing_position(self):
		if self.up_shifts:
			flight_range = self.apply_upshifts_and_get_range()
		else:
			flight_range = self.get_range()
		return (round(self.x0+flight_range,2),0.0)


class IncorrectFormatException(Exception):
	pass

class LaunchException(Exception):
	pass



missile = Missile()
print "Enter 'q' to quit"

while True:
	com = raw_input('Command:').split()
   	if len(com) == 0:
   		break
   	if com[0] == 'q':
		break
	if com[0] == 'MISSILE': # Missile init
		try:
			if len(com)!=4:
				raise IncorrectFormatException
			try:
				x_coordinate = int(com[2].replace(',',''))
				y_coordinate = int(com[3])
			except:
				raise IncorrectFormatException
			missile.set_initial_position(x_coordinate,y_coordinate)
			print "Success"
		except IncorrectFormatException:
			print "Incorrect format detected"
			print "Correct format : MISSILE INIT (x-coordinate), (y-coordinate)"
			print "Example : MISSILE INIT 0, 0"
		except LaunchException as e:
			print str(e)
	elif com[0] == 'DEGREE': # DEGREE
		try:
			if len(com)!=2:
				raise IncorrectFormatException
			degree = int(com[1])
			missile.increase_angle(degree)
			print "Success"
		except IncorrectFormatException:
			print "Incorrect format detected"
			print "Correct format : DEGREE (sign)(magnitude)"
			print "Example : DEGREE +45"
		except LaunchException as e:
			print str(e)
	elif com[0] == 'LAUNCH':
		try:
			if len(com)!=2:
				raise IncorrectFormatException
			initial_velocity = int(com[1])
			if initial_velocity<0:
				raise IncorrectFormatException
			missile.launch(initial_velocity)
			print "Success"
		except IncorrectFormatException:
			print "Incorrect format detected"
			print "Correct format : LAUNCH (initial_velocity)"
			print "Example : LAUNCH 45"
		except LaunchException as e:
			print str(e)
	elif com[0] == 'UP':
		try:
			if len(com)!=3:
				raise IncorrectFormatException
			timestamp = int(com[2])
			shift_distance = int(com[1])
			missile.shift_up(shift_distance,timestamp)
			print "Success"
		except IncorrectFormatException:
			print "Incorrect format detected"
			print "Correct format : UP (shift_distance) (timestamp)"
			print "Example : UP 5 45"
		except LaunchException as e:
			print str(e)
	elif com[0] == 'LANDING_POSITION':
		print missile.get_landing_position()
		break



