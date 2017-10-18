import brickpi
import time
import json

class Robot:
	def __init__(self, interface, config_file="config.json"):
		self.motors = [0,1]
		self.motorParams = {}
		self.interface = interface
		self.left_speed = 0
		self.right_speed = 0

		#Enabling the motors
		self.interface.motorEnable(self.motors[0])
		self.interface.motorEnable(self.motors[1])

		#Open the config file
		data = None
    	with open(config_file) as data_file:
    		data = json.load(data_file)

		#Configuring the left motor
		self.motorParams["left"] = self.interface.MotorAngleControllerParameters()
		self.motorParams["left"].maxRotationAcceleration = data["left"]["maxRotationAcceleration"]
		self.motorParams["left"].maxRotationSpeed = data["left"]["maxRotationSpeed"]
		self.motorParams["left"].feedForwardGain = data["left"]["feedForwardGain"]
		self.motorParams["left"].minPWM = data["left"]["minPWM"]
		self.motorParams["left"].pidParameters.minOutput = data["left"]["minOutput"]
		self.motorParams["left"].pidParameters.maxOutput = data["left"]["maxOutput"]
		self.motorParams["left"].pidParameters.k_p = data["left"]["k_p"]
		self.motorParams["left"].pidParameters.k_i = data["left"]["k_i"]
		self.motorParams["left"].pidParameters.k_d = data["left"]["k_d"]

		#Configure the right motor
		self.motorParams["right"] = self.interface.MotorAngleControllerParameters()
		self.motorParams["right"].maxRotationAcceleration = data["right"]["maxRotationAcceleration"]
		self.motorParams["right"].maxRotationSpeed = data["right"]["maxRotationSpeed"]
		self.motorParams["right"].feedForwardGain = data["right"]["feedForwardGain"]
		self.motorParams["right"].minPWM = data["right"]["minPWM"]
		self.motorParams["right"].pidParameters.minOutput = data["right"]["minOutput"]
		self.motorParams["right"].pidParameters.maxOutput = data["right"]["maxOutput"]
		self.motorParams["right"].pidParameters.k_p = data["right"]["k_p"]
		self.motorParams["right"].pidParameters.k_i = data["right"]["k_i"]
		self.motorParams["right"].pidParameters.k_d = data["right"]["k_d"]

		self.interface.setMotorAngleControllerParameters(self.motors[0],self.motorParams["left"])
		self.interface.setMotorAngleControllerParameters(self.motors[1],self.motorParams["right"])

		self.interface.setMotorRotationSpeedReferences(self.motors,[self.left_speed,self.right_speed])

	#Takes the distance in centimeters and moves it forward

	def __moveWheel(self,motor, speed, delta):
		start = time.time()
		duration = 0
		while delta<duration:
			if motor == 0:
				self.interface.setMotorRotationSpeedReferences(1,self.right_speed)
				self.left_speed = speed
			else:
				self.interface.setMotorRotationSpeedReferences(0,self.left_speed)
				self.right_speed = speed
			duration = start-time.time()


	def forward(self,distance, speed = None, delta = None):
		pass


	#Takes the distance in centimeters and moves it backwards
	def backward(self, distance):
		pass

	#Takes the angle in degrees and rotates the robot right
	def rotateRight(self, angle):
		pass

	#Takes the angle in degrees and rotates the robot left
	def rotateLeft(self, angle):
		pass

	def calibrate(self, angle):
		#So that we always start calibrating approximately at zero
		motorAngles = self.interface.getMotorAngles(self.motors)
		motorAngles_zero = (round(0-motorAngles[0][0],2), round(0-motorAngles[0][1],2))
		self.interface.increaseMotorAngleReferences(self.motors,[motorAngles_zero[0],motorAngles_zero[1]])
		while not self.interface.motorAngleReferencesReached(self.motors):
			motorAngles = self.interface.getMotorAngles(self.motors)
			print "Motor angles calibrating to 0: ", motorAngles[0][0], ", ", motorAngles[1][0]
			time.sleep(0.1)

		self.interface.increaseMotorAngleReferences(self.motors,[angle,angle])
    	while not self.interface.motorAngleReferencesReached(self.motors):
			motorAngles = self.interface.getMotorAngles(self.motors)
			if motorAngles:
		    	print "Motor angles: ", motorAngles[0][0], ", ", motorAngles[1][0]
			time.sleep(0.1)