#!/usr/bin/env python3

import rospy
import numpy
import time
import serial
from commands import *
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist
from read_packet import *

def initRevHub():
	#Initialization section
	msg = COMMAND_DISCOVERY()
	ser.write(msg)
	pbuf = read_packet(ser)

	for i in range (4):
		msg = LynxSetMotorChannelModeCommand(i, 'RUN_WITHOUT_ENCODER', True)
		ser.write(msg)
		pbuf = read_packet(ser)

		msg = LynxSetMotorConstantPowerCommand(i, 0.0)
		ser.write(msg)
		pbuf = read_packet(ser)


	for i in range (6):
		msg = LynxSetServoConfigurationCommand(i, 20000)
		ser.write(msg)
		pbuf = read_packet(ser)

	msg = COMMAND_GET_MODULE_STATUS()
	ser.write(msg)
	pbuf = read_packet(ser)

	for i in range(4):
		msg = LynxSetMotorChannelEnableCommand(i, True)
		ser.write(msg)
		pbuf = read_packet(ser)

	for i in range(6):
		msg = LynxSetServoEnableCommand(i, True)
		ser.write(msg)
		pbuf = read_packet(ser)

	for i in range (4):
		msg = LynxResetMotorEncoderCommand(i)
		ser.write(msg)
		buf = read_packet(ser)

	for i in range (8):
		msg = LynxSetDIODirectionCommand(i, 0)
		ser.write(msg)
		pbuf = read_packet(ser)

	for i in range (4):
		msg = LynxSetMotorTargetPositionCommand(i, 0, 5)  # check if zero would be better
		ser.write(msg)
		pbuf = read_packet(ser)

	for i in range (4):
		msg = LynxSetMotorTargetVelocityCommand(i, 0)
		ser.write(msg)
		pbuf = read_packet(ser)

	for i in range (4):
		msg = LynxSetServoPulseWidthCommand(i, 1500)
		ser.write(msg)
		pbuf = read_packet(ser)
		

	#rospy.loginfo("servo 2: " + str(data))

def thrusterAngle1Callback(data):
	angle_radians = math.radians(data.data)
	if (angle_radians < 0.0):
		angle_radians = angle_radians+(math.pi*2)
	w = 2 * 288/360 * angle_radians
	msg = LynxSetMotorTargetPositionCommand(0, int(w), 5)
	ser.write(msg)
	msg = LynxSetMotorTargetVelocityCommand(0, 2000)
	ser.write(msg)
	rospy.loginfo("motor angle 0: " + str(w))

def thrusterAngle2Callback(data):
	angle_radians = math.radians(data.data)
	if (angle_radians < 0.0):
		angle_radians = angle_radians+(math.pi*2)
	w = 2 * 288/360 * angle_radians
	msg = LynxSetMotorTargetPositionCommand(1, int(w), 5)
	ser.write(msg)
	msg = LynxSetMotorTargetVelocityCommand(1, 2000)
	ser.write(msg)
	rospy.loginfo("motor angle 1: " + str(w))

def thrusterAngle3Callback(data):
	angle_radians = math.radians(data.data)
	if (angle_radians < 0.0):
		angle_radians = angle_radians+(math.pi*2)
	w = 2 * 288/360 * angle_radians
	msg = LynxSetMotorTargetPositionCommand(2, int(w), 5)
	ser.write(msg)
	msg = LynxSetMotorTargetVelocityCommand(2, 2000)
	ser.write(msg)
	rospy.loginfo("motor angle 2: " + str(w))	

def turretAngle4Callback(data):
	msg = LynxSetServoPulseWidthCommand(0, data.data) 
	ser.write(msg)
	rospy.loginfo("motor angle 2: " + data.data)


	   
def main():
	# configure the serial connections (the parameters differs on the device you are connecting to)
	global ser
	ser = serial.Serial(
		port='/dev/ttyUSB1',
		baudrate=460800,
		parity=serial.PARITY_NONE,
		stopbits=serial.STOPBITS_ONE,
		bytesize=serial.EIGHTBITS
	)
	initRevHub()
	print("starting")


	for i in range(4):
		msg = LynxSetMotorChannelModeCommand(i, 'RUN_TO_POSITION', True)
		ser.write(msg)

	rospy.init_node("rev_driver_node", anonymous=False)
	rospy.Subscriber("wdog/thrusters/1_thrust_angle", Float32, thrusterAngle1Callback)
	rospy.Subscriber("wdog/thrusters/2_thrust_angle", Float32, thrusterAngle2Callback)
	rospy.Subscriber("wdog/thrusters/3_thrust_angle", Float32, thrusterAngle3Callback)

	# msg = LynxSetMotorConstantPowerCommand(0, 0.5)
	# ser.write(msg)
	# pbuf = read_packet(ser)

	msg = LynxSetMotorTargetPositionCommand(0, 0, 5)
	ser.write(msg)
	msg = LynxSetMotorTargetVelocityCommand(0, 2000)
	ser.write(msg)

	# msg = LynxI2cWriteMultipleBytesCommand(0, b'\x28', (bytearray(b'\x01\x02', 2)))
	# ser.write(msg.hex)


	r = rospy.Rate(10) # 10Hz
	while not rospy.is_shutdown(): 
		msg = COMMAND_KEEP_ALIVE()
		#print("Send KEEP_ALIVE: " + msg.hex())
		ser.write(msg)
		pbuf = read_packet(ser)

		msg = LynxGetMotorEncoderPositionCommand(0)
		#print("Send LynxGetMotorEncoderPositionCommand: " + msg.hex())
		ser.write(msg)
		pbuf = read_packet(ser)
		#print("Got: " + pbuf.hex())
		payload_format = Struct(
			"count" / Int32ul)
		#x = payload_format.parse(pbuf[11:])
		pos = int.from_bytes(pbuf[10:14], "little")
		#print(pos)

		# # read and kill incoming packets
		# n = ser.inWaiting()
		# if n > 0:
		#	temp = ser.read(n)

		r.sleep()

if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass
