from construct import *
from packet_header_format import (
	message_format_packet_header, message_crc, Container, create_crc)
from enum import Enum
from io import *

message_motor = Struct(
	"motor" / Int8ub,
	"power" / Int16ul,
)

payload_two_bytes = Struct(
	"byte_1" / Int8ub,
	"byte_2" / Int8ub)

################################################################

def LynxSetMotorChannelModeCommand(motor, mode, floatAtZero):
	header = message_format_packet_header.build(dict(
		length=11+3, 
		dest_module=3,
		source_module=0,
		packet_num=0,
		reference_num=0,
		packet_id='LynxSetMotorChannelModeCommand'))

	payload_format = Struct(
	"motor" / Int8ub,
	"mode" / Int8ub,
	"floatAtZero" / Int8ub)

	if mode == 'RUN_WITHOUT_ENCODER':
		my_mode = 0;
	elif mode == 'RUN_USING_ENCODER':
		my_mode = 1;
	elif mode == 'RUN_TO_POSITION':
		my_mode = 2

	if floatAtZero == True:
		my_floatAtZero = 1
	else:
		my_floatAtZero = 0

	payload = payload_format.build(dict(
		motor = motor,
		mode = my_mode,
		floatAtZero = my_floatAtZero))

	cmd_all = header + payload
	msg_crc = message_crc.build(dict(crc=create_crc(cmd_all)))

	return(cmd_all + msg_crc)

################################################################

def LynxSetMotorConstantPowerCommand(motor, power):
	header = message_format_packet_header.build(dict(
		length=14, 
		dest_module=3,
		source_module=0,
		packet_num=0,
		reference_num=0,
		packet_id='LynxSetMotorConstantPowerCommand'))

	int_power = int(power * 32000)
	payload = message_motor.build(dict(
		motor=motor,
		power=int_power))

	cmd_all = header + payload

	msg_crc = message_crc.build(dict(crc=create_crc(cmd_all)))

	return(cmd_all + msg_crc)

################################################################

def LynxSetMotorTargetVelocityCommand(motor, velocity):
	header = message_format_packet_header.build(dict(
		length=11+3,  
		dest_module=3,
		source_module=0,
		packet_num=0,
		reference_num=0,
		packet_id='LynxSetMotorTargetVelocityCommand'))

	payload_format = Struct(
	"motor" / Int8ub,
	"velocity" / Int16sl)	# signed

	payload = payload_format.build(dict(
		motor = motor,
		velocity = velocity))

	cmd_all = header + payload
	msg_crc = message_crc.build(dict(crc=create_crc(cmd_all)))

	return(cmd_all + msg_crc)

	
################################################################

def LynxSetMotorChannelEnableCommand(motor, enable):
	header = message_format_packet_header.build(dict(
		length=13, 
		dest_module=3,
		source_module=0,
		packet_num=0,
		reference_num=0,
		packet_id='LynxSetMotorChannelEnableCommand'))

	payload = payload_two_bytes.build(dict(
		byte_1 = motor,
		byte_2 = enable))

	cmd_all = header + payload
	msg_crc = message_crc.build(dict(crc=create_crc(cmd_all)))

	return(cmd_all + msg_crc)

################################################################

def LynxSetMotorTargetPositionCommand(motor, target, tolerance):
	header = message_format_packet_header.build(dict(
		length=11+7,  
		dest_module=3,
		source_module=0,
		packet_num=0,
		reference_num=0,
		packet_id='LynxSetMotorTargetPositionCommand'))

	payload_format = Struct(
	"motor" / Int8ub,
	"target" / Int32ul,
	"tolerance" / Int16ul)	# unsigned

	payload = payload_format.build(dict(
		motor = motor,
		target = target,
		tolerance = tolerance))

	cmd_all = header + payload
	msg_crc = message_crc.build(dict(crc=create_crc(cmd_all)))

	return(cmd_all + msg_crc)

################################################################

