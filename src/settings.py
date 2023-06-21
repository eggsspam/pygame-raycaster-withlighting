import math

# ENGINE SETTINGS
MAX_DEPTH = 5                           # you can turn it up although lighting probably prevents you from seeing extra depth
FOV = 60                                # Game breaks if fov is anything other than 60, not sure why. 
RAY_RES = 8                              # NEEDS TO BE POWERS OF 2, to make sure each ray fits nicely in the screen when divided

# ignore this!
HALF_FOV = FOV//2
NUM_RAYS = FOV * RAY_RES
HALF_RAYS = NUM_RAYS//2
DELTA_RA = HALF_FOV / HALF_RAYS
r_DELTA_RA = math.radians(DELTA_RA)
r_HALF_FOV = math.radians(HALF_FOV)


#light settings:
LIGHT_MAX = 800
LIGHT_OFFSET = 0
#Game settings:
TIMER = 60

# PLAYER SETTINGS
PLAYER_ROT_SPEED = 1.5
PLAYER_SPEED = 125
PAN_Z_AXIS = 500
SPAWN_POINT = 150, 1100              # first value is x coordinate, second is y. Keep the cube size in mind when picking it.
INIT_ANGLE = 0
