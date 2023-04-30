#!/bin/python

import time
import serial
from commands import *

def xread_packet(ser):
	return

def read_packet(ser):
	state = 'START'
	next_state = 'START'
	done = False
	pbuf = bytearray()
	while not done:
		if state == 'START':     
			while ser.inWaiting() == 0:
				pass
			temp = ser.read(1)
			if temp == b'\x44':
				next_state = 'GOT44'
		elif state == 'GOT44':
			while ser.inWaiting() == 0:
				pass
			temp = ser.read(1)
			if temp == b'\x4b':
				next_state = 'FOUND_PACKET'
			elif temp == b'\x44':
				next_state = 'GOT44'
			else:
				next_state = 'START'
		elif state == 'FOUND_PACKET':
			while ser.inWaiting() == 0:
				pass
			temp = ser.read(1)  # low byte of length
			
			# Construct what we have so far
			pbuf = bytearray()  # clear buffer
			pbuf += b'\x44'
			pbuf += b'\x4b'
			pbuf += temp

			# Read the rest of the packet
			len = int.from_bytes(temp, "little")
			pbuf += ser.read(len - 3)

			next_state = 'DONE'
		elif state == 'DONE':
			done = True
		state = next_state
		#time.sleep(.1)

	return(pbuf)