def LynxGetMotorPIDFControlLoopCoefficientsCommand(motor, mode):
	header = message_format_packet_header.build(dict(
		length=11+2,  
		dest_module=3,
		source_module=0,
		packet_num=0,
		reference_num=0,
		packet_id='LynxGetMotorPIDFControlLoopCoefficientsCommand'))

	payload_format = Struct(
	"motor" / Int8ub,
	"mode" / Int8ub)

	if mode == 'RUN_USING_ENCODER':
		my_mode = 1;
	elif mode == 'RUN_TO_POSITION':
		my_mode = 2

	payload = payload_format.build(dict(
		motor = motor,
		mode = my_mode))

	cmd_all = header + payload
	msg_crc = message_crc.build(dict(crc=create_crc(cmd_all)))

	return(cmd_all + msg_crc)

################################################################

def LynxGetMotorEncoderPositionCommand(motor):
	header = message_format_packet_header.build(dict(
		length=11+1,  
		dest_module=3,
		source_module=0,
		packet_num=0,
		reference_num=0,
		packet_id='LynxGetMotorEncoderPositionCommand'))

	payload_format = Struct(
	"motor" / Int8ub)

	payload = payload_format.build(dict(
		motor = motor))

	cmd_all = header + payload
	msg_crc = message_crc.build(dict(crc=create_crc(cmd_all)))

	return(cmd_all + msg_crc)

################################################################
def LynxSetServoEnableCommand(channel, enable):
	header = message_format_packet_header.build(dict(
		length=13,  
		dest_module=3,
		source_module=0,
		packet_num=0,
		reference_num=0,
		packet_id='LynxSetServoEnableCommand'))

	payload = payload_two_bytes.build(dict(
		byte_1 = channel,
		byte_2 = enable))

	cmd_all = header + payload
	msg_crc = message_crc.build(dict(crc=create_crc(cmd_all)))

	return(cmd_all + msg_crc)

################################################################

def LynxSetMotorPIDControlLoopCoefficientsCommand(motor, mode, p, i, d):
	header = message_format_packet_header.build(dict(
		length=11+14, 
		dest_module=3,
		source_module=0,
		packet_num=0,
		reference_num=0,
		packet_id='LynxSetMotorPIDControlLoopCoefficientsCommand'))

	payload_format = Struct(
	"motor" / Int8ub,
	"mode" / Int8ub,
	"p" / Int32ul,
	"i" / Int32ul, 
	"d" / Int32ul)

	if mode == 'RUN_USING_ENCODER':
		my_mode = 1;
	elif mode == 'RUN_TO_POSITION':
		my_mode = 2

	payload = payload_format.build(dict(
		motor = motor,
		mode = my_mode,
		p = p,
		i = i,
		d = d))

	cmd_all = header + payload
	msg_crc = message_crc.build(dict(crc=create_crc(cmd_all)))

	return(cmd_all + msg_crc)

################################################################

def LynxResetMotorEncoderCommand(motor):
	header = message_format_packet_header.build(dict(
		length=11+1, 
		dest_module=3,
		source_module=0,
		packet_num=0,
		reference_num=0,
		packet_id='LynxResetMotorEncoderCommand'))

	payload_format = Struct(
		"motor" / Int8ub
		)

	payload = payload_format.build(dict(
		motor=motor))

	cmd_all = header + payload

	msg_crc = message_crc.build(dict(crc=create_crc(cmd_all)))

	return(cmd_all + msg_crc)

################################################################

def LynxSetSingleDIOOutputCommand(pin, value):
	header = message_format_packet_header.build(dict(
		length=11+2, 
		dest_module=3,
		source_module=0,
		packet_num=0,
		reference_num=0,
		packet_id='LynxSetSingleDIOOutputCommand'))

	payload_format = Struct(
		"pin" / Int8ub,
		"value" / Int8ub)

	payload = payload_format.build(dict(
		pin = pin,
		value = value))

	cmd_all = header + payload

	msg_crc = message_crc.build(dict(crc=create_crc(cmd_all)))

	return(cmd_all + msg_crc)

################################################################

