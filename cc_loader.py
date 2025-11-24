# @name: cc_loader.py
# @desc: compadre-cache loader... loads the cache accessible by Compadre.

import os
import game.helpers.JSONHelper as JSON

player_speed = 1 # pixels/frame
present_fall_speed = 1 # pixels/frame

floor_width = 500*4

present_y_floor = 900 - 50
present_y_spawn = 5
present_y_dist = present_y_floor - present_y_spawn

positions = []

player_reach = (present_y_dist / present_fall_speed) * player_speed

for x in range(floor_width+1):
    xRow = []
    for present_x in range(floor_width+1):
        diff = abs(present_x-x)
        presentWillFall = diff > player_reach
        if presentWillFall:
            xRow.append(present_x)
    positions.append(xRow)

JSON.write("positions.json", positions)