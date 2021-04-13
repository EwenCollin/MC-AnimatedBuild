wrap_template = """
summon falling_block ~ ~1 ~ {Time:1,BlockState:{Name:redstone_block},Passengers:[
{id:armor_stand,Health:0,Passengers:[
{id:falling_block,Time:1,BlockState:{Name:activator_rail},Passengers:[
{id:command_block_minecart,Command:'gamerule commandBlockOutput false'},
{id:command_block_minecart,Command:'data merge block ~ ~-2 ~ {auto:0}'},
{{ commands }}
{id:command_block_minecart,Command:'setblock ~ ~1 ~ command_block{auto:1,Command:"fill ~ ~ ~ ~ ~-2 ~ air"}'},
{id:command_block_minecart,Command:'kill @e[type=command_block_minecart,distance=..1]'}]}]}]}
"""

command_template = "{id:command_block_minecart,Command:'summon falling_block ~{{ x }} ~{{ y }} ~{{ z }} {Time:1,BlockState:{{ block_state }}}'},"

command_list = []

import nbtlib
import json

block_states = ["age", "attached", "attachment", "axis", "bites", "bottom", "charges", "conditional", "delay", "disarmed", "distance", "down", "drag", "east", "eggs", "enabled", "extended", "eye", "face", "facing", "half", "hanging", "has_book", "has_bottle_0", "has_bottle_1", "has_bottle_2", "has_record", "hatch", "hinge", "in_wall", "instrument", "inverted", "layers", "leaves", "level", "lit", "locked", "mode", "moisture", "north", "note", "occupied", "open", "orientation", "part", "persistent", "pickles", "power", "powered", "rotation", "shape", "short", "signal_fire", "snowy", "south", "stage", "triggered", "type", "unstable", "up", "waterlogged", "west"]

rejected_blocks = ["minecraft:air", "minecraft:water", "minecraft:lava"]

#change 'tower.nbt' to your structure file path as string
nbt_file = nbtlib.load('tower.nbt')

palette = []
for block in nbt_file.root["palette"]:
    new_block = {"id": str(block["Name"]), "properties": {}}
    if "Properties" in block:
        block_prop = block["Properties"]
        for block_state in block_states:
            if block_state in block_prop:
                new_block["properties"][block_state] = str(block_prop[block_state])
    palette.append(new_block)
print(palette)

structure = []
for i in range(32):
    level = []
    for j in range(32):
        row = []
        for k in range(32):
            row.append({})
        level.append(row)
    structure.append(level)

for block in nbt_file.root["blocks"]:
    block_data = palette[block["state"]]
    if block_data["id"] not in rejected_blocks:
        if len(json.dumps(block_data["properties"])) < 3:
            structure[int(block["pos"][0])][int(block["pos"][1])][int(block["pos"][2])] = {"Name": block_data["id"]}
        else:
            structure[int(block["pos"][0])][int(block["pos"][1])][int(block["pos"][2])] = {"Name": block_data["id"], "Properties": block_data["properties"]}
level_grid = [[False for z in range(32)] for x in range(32)]


for x in range(32):
    for z in range(32):
        for y in range(32):
            Y = 31 - y
            if "Name" in structure[x][Y][z]:
                level_grid[x][z] = True
            elif level_grid[x][z]:
                structure[x][Y][z] = {"Name": "minecraft:barrier"}

height = 20
for x in range(32):
    for y in range(32):
        for z in range(32):
            if "Name" in structure[x][y][z]:
                command = command_template.replace("{{ x }}", str(x))
                command = command.replace("{{ y }}", str(y + height))
                command = command.replace("{{ z }}", str(z))
                command = command.replace("{{ block_state }}", json.dumps(structure[x][y][z],separators=(',', ':')))
                command_list.append(command)
                height += 1


str_command_list = ""
for command in command_list:
    str_command_list += command + "\n"

final_command = wrap_template.replace("{{ commands }}", str_command_list)

#final_command is the command string, you can save it as file for better usage
print(final_command)