def LynxSetAllDIOOutputsCommand(value):
	header = message_format_packet_header.build(dict(
		length=11+1, 
		dest_module=3,
		source_module=0,
		packet_num=0,
		reference_num=0,
		packet_id='LynxSetAllDIOOutputsCommand'))

	payload_format = Struct(
		"value" / Int8ub)

	payload = payload_format.build(dict(
		value = value))


	cmd_all = header + payload

	msg_crc = message_crc.build(dict(crc=create_crc(cmd_all)))

	return(cmd_all + msg_crc)

################################################################

def LynxSetDIODirectionCommand(pin, direction):
	header = message_format_packet_header.build(dict(
		length=11+2, 
		dest_module=3,
		source_module=0,
		packet_num=0,
		reference_num=0,
		packet_id='LynxSetDIODirectionCommand'))

	payload_format = Struct(
		"pin" / Int8ub,
		"direction" / Int8ub)

	if direction == "input":
		my_direction = 0
	else:
		my_direction = 1

	payload = payload_format.build(dict(
		pin = pin,
		direction = my_direction))


	cmd_all = header + payload

	msg_crc = message_crc.build(dict(crc=create_crc(cmd_all)))

	return(cmd_all + msg_crc)

################################################################

def LynxIsMotorAtTargetCommand(motor):
	header = message_format_packet_header.build(dict(
		length=11+1, 
		dest_module=3,
		source_module=0,
		packet_num=0,
		reference_num=0,
		packet_id='LynxIsMotorAtTargetCommand'))

	payload_format = Struct(
		"motor" / Int8ub)

	payload = payload_format.build(dict(
		motor = motor))


	cmd_all = header + payload

	msg_crc = message_crc.build(dict(crc=create_crc(cmd_all)))

	return(cmd_all + msg_crc)

################################################################

def LynxSetServoConfigurationCommand(channel, framePeriod):
	header = message_format_packet_header.build(dict(
		length=11+3, 
		dest_module=3,
		source_module=0,
		packet_num=0,
		reference_num=0,
		packet_id='LynxSetServoConfigurationCommand'))

	payload_format = Struct(
		"channel" / Int8ub,
		"framePeriod" / Int16ul)

	payload = payload_format.build(dict(
		channel = channel,
		framePeriod = framePeriod))


	cmd_all = header + payload

	msg_crc = message_crc.build(dict(crc=create_crc(cmd_all)))

	return(cmd_all + msg_crc)

################################################################

def LynxSetServoPulseWidthCommand(channel, pulseWidth):
	header = message_format_packet_header.build(dict(
		length=11+3, 
		dest_module=3,
		source_module=0,
		packet_num=0,
		reference_num=0,
		packet_id='LynxSetServoPulseWidthCommand'))

	payload_format = Struct(
		"channel" / Int8ub,
		"pulseWidth" / Int16ul)

	payload = payload_format.build(dict(
		channel = channel,
		pulseWidth = pulseWidth))


	cmd_all = header + payload

	msg_crc = message_crc.build(dict(crc=create_crc(cmd_all)))

	return(cmd_all + msg_crc)

################################################################

def LynxGetServoPulseWidthCommand(channel):
	header = message_format_packet_header.build(dict(
		length=11+1, 
		dest_module=3,
		source_module=0,
		packet_num=0,
		reference_num=0,
		packet_id='LynxGetServoPulseWidthCommand'))

	payload_format = Struct(
		"channel" / Int8ub)

	payload = payload_format.build(dict(
		channel = channel))

	cmd_all = header + payload

	msg_crc = message_crc.build(dict(crc=create_crc(cmd_all)))

	return(cmd_all + msg_crc)

################################################################

def LynxGetSingleDIOInputCommand(pin):
	header = message_format_packet_header.build(dict(
		length=11+1, 
		dest_module=3,
		source_module=0,
		packet_num=0,
		reference_num=0,
		packet_id='LynxGetSingleDIOInputCommand'))

	payload_format = Struct(
		"pin" / Int8ub)

	payload = payload_format.build(dict(
		pin = pin))

	cmd_all = header + payload

	msg_crc = message_crc.build(dict(crc=create_crc(cmd_all)))

	return(cmd_all + msg_crc)

