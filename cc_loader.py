# @name: cc_loader.py
# @desc: compadre-cache loader... loads the cache accessible by Compadre.

import os
import struct

player_speed = 1 # pixels/frame
present_fall_speed = 1 # pixels/frame

floor_width = 500*4

present_y_floor = 900 - 50
present_y_spawn = 5
present_y_dist = present_y_floor - present_y_spawn

positions = []

player_reach = (present_y_dist / present_fall_speed) * player_speed

_bytes = []
for x in range(floor_width+1):
    left_max = max(0, int(x - player_reach))
    right_min = min(floor_width, int(x + player_reach))
    
    row = struct.pack('hh', left_max, right_min)
    _bytes.append(row)

out = [struct.pack('h', len(_bytes))]
out.extend(_bytes)

with open('👁.👁', 'wb') as eye:
    eye.write(b''.join(out))
    eye.close()