from construct import *

message_crc = Struct("crc" / Int8ub)

message_motor = Struct(
	"motor" / Int8ub,
	"power" / Int16ul,
)

message_format_packet_header = Struct(
	"signature" / Const(b'\x44\x4b'),
	"length" / Int16ul,		# packet length
	"dest_module" / Int8ub,		# Destination module address ex. 3
	"source_module" / Int8ub,	# Source module address
	"packet_num" / Int8ub,		# Increments each packet
	"reference_num" / Int8ub,	# ?
	"packet_id" / Enum(Int16ul,
		LynxSetMotorChannelModeCommand = 0x1008,
		LynxSetMotorChannelEnableCommand = 0x100a,
		LynxResetMotorEncoderCommand = 0x100e,
		LynxSetMotorConstantPowerCommand = 0x100f,
		LynxSetMotorTargetVelocityCommand = 0x1011,
		LynxSetMotorTargetPositionCommand = 0x1013,
		LynxGetMotorEncoderPositionCommand = 0x1016,
		LynxSetMotorPIDControlLoopCoefficientsCommand = 0x1017,
		LynxSetServoEnableCommand = 0x1023,
		LynxGetMotorPIDFControlLoopCoefficientsCommand = 0x1035,
		LynxSetSingleDIOOutputCommand = 0x1001,
		LynxSetAllDIOOutputsCommand = 0x1002,
		LynxSetDIODirectionCommand = 0x1003,
		LynxIsMotorAtTargetCommand = 0x1015,
		LynxSetServoConfigurationCommand = 0x101f,
		LynxSetServoPulseWidthCommand = 0x1021,
		LynxGetServoPulseWidthCommand = 0x1022,
		LynxGetSingleDIOInputCommand = 0x1005,
		LynxGetADCCommand = 0x1007,
		LynxI2cWriteSingleByteCommand = 0x10025,
		LynxI2cWriteMultipleBytesCommand = 0x1026,
		LynxI2cReadSingleByteCommand = 0x1027,
		LynxI2cReadMultipleBytesCommand = 0x1028,
		LynxI2cReadStatusQueryCommand = 0x1029,
		LynxI2cWriteStatusQueryCommand = 0x1030,
		LynxI2cConfigureChannelCommand = 0x1031,
		LynxI2cConfigureQueryCommand = 0x102f,
		COMMAND_NUMBER_ACK = 0x7f01,
		COMMAND_NUMBER_GET_MODULE_STATUS = 0x7f03,
		COMMAND_NUMBER_KEEP_ALIVE = 0x7f04,
		COMMAND_NUMBER_DISCOVERY = 0x7f0f,
		COMMAND_NUMBER_DEBUG_LOG_LEVEL = 0x7f0e,
		COMMAND_NUMBER_FAIL_SAFE = 0x7f05)
	)


def create_crc(msg):
    sum = 0
    for i in msg:
        sum += i

    return((sum & 255))


# I promise that you'll never find another like me
# I know that I'm a handful, baby, uh
# I know I never think before I jump
# And you're the kind of guy the ladies want
# (And there's a lot of cool chicks out there)
# I know that I went psycho on the phone
# I never leave well enough alone
# And trouble's gonna follow where I go
# (And there's a lot of cool chicks out there)
# But one of these things is not like the others
# Like a rainbow with all of the colors
# Baby doll, when it comes to a lover
# I promise that you'll never find another like
# Me-e-e, ooh-ooh-ooh-ooh
# I'm the only one of me
# Baby, that's the fun of me
# Eeh-eeh-eeh, ooh-ooh-ooh-ooh
# You're the only one of you
# Baby, that's the fun of you
# And I promise that nobody's gonna love you like me-e-e
# I know I tend to make it about me
# I know you never get just what you see
# But I will never bore you, baby
# {And there's a lot of lame guys out there} 
# And when we had that fight out in the rain
# You ran after me and called my name
# I never wanna see you walk away
# (And there's a lot of lame guys out there)
# 'Cause one of these things is not like the others
# Livin' in winter, I am your summer
# Baby doll, when it comes to a lover
# I promise that you'll never find another like
# Me-e-e, ooh-ooh-ooh-ooh
# I'm the only one of me
# Let me keep you company
# Eeh-eeh-eeh, ooh-ooh-ooh-ooh
# You're the only one of you
# Baby, that's the fun of you
# And I promise that nobody's gonna love you like me-e-e
# Hey, kids!
# Spelling is fun!
# Girl, there ain't no I in "team"
# But you know there is a "me"
# Strike the band up, one, two, three
# I promise that you'll never find another like me
# Girl, there ain't no I in "team"
# But you know there is a "me"
# And you can't spell "awesome" without "me"
# I promise that you'll never find another like
# Me-e-e (yeah), ooh-ooh-ooh-ooh (and I won't stop, baby)
# I'm the only one of me (I'm the only one of me)
# Baby, that's the fun of me (baby, that's the fun of me)
# Eeh-eeh-eeh, ooh-ooh-ooh-ooh (oh)
# You're the only one of you (oh)
# Baby, that's the fun of you
# And I promise that nobody's gonna love you like me-e-e
# Girl, there ain't no I in "team" (ooh-ooh-ooh-ooh)
# But you know there is a "me"
# I'm the only one of me (oh-oh)
# Baby, that's the fun of me
# (Eeh-eeh-eeh, ooh-ooh-ooh-ooh)
# Strike the band up, one, two, three
# You can't spell "awesome" without "me"
# You're the only one of you
# Baby, that's the fun of you
# And I promise that nobody's gonna love you like me-e-e