################################################################

def LynxGetADCCommand(channel, mode):
	header = message_format_packet_header.build(dict(
		length=11+2, 
		dest_module=3,
		source_module=0,
		packet_num=0,
		reference_num=0,
		packet_id='LynxGetADCCommand'))

	payload_format = Struct(
		"channel" / Int8ub,
		"mode" / Int8ub)

	payload = payload_format.build(dict(
		channel = channel,
		mode = mode))

	cmd_all = header + payload

	msg_crc = message_crc.build(dict(crc=create_crc(cmd_all)))

	return(cmd_all + msg_crc)




################################################################

def COMMAND_ACK():
	header = message_format_packet_header.build(dict(
		length=11, 
		dest_module=3,
		source_module=0,
		packet_num=0,
		reference_num=0,
		packet_id='COMMAND_NUMBER_ACK'))

	cmd_all = header
	msg_crc = message_crc.build(dict(crc=create_crc(cmd_all)))

	return(cmd_all + msg_crc)

################################################################

def COMMAND_KEEP_ALIVE():
	header = message_format_packet_header.build(dict(
		length=11, 
		dest_module=3,
		source_module=0,
		packet_num=0,
		reference_num=0,
		packet_id='COMMAND_NUMBER_KEEP_ALIVE'))

	cmd_all = header
	msg_crc = message_crc.build(dict(crc=create_crc(cmd_all)))

	return(cmd_all + msg_crc)

################################################################

def COMMAND_DISCOVERY():
	header = message_format_packet_header.build(dict(
		length=11, 
		dest_module=255,
		source_module=0,
		packet_num=0,
		reference_num=0,
		packet_id='COMMAND_NUMBER_DISCOVERY'))

	cmd_all = header
	msg_crc = message_crc.build(dict(crc=create_crc(cmd_all)))

	return(cmd_all + msg_crc)

################################################################

def COMMAND_GET_MODULE_STATUS():
	header = message_format_packet_header.build(dict(
		length=12, 
		dest_module=3,
		source_module=0,
		packet_num=0,
		reference_num=0,
		packet_id='COMMAND_NUMBER_GET_MODULE_STATUS'))

	payload = bytearray(b'\x01')
	cmd_all = header + payload
	msg_crc = message_crc.build(dict(crc=create_crc(cmd_all)))

	return(cmd_all + msg_crc)

################################################################

def COMMAND_DEBUG_LOG_LEVEL():
	header = message_format_packet_header.build(dict(
		length=11+2, 
		dest_module=3,
		source_module=0,
		packet_num=0,
		reference_num=0,
		packet_id='COMMAND_NUMBER_DEBUG_LOG_LEVEL'))

	payload = bytearray(b'\x01\x02')
	cmd_all = header + payload
	msg_crc = message_crc.build(dict(crc=create_crc(cmd_all)))

	return(cmd_all + msg_crc)

################################################################

def COMMAND_FAIL_SAFE():
	header = message_format_packet_header.build(dict(
		length=11, 
		dest_module=3,
		source_module=0,
		packet_num=0,
		reference_num=0,
		packet_id='COMMAND_NUMBER_FAIL_SAFE'))

	cmd_all = header
	msg_crc = message_crc.build(dict(crc=create_crc(cmd_all)))

	return(cmd_all + msg_crc)

################################################################

def LynxI2cWriteSingleByteCommand(busZ, i2cAddr, bValue):
	header = message_format_packet_header.build(dict(
		length=11 + 3, 
		dest_module=3,
		source_module=0,
		packet_num=0,
		reference_num=0,
		packet_id='LynxI2cWriteSingleByteCommand'))

	payload_format = Struct(
		"i2cBus" / Int8ub,
		"i2cAddr7Bit" / Int8ub,
		"bValue"/ Int8ub)

	payload = payload_format(
		i2cBus = busZ,
		i2cAddrBit = i2cAddrBit,
		bValue = bValue)

	cmd_all = header + payload
	msg_crc = message_crc.build(dict(crc=create_crc(cmd_all)))

	return(cmd_all + msg_crc)

