import time

class Conf:
	"""Configuration file"""
	LAUNCH_TIME = time.time()

	class TURTLE:
		""" Configuration of the turtle """
		INIT_POS = (0, 0, 0)
		INIT_HEADING = (0, 1, 0)
		INIT_COLOR = (0.1, 0.1, 0.1)
		APPEND_STEP = 2

	class GRAPHX:
		BASE_COLOR = (0.2, 0.2, 0.2)
		CAMERA_UPDATE_PERIOD = 1
		CAMERA_ROTATION_VELOC = 0

	class LSYSTEM:
		AUTORUN_STEP = 10

	DEBUG = {
		'lsystem': 0,
	}