################################################################

def LynxI2cWriteMultipleBytesCommand(busZ, I2cAddr, payload):
	header = message_format_packet_header.build(dict(
		length=11 + len(payload), 
		dest_module=3,
		source_module=0,
		packet_num=0,
		reference_num=0,
		packet_id='LynxI2cWriteMultipleBytesCommand'))

	payload_format = Struct(
		"i2cBus" / Int8ub,
		"i2cAddr7Bit" / Int8ub,
		"payload"/ Array(payload, payload.length))

	payload = payload_format(
		i2cBus = busZ,
		i2cAddrBit = i2cAddrBit,
		payload = payload)

	cmd_all = header + payload
	msg_crc = message_crc.build(dict(crc=create_crc(cmd_all)))

################################################################

def LynxI2cReadSingleByteCommand(busZ, i2cAddr):
	header = message_format_packet_header.build(dict(
		length=11 + 2, 
		dest_module=3,
		source_module=0,
		packet_num=0,
		reference_num=0,
		packet_id='LynxI2cReadSingleByteCommand'))

	payload_format = Struct(
		"i2cBus" / Int8ub,
		"i2cAddr7Bit" / Int8ub)

	payload = payload_format(
		i2cBus = busZ,
		i2cAddrBit = i2cAddrBit)

	cmd_all = header + payload
	msg_crc = message_crc.build(dict(crc=create_crc(cmd_all)))

################################################################

def LynxI2cReadStatusQueryCommand(busZ, i2cAddr, cbToRead):
	header = message_format_packet_header.build(dict(
		length=11 + 3, 
		dest_module=3,
		source_module=0,
		packet_num=0,
		reference_num=0,
		packet_id='LynxI2cReadStatusQueryCommand'))

	payload_format = Struct(
		"i2cBus" / Int8ub,
		"i2cAddr7Bit" / Int8ub,
		"cbToRead" / Int8ub)

	payload = payload_format(
		i2cBus = busZ,
		i2cAddrBit = i2cAddrBit,
		cbToRead = cbToRead)

	cmd_all = header + payload
	msg_crc = message_crc.build(dict(crc=create_crc(cmd_all)))

################################################################

def LynxI2cWriteStatusQueryCommand(busZ):
	header = message_format_packet_header.build(dict(
		length=11 + 1, 
		dest_module=3,
		source_module=0,
		packet_num=0,
		reference_num=0,
		packet_id='LynxI2cWriteStatusQueryCommand'))

	payload_format = Struct(
		"i2cBus" / Int8ub)

	payload = payload_format(
		i2cBus = busZ)

	cmd_all = header + payload
	msg_crc = message_crc.build(dict(crc=create_crc(cmd_all)))

################################################################

def LynxI2cConfigureChannelCommand(busZ, speedCode):
	header = message_format_packet_header.build(dict(
		length=11 + 2, 
		dest_module=3,
		source_module=0,
		packet_num=0,
		reference_num=0,
		packet_id='LynxI2cConfigureChannelCommand'))

	payload_format = Struct(
		"i2cBus" / Int8ub,
		"speedCode" / Int8ub)

	payload = payload_format(
		i2cBus = busZ,
		speedCode = speedCode)

	cmd_all = header + payload
	msg_crc = message_crc.build(dict(crc=create_crc(cmd_all)))

################################################################

def LynxI2cConfigureQueryCommand(busZ):
	header = message_format_packet_header.build(dict(
		length=11 + 1, 
		dest_module=3,
		source_module=0,
		packet_num=0,
		reference_num=0,
		packet_id='LynxI2cConfigureQueryCommand'))

	payload_format = Struct(
		"i2cBus" / Int8ub)

	payload = payload_format(
		i2cBus = busZ)

	cmd_all = header + payload
	msg_crc = message_crc.build(dict(crc=create_crc(cmd_all)))
