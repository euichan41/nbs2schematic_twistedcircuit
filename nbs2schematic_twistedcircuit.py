from stat import SF_APPEND
import sys
import os
import math
from pathlib import Path

import pynbs41
from litemapy import Schematic, Region, BlockState

from tkinter import *
from tkinter import filedialog as filedialog
from tkinter import messagebox as msg

#open file

root = Tk()
root.filename =  filedialog.askopenfilename(initialdir = r"C:\Users",title = "choose your file",filetypes = (("nbs files","*.nbs"),("all files","*.*")))
print (root.filename)

demo = pynbs41.read(root.filename)

header=demo.header
print (header.tempo)

file_path = root.filename
file_name = Path(file_path).stem
print(file_name)


new_file = pynbs41.new_file(song_name=file_name + '_20tickconverted')


#convert nbs file into 20t/s

layer_respective = [0]

temp_value = 0;

layer_maximum = 0;

note_temp = 0;
sequence_temp = 0;




for tick, chord in pynbs41.read(root.filename):
    note_tick = [note.tick for note in chord]
    note_layer = [note.layer for note in chord]
    note_instrument = [note.instrument for note in chord]
    note_key = [note.key for note in chord]
    note_velocity = [note.velocity for note in chord]
    note_panning = [note.panning for note in chord] 
    note_pitch = [note.pitch for note in chord]
    
    if layer_maximum <= len(note_layer):      ##count the maximum chord length for every tick
        layer_maximum = len(note_layer)
    
    new_file.notes.extend([
        pynbs41.Note(round(note_tick[i]*(20/header.tempo)), note_layer[i], note_instrument[i], note_key[i], note_velocity[i], note_panning[i], note_pitch[i]) for i in range(len(note_key))
    ])

new_file.header.tempo = 20

new_file.save(file_name + '_20tickconverted' + '.nbs')




#open 20t/s converted nbs file

nbs2schematic_nbsfile = pynbs41.read(file_name + '_20tickconverted' + '.nbs')


"""
for tick, chord in nbs2schematic_nbsfile:
    note_tick = [note.tick for note in chord]
    note_layer = [note.layer for note in chord]
    note_instrument = [note.instrument for note in chord]
    note_key = [note.key for note in chord]
    
    layer_diff = [i for i in note_layer if i not in layer_respective]
    layer_respective = layer_diff + layer_respective

"""

#layer_respective_sorted = sorted(layer_respective) ##sort the layers in ascending order
#print("sorted layer numbers = ", layer_respective_sorted)


if layer_maximum > 6:
    print("error! layer number over 6 is not compatible!")
    msg.showwarning("error","layer number over 6 is not compatible!")
    sys.exit(0)

"""
for x in sand_layers:
    if x in layer_respective_sorted:
        layer_respective_sorted.remove(x)

print("number of layers without sand = ", len(layer_respective_sorted))
""" ##sand layer sorting already done in line 72



"""
layers_rearranged = sand_layers + layer_respective_sorted ##rearrange the layer, put sand layers in front of the array
print("rearranged layer = ", layers_rearranged)
""" ##sand layer sorting already done in line 72

#layers_rearranged = layer_respective_sorted

songlength = nbs2schematic_nbsfile.header.song_length
print("length of the song = ", songlength)




#define minecraft blockstate

diamond_block = BlockState('minecraft:diamond_block')
cyan_concrete = BlockState('minecraft:cyan_concrete')
white_concrete = BlockState('minecraft:white_concrete')
orange_concrete = BlockState('minecraft:orange_concrete')
prismarine_slab = BlockState('minecraft:prismarine_brick_slab', {'type' : 'top'})
prismarine_bricks = BlockState('minecraft:prismarine_bricks')
dark_prismarine_slab = BlockState('minecraft:dark_prismarine_slab', {'type' : 'top'})

repeater = BlockState('minecraft:repeater')
repeater_delay2 = BlockState('minecraft:repeater', {'delay' : '2'})
repeater_eastFacing = BlockState('minecraft:repeater', {'facing' : 'east'})
repeater_westFacing = BlockState('minecraft:repeater', {'facing' : 'west'})
redstone = BlockState('minecraft:redstone_wire', {'east' : 'side', 'west' : 'side', 'north' : 'side', 'south' : 'side'})
redstone_NS = BlockState('minecraft:redstone_wire', {'east' : 'none', 'west' : 'none', 'north' : 'side', 'south' : 'side'})
redstone_NW = BlockState('minecraft:redstone_wire', {'east' : 'none', 'west' : 'side', 'north' : 'side', 'south' : 'none'})
redstone_SE = BlockState('minecraft:redstone_wire', {'east' : 'side', 'west' : 'none', 'north' : 'none', 'south' : 'side'})
redstone_NE = BlockState('minecraft:redstone_wire', {'east' : 'side', 'west' : 'none', 'north' : 'side', 'south' : 'none'})
redstone_SW = BlockState('minecraft:redstone_wire', {'east' : 'none', 'west' : 'side', 'north' : 'none', 'south' : 'side'})

sticky_piston = BlockState('minecraft:sticky_piston', {'facing' : 'down'})
redstone_block = BlockState('minecraft:redstone_block')

#create the schematic

reg = Region(-18, -7, 0, 48, 19, songlength//4 + 20) 
schem = reg.as_schematic(name=file_name, author="euichan41", description="Made with nbs2schematic")


#load the starting platform schematic

schem1 = Schematic.load("startingplatform_void1.litematic")
reg1 = list(schem1.regions.values())[0]

for x in reg1.xrange():
    for y in reg1.yrange():
        for z in reg1.zrange():
            reg.setblock(x,y,z,reg1.getblock(x,y,z))
            
"""
if layer_maximum>3:
    print("error! layer number over 36 is not compatible!")
    msg.showwarning("error","the layer number should be under 36!")
    sys.exit(0)

if layer_maximum==0:
    print("error! there must be at least 1 layer!")
    msg.showwarning("error","there must be at least 1 layer!")
    sys.exit(0)

if layer_maximum>0 and layer_maximum<=3:
    layer_case=math.ceil(layer_maximum/3)
    print("needed noteblock row number = ",layer_case) ## e.g. there will be 2 noteblock rows for 5 layers in nbs file (one row can cover 3 layers) => layer_case = 1
"""
temp_constant1 = 14
temp_constant2 = 6
for j in range(0,(songlength//32)+1):
    reg.setblock(temp_constant1+4,temp_constant2+0,j*8+4,prismarine_slab)
    reg.setblock(temp_constant1+4,temp_constant2+1,j*8+4,repeater)
    reg.setblock(temp_constant1+4,temp_constant2+0,j*8+5,dark_prismarine_slab)
    reg.setblock(temp_constant1+4,temp_constant2+1,j*8+5,prismarine_bricks) #1
    
    reg.setblock(temp_constant1+3,temp_constant2+0,j*8+5,prismarine_slab)
    reg.setblock(temp_constant1+3,temp_constant2+1,j*8+5,repeater_eastFacing)
    reg.setblock(temp_constant1+2,temp_constant2+0,j*8+5,dark_prismarine_slab)
    reg.setblock(temp_constant1+2,temp_constant2+1,j*8+5,prismarine_bricks) #2
    
    reg.setblock(temp_constant1+1,temp_constant2+0,j*8+5,prismarine_slab)
    reg.setblock(temp_constant1+1,temp_constant2+1,j*8+5,repeater_eastFacing)
    reg.setblock(temp_constant1+0,temp_constant2+0,j*8+5,dark_prismarine_slab)
    reg.setblock(temp_constant1+0,temp_constant2+1,j*8+5,prismarine_bricks) #3
    
    reg.setblock(temp_constant1+-1,temp_constant2+0,j*8+5,prismarine_slab)
    reg.setblock(temp_constant1+-1,temp_constant2+1,j*8+5,repeater_eastFacing)
    reg.setblock(temp_constant1+-2,temp_constant2+0,j*8+5,dark_prismarine_slab)
    reg.setblock(temp_constant1+-2,temp_constant2+1,j*8+5,prismarine_bricks) #4
    
    reg.setblock(temp_constant1+-3,temp_constant2+0,j*8+5,prismarine_slab)
    reg.setblock(temp_constant1+-3,temp_constant2+1,j*8+5,repeater_eastFacing)
    reg.setblock(temp_constant1+-4,temp_constant2+0,j*8+5,dark_prismarine_slab)
    reg.setblock(temp_constant1+-4,temp_constant2+1,j*8+5,prismarine_bricks) #5
    
    reg.setblock(temp_constant1+-5,temp_constant2+0,j*8+5,prismarine_slab)
    reg.setblock(temp_constant1+-5,temp_constant2+1,j*8+5,repeater_eastFacing)
    reg.setblock(temp_constant1+-6,temp_constant2+0,j*8+5,dark_prismarine_slab)
    reg.setblock(temp_constant1+-6,temp_constant2+1,j*8+5,prismarine_bricks) #6
    
    reg.setblock(temp_constant1+-7,temp_constant2+0,j*8+5,prismarine_slab)
    reg.setblock(temp_constant1+-7,temp_constant2+1,j*8+5,repeater_eastFacing)
    reg.setblock(temp_constant1+-8,temp_constant2+0,j*8+5,dark_prismarine_slab)
    reg.setblock(temp_constant1+-8,temp_constant2+1,j*8+5,prismarine_bricks) #7
    
    reg.setblock(temp_constant1+-9,temp_constant2+0,j*8+5,prismarine_slab)
    reg.setblock(temp_constant1+-9,temp_constant2+1,j*8+5,repeater_eastFacing)
    reg.setblock(temp_constant1+-10,temp_constant2+0,j*8+5,dark_prismarine_slab)
    reg.setblock(temp_constant1+-10,temp_constant2+1,j*8+5,prismarine_bricks) #8
    
    
    reg.setblock(temp_constant1+-10,temp_constant2+0,j*8+6,prismarine_slab)
    reg.setblock(temp_constant1+-10,temp_constant2+0,j*8+7,prismarine_slab)
    reg.setblock(temp_constant1+-11,temp_constant2+0,j*8+7,prismarine_slab)
    reg.setblock(temp_constant1+-10,temp_constant2+1,j*8+6,redstone_NS)
    reg.setblock(temp_constant1+-10,temp_constant2+2,j*8+6,orange_concrete)
    reg.setblock(temp_constant1+-10,temp_constant2+1,j*8+7,redstone_NW)
    reg.setblock(temp_constant1+-11,temp_constant2+1,j*8+7,redstone_SE) #turn1
    
    
    reg.setblock(temp_constant1+-11,temp_constant2+0,j*8+8,prismarine_slab)
    reg.setblock(temp_constant1+-11,temp_constant2+1,j*8+8,repeater)
    reg.setblock(temp_constant1+-11,temp_constant2+0,j*8+9,dark_prismarine_slab)
    reg.setblock(temp_constant1+-11,temp_constant2+1,j*8+9,prismarine_bricks) #9
    
    reg.setblock(temp_constant1+-10,temp_constant2+0,j*8+9,prismarine_slab)
    reg.setblock(temp_constant1+-10,temp_constant2+1,j*8+9,repeater_westFacing)
    reg.setblock(temp_constant1+-9,temp_constant2+0,j*8+9,dark_prismarine_slab)
    reg.setblock(temp_constant1+-9,temp_constant2+1,j*8+9,prismarine_bricks) #10
    
    reg.setblock(temp_constant1+-8,temp_constant2+0,j*8+9,prismarine_slab)
    reg.setblock(temp_constant1+-8,temp_constant2+1,j*8+9,repeater_westFacing)
    reg.setblock(temp_constant1+-7,temp_constant2+0,j*8+9,dark_prismarine_slab)
    reg.setblock(temp_constant1+-7,temp_constant2+1,j*8+9,prismarine_bricks) #11
    
    reg.setblock(temp_constant1+-6,temp_constant2+0,j*8+9,prismarine_slab)
    reg.setblock(temp_constant1+-6,temp_constant2+1,j*8+9,repeater_westFacing)
    reg.setblock(temp_constant1+-5,temp_constant2+0,j*8+9,dark_prismarine_slab)
    reg.setblock(temp_constant1+-5,temp_constant2+1,j*8+9,prismarine_bricks) #12
    
    reg.setblock(temp_constant1+-4,temp_constant2+0,j*8+9,prismarine_slab)
    reg.setblock(temp_constant1+-4,temp_constant2+1,j*8+9,repeater_westFacing)
    reg.setblock(temp_constant1+-3,temp_constant2+0,j*8+9,dark_prismarine_slab)
    reg.setblock(temp_constant1+-3,temp_constant2+1,j*8+9,prismarine_bricks) #13
    
    reg.setblock(temp_constant1+-2,temp_constant2+0,j*8+9,prismarine_slab)
    reg.setblock(temp_constant1+-2,temp_constant2+1,j*8+9,repeater_westFacing)
    reg.setblock(temp_constant1+-1,temp_constant2+0,j*8+9,dark_prismarine_slab)
    reg.setblock(temp_constant1+-1,temp_constant2+1,j*8+9,prismarine_bricks) #14
    
    reg.setblock(temp_constant1+0,temp_constant2+0,j*8+9,prismarine_slab)
    reg.setblock(temp_constant1+0,temp_constant2+1,j*8+9,repeater_westFacing)
    reg.setblock(temp_constant1+1,temp_constant2+0,j*8+9,dark_prismarine_slab)
    reg.setblock(temp_constant1+1,temp_constant2+1,j*8+9,prismarine_bricks) #15
    
    reg.setblock(temp_constant1+2,temp_constant2+0,j*8+9,prismarine_slab)
    reg.setblock(temp_constant1+2,temp_constant2+1,j*8+9,repeater_westFacing)
    reg.setblock(temp_constant1+3,temp_constant2+0,j*8+9,dark_prismarine_slab)
    reg.setblock(temp_constant1+3,temp_constant2+1,j*8+9,prismarine_bricks) #16
    
    
    reg.setblock(temp_constant1+3,temp_constant2+0,j*8+10,prismarine_slab)
    reg.setblock(temp_constant1+3,temp_constant2+0,j*8+11,prismarine_slab)
    reg.setblock(temp_constant1+4,temp_constant2+0,j*8+11,prismarine_slab)
    reg.setblock(temp_constant1+3,temp_constant2+1,j*8+10,redstone_NS)
    reg.setblock(temp_constant1+3,temp_constant2+2,j*8+10,orange_concrete)
    reg.setblock(temp_constant1+3,temp_constant2+1,j*8+11,redstone_NE)
    reg.setblock(temp_constant1+4,temp_constant2+1,j*8+11,redstone_SW) #turn2
    
    
    
#create blocks for each notes in layers (if a layer contains snare drum(sand), it will be placed in middle_row1)

rowx = [18, 10] ##coordinate of noteblock placement
rowy = [8, 2]


noteblock_keys = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24']
noteblock_instruments = ['harp', 'bass', 'basedrum', 'snare', 'hat', 'guitar', 'flute', 'bell', 'chime', 'xylophone', 'iron_xylophone', 'cow_bell', 'didgeridoo', 'bit', 'banjo', 'pling']
noteblock_instruments_BlockState = [BlockState('minecraft:dirt'), BlockState('minecraft:oak_planks'), BlockState('minecraft:cobblestone'), BlockState('minecraft:sand'), BlockState('minecraft:glass'), BlockState('minecraft:white_wool'), BlockState('minecraft:clay'), BlockState('minecraft:gold_block'), BlockState('minecraft:packed_ice'), BlockState('minecraft:bone_block'), BlockState('minecraft:iron_block'), BlockState('minecraft:soul_sand'), BlockState('minecraft:pumpkin'), BlockState('minecraft:emerald_block'), BlockState('minecraft:hay_block'), BlockState('minecraft:glowstone')]


init_z = 5

for tick, chord in nbs2schematic_nbsfile:
    note_tick = [note.tick for note in chord]
    note_layer = [note.layer for note in chord]
    note_instrument = [note.instrument for note in chord]
    note_key = [note.key for note in chord]
    
    sand_layers = []
    perc_layers = []
    layer_sequence =[]
    
    for x in range(len(note_layer)):  ##get the array of number 0 to (len(note_layer) - 1)
        layer_sequence.append(x)
    
    
    for i in range(len(layer_sequence)):
        if note_instrument[i] == 2 or note_instrument[i] == 4:
            if layer_sequence[i] not in perc_layers:
                perc_layers.append(layer_sequence[i])
    
    for i in range(len(layer_sequence)):
        if note_instrument[i] == 3:
            if layer_sequence[i] not in sand_layers:
                sand_layers.append(layer_sequence[i])
    
    for x in perc_layers:
        if x in layer_sequence:
            layer_sequence.remove(x)
    
    for x in sand_layers:
        if x in layer_sequence:
            layer_sequence.remove(x)
    
    if len(sand_layers) > 9:
        print("error! sand layer number over 3 is not compatible!")
        msg.showwarning("error","there must be maximum 3 layers of snare drum(sand)!")
        sys.exit(0)
    
    layer_rearranged = sand_layers + perc_layers + layer_sequence
    
    
    print(sand_layers, perc_layers, layer_sequence, layer_rearranged)
    
    #for c in range(layer_maximum):
        #layer_sequence[c] = (layer_maximum - 1) - layer_sequence[c]
    
    #print(layer_sequence)



    for j in range(len(layer_rearranged)):
        for i in range(len(note_layer)):
            if i == layer_rearranged[j]:
                if note_tick[i] == 1:
                    reg.setblock(rowx[(j//6)], rowy[(j//6)]-1, (note_tick[i]//32)*8+init_z-2, redstone_NS)
                    reg.setblock(rowx[(j//6)], rowy[(j//6)]-2, (note_tick[i]//32)*8+init_z-2, sticky_piston)
                    reg.setblock(rowx[(j//6)], rowy[(j//6)]-3, (note_tick[i]//32)*8+init_z-2, redstone_block)
                    reg.setblock(rowx[(j//6)], rowy[(j//6)]-5, (note_tick[i]//32)*8+init_z-2, redstone)
                    reg.setblock(rowx[(j//6)], rowy[(j//6)]-6, (note_tick[i]//32)*8+init_z-2, prismarine_slab)
                    if j % 6 == 0:
                        reg.setblock(rowx[(j//6)]+1, rowy[(j//6)]-5, (note_tick[i]//32)*8+init_z-2, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                        reg.setblock(rowx[(j//6)]+1, rowy[(j//6)]-6, (note_tick[i]//32)*8+init_z-2, noteblock_instruments_BlockState[note_instrument[i]])
                        if note_instrument[i] == 3:
                            reg.setblock(rowx[(j//6)]+1, rowy[(j//6)]-7, (note_tick[i]//32)*8+init_z-2, prismarine_slab)
                        reg.setblock(rowx[(j//6)], rowy[(j//6)]-5, (note_tick[i]//32)*8+init_z-2, redstone)
                        
                    if j % 6 == 1:
                        reg.setblock(rowx[(j//6)], rowy[(j//6)]-5, (note_tick[i]//32)*8+init_z-2-1, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                        reg.setblock(rowx[(j//6)], rowy[(j//6)]-6, (note_tick[i]//32)*8+init_z-2-1, noteblock_instruments_BlockState[note_instrument[i]])
                        if note_instrument[i] == 3:
                            reg.setblock(rowx[(j//6)], rowy[(j//6)]-7, (note_tick[i]//32)*8+init_z-2-1, prismarine_slab)
                        reg.setblock(rowx[(j//6)], rowy[(j//6)]-5, (note_tick[i]//32)*8+init_z-2, redstone)
                        
                    if j % 6 == 2:
                        reg.setblock(rowx[(j//6)]+1, rowy[(j//6)]-5, (note_tick[i]//32)*8+init_z-2-1, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                        reg.setblock(rowx[(j//6)]+1, rowy[(j//6)]-6, (note_tick[i]//32)*8+init_z-2-1, noteblock_instruments_BlockState[note_instrument[i]])
                        if note_instrument[i] == 3:
                            reg.setblock(rowx[(j//6)]+1, rowy[(j//6)]-7, (note_tick[i]//32)*8+init_z-2-1, prismarine_slab)
                        reg.setblock(rowx[(j//6)], rowy[(j//6)]-5, (note_tick[i]//32)*8+init_z-2, redstone)
                        
                    if j % 6 == 3:
                        reg.setblock(rowx[(j//6)], rowy[(j//6)]-5, (note_tick[i]//32)*8+init_z-2-2, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                        reg.setblock(rowx[(j//6)], rowy[(j//6)]-6, (note_tick[i]//32)*8+init_z-2-2, noteblock_instruments_BlockState[note_instrument[i]])
                        if note_instrument[i] == 3:
                            reg.setblock(rowx[(j//6)], rowy[(j//6)]-7, (note_tick[i]//32)*8+init_z-2-2, prismarine_slab)
                        reg.setblock(rowx[(j//6)], rowy[(j//6)]-5, (note_tick[i]//32)*8+init_z-2, redstone)
                        
                    if j % 6 == 4:
                        reg.setblock(rowx[(j//6)]+1, rowy[(j//6)]-5, (note_tick[i]//32)*8+init_z-2+1, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                        reg.setblock(rowx[(j//6)]+1, rowy[(j//6)]-6, (note_tick[i]//32)*8+init_z-2+1, noteblock_instruments_BlockState[note_instrument[i]])
                        if note_instrument[i] == 3:
                            reg.setblock(rowx[(j//6)]+1, rowy[(j//6)]-7, (note_tick[i]//32)*8+init_z-2+1, prismarine_slab)
                        reg.setblock(rowx[(j//6)], rowy[(j//6)]-5, (note_tick[i]//32)*8+init_z-2, redstone)
                        
                    if j % 6 == 5:
                        reg.setblock(rowx[(j//6)]+2, rowy[(j//6)]-5, (note_tick[i]//32)*8+init_z-2, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                        reg.setblock(rowx[(j//6)]+2, rowy[(j//6)]-6, (note_tick[i]//32)*8+init_z-2, noteblock_instruments_BlockState[note_instrument[i]])
                        if note_instrument[i] == 3:
                            reg.setblock(rowx[(j//6)]+2, rowy[(j//6)]-7, (note_tick[i]//32)*8+init_z-2, prismarine_slab)
                        reg.setblock(rowx[(j//6)], rowy[(j//6)]-5, (note_tick[i]//32)*8+init_z-2, redstone)
                    
                    
                for k in range (0,8):
                    if note_tick[i] % 32 == 2*k:
                        if k == 0:
                            if j % 6 == 0:
                                reg.setblock(rowx[(j//6)]-2*k+1, rowy[(j//6)], (note_tick[i]//32)*8+init_z, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                                reg.setblock(rowx[(j//6)]-2*k+1, rowy[(j//6)]-1, (note_tick[i]//32)*8+init_z, noteblock_instruments_BlockState[note_instrument[i]])
                                if note_instrument[i] == 3:
                                    reg.setblock(rowx[(j//6)]+2*k+1, rowy[(j//6)]-2, (note_tick[i]//32)*8+init_z, prismarine_slab)
                                reg.setblock(rowx[(j//6)]-2*k, rowy[(j//6)], (note_tick[i]//32)*8+init_z, redstone)
                                
                            if j % 6 == 1:
                                reg.setblock(rowx[(j//6)]-2*k, rowy[(j//6)], (note_tick[i]//32)*8+init_z+1, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                                reg.setblock(rowx[(j//6)]-2*k, rowy[(j//6)]-1, (note_tick[i]//32)*8+init_z+1, noteblock_instruments_BlockState[note_instrument[i]])
                                if note_instrument[i] == 3:
                                    reg.setblock(rowx[(j//6)]-2*k, rowy[(j//6)]-2, (note_tick[i]//32)*8+init_z+1, prismarine_slab)
                                reg.setblock(rowx[(j//6)]-2*k, rowy[(j//6)], (note_tick[i]//32)*8+init_z, redstone)
                                
                            if j % 6 == 2:
                                reg.setblock(rowx[(j//6)]-2*k+2, rowy[(j//6)], (note_tick[i]//32)*8+init_z, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                                reg.setblock(rowx[(j//6)]-2*k+2, rowy[(j//6)]-1, (note_tick[i]//32)*8+init_z, noteblock_instruments_BlockState[note_instrument[i]])
                                if note_instrument[i] == 3:
                                    reg.setblock(rowx[(j//6)]-2*k+2, rowy[(j//6)]-2, (note_tick[i]//32)*8+init_z, prismarine_slab)
                                reg.setblock(rowx[(j//6)]-2*k, rowy[(j//6)], (note_tick[i]//32)*8+init_z, redstone)
                                
                            if j % 6 == 3:
                                reg.setblock(rowx[(j//6)]-2*k-1, rowy[(j//6)], (note_tick[i]//32)*8+init_z+1, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                                reg.setblock(rowx[(j//6)]-2*k-1, rowy[(j//6)]-1, (note_tick[i]//32)*8+init_z+1, noteblock_instruments_BlockState[note_instrument[i]])
                                if note_instrument[i] == 3:
                                    reg.setblock(rowx[(j//6)]-2*k-1, rowy[(j//6)]-2, (note_tick[i]//32)*8+init_z+1, prismarine_slab)
                                reg.setblock(rowx[(j//6)]-2*k, rowy[(j//6)], (note_tick[i]//32)*8+init_z, redstone)
                                
                            if j % 6 == 4:
                                reg.setblock(rowx[(j//6)]-2*k+1, rowy[(j//6)], (note_tick[i]//32)*8+init_z+1, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                                reg.setblock(rowx[(j//6)]-2*k+1, rowy[(j//6)]-1, (note_tick[i]//32)*8+init_z+1, noteblock_instruments_BlockState[note_instrument[i]])
                                if note_instrument[i] == 3:
                                    reg.setblock(rowx[(j//6)]-2*k+1, rowy[(j//6)]-2, (note_tick[i]//32)*8+init_z+1, prismarine_slab)
                                reg.setblock(rowx[(j//6)]-2*k, rowy[(j//6)], (note_tick[i]//32)*8+init_z, redstone)
                                
                            if j % 6 == 5:
                                reg.setblock(rowx[(j//6)]-2*k, rowy[(j//6)], (note_tick[i]//32)*8+init_z+2, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                                reg.setblock(rowx[(j//6)]-2*k, rowy[(j//6)]-1, (note_tick[i]//32)*8+init_z+2, noteblock_instruments_BlockState[note_instrument[i]])
                                if note_instrument[i] == 3:
                                    reg.setblock(rowx[(j//6)]-2*k, rowy[(j//6)]-2, (note_tick[i]//32)*8+init_z+2, prismarine_slab)
                                reg.setblock(rowx[(j//6)]-2*k, rowy[(j//6)], (note_tick[i]//32)*8+init_z, redstone)
                                
                        if k > 0 and k < 7:
                            if j % 6 == 0:
                                reg.setblock(rowx[(j//6)]-2*k, rowy[(j//6)], (note_tick[i]//32)*8+init_z+1, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                                reg.setblock(rowx[(j//6)]-2*k, rowy[(j//6)]-1, (note_tick[i]//32)*8+init_z+1, noteblock_instruments_BlockState[note_instrument[i]])
                                if note_instrument[i] == 3:
                                    reg.setblock(rowx[(j//6)]-2*k, rowy[(j//6)]-2, (note_tick[i]//32)*8+init_z+1, prismarine_slab)
                                reg.setblock(rowx[(j//6)]-2*k, rowy[(j//6)], (note_tick[i]//32)*8+init_z, redstone)
                                
                            if j % 6 == 1:
                                reg.setblock(rowx[(j//6)]-2*k, rowy[(j//6)], (note_tick[i]//32)*8+init_z-1, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                                reg.setblock(rowx[(j//6)]-2*k, rowy[(j//6)]-1, (note_tick[i]//32)*8+init_z-1, noteblock_instruments_BlockState[note_instrument[i]])
                                if note_instrument[i] == 3:
                                    reg.setblock(rowx[(j//6)]-2*k, rowy[(j//6)]-2, (note_tick[i]//32)*8+init_z-1, prismarine_slab)
                                reg.setblock(rowx[(j//6)]-2*k, rowy[(j//6)], (note_tick[i]//32)*8+init_z, redstone)
                                
                            if j % 6 == 2:
                                reg.setblock(rowx[(j//6)]-2*k, rowy[(j//6)], (note_tick[i]//32)*8+init_z+2, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                                reg.setblock(rowx[(j//6)]-2*k, rowy[(j//6)]-1, (note_tick[i]//32)*8+init_z+2, noteblock_instruments_BlockState[note_instrument[i]])
                                if note_instrument[i] == 3:
                                    reg.setblock(rowx[(j//6)]-2*k, rowy[(j//6)]-2, (note_tick[i]//32)*8+init_z+2, prismarine_slab)
                                reg.setblock(rowx[(j//6)]-2*k, rowy[(j//6)], (note_tick[i]//32)*8+init_z, redstone)
                                
                            if j % 6 == 3:
                                reg.setblock(rowx[(j//6)]-2*k, rowy[(j//6)], (note_tick[i]//32)*8+init_z-2, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                                reg.setblock(rowx[(j//6)]-2*k, rowy[(j//6)]-1, (note_tick[i]//32)*8+init_z-2, noteblock_instruments_BlockState[note_instrument[i]])
                                if note_instrument[i] == 3:
                                    reg.setblock(rowx[(j//6)]-2*k, rowy[(j//6)]-2, (note_tick[i]//32)*8+init_z-2, prismarine_slab)
                                reg.setblock(rowx[(j//6)]-2*k, rowy[(j//6)], (note_tick[i]//32)*8+init_z, redstone)
                                
                            if j % 6 == 4:
                                reg.setblock(rowx[(j//6)]-2*k-1, rowy[(j//6)], (note_tick[i]//32)*8+init_z+1, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                                reg.setblock(rowx[(j//6)]-2*k-1, rowy[(j//6)]-1, (note_tick[i]//32)*8+init_z+1, noteblock_instruments_BlockState[note_instrument[i]])
                                if note_instrument[i] == 3:
                                    reg.setblock(rowx[(j//6)]-2*k-1, rowy[(j//6)]-2, (note_tick[i]//32)*8+init_z+1, prismarine_slab)
                                reg.setblock(rowx[(j//6)]-2*k, rowy[(j//6)], (note_tick[i]//32)*8+init_z, redstone)
                                
                            if j % 6 == 5:
                                reg.setblock(rowx[(j//6)]-2*k-1, rowy[(j//6)], (note_tick[i]//32)*8+init_z-1, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                                reg.setblock(rowx[(j//6)]-2*k-1, rowy[(j//6)]-1, (note_tick[i]//32)*8+init_z-1, noteblock_instruments_BlockState[note_instrument[i]])
                                if note_instrument[i] == 3:
                                    reg.setblock(rowx[(j//6)]-2*k-1, rowy[(j//6)]-2, (note_tick[i]//32)*8+init_z-1, prismarine_slab)
                                reg.setblock(rowx[(j//6)]-2*k, rowy[(j//6)], (note_tick[i]//32)*8+init_z, redstone)
                                
                        if k == 7:
                            if j % 6 == 0:
                                reg.setblock(rowx[(j//6)]-2*k-1, rowy[(j//6)], (note_tick[i]//32)*8+init_z, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                                reg.setblock(rowx[(j//6)]-2*k-1, rowy[(j//6)]-1, (note_tick[i]//32)*8+init_z, noteblock_instruments_BlockState[note_instrument[i]])
                                if note_instrument[i] == 3:
                                    reg.setblock(rowx[(j//6)]-2*k-1, rowy[(j//6)]-2, (note_tick[i]//32)*8+init_z, prismarine_slab)
                                reg.setblock(rowx[(j//6)]-2*k, rowy[(j//6)], (note_tick[i]//32)*8+init_z, redstone)
                                
                            if j % 6 == 1:
                                reg.setblock(rowx[(j//6)]-2*k, rowy[(j//6)], (note_tick[i]//32)*8+init_z-1, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                                reg.setblock(rowx[(j//6)]-2*k, rowy[(j//6)]-1, (note_tick[i]//32)*8+init_z-1, noteblock_instruments_BlockState[note_instrument[i]])
                                if note_instrument[i] == 3:
                                    reg.setblock(rowx[(j//6)]-2*k, rowy[(j//6)]-2, (note_tick[i]//32)*8+init_z-1, prismarine_slab)
                                reg.setblock(rowx[(j//6)]-2*k, rowy[(j//6)], (note_tick[i]//32)*8+init_z, redstone)
                                
                            if j % 6 == 2:
                                reg.setblock(rowx[(j//6)]-2*k-1, rowy[(j//6)], (note_tick[i]//32)*8+init_z+1, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                                reg.setblock(rowx[(j//6)]-2*k-1, rowy[(j//6)]-1, (note_tick[i]//32)*8+init_z+1, noteblock_instruments_BlockState[note_instrument[i]])
                                if note_instrument[i] == 3:
                                    reg.setblock(rowx[(j//6)]-2*k-1, rowy[(j//6)]-2, (note_tick[i]//32)*8+init_z+1, prismarine_slab)
                                reg.setblock(rowx[(j//6)]-2*k, rowy[(j//6)], (note_tick[i]//32)*8+init_z, redstone)
                                
                            if j % 6 == 3:
                                reg.setblock(rowx[(j//6)]-2*k, rowy[(j//6)], (note_tick[i]//32)*8+init_z-2, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                                reg.setblock(rowx[(j//6)]-2*k, rowy[(j//6)]-1, (note_tick[i]//32)*8+init_z-2, noteblock_instruments_BlockState[note_instrument[i]])
                                if note_instrument[i] == 3:
                                    reg.setblock(rowx[(j//6)]-2*k, rowy[(j//6)]-2, (note_tick[i]//32)*8+init_z-2, prismarine_slab)
                                reg.setblock(rowx[(j//6)]-2*k, rowy[(j//6)], (note_tick[i]//32)*8+init_z, redstone)
                                
                            if j % 6 == 4:
                                reg.setblock(rowx[(j//6)]-2*k-2, rowy[(j//6)], (note_tick[i]//32)*8+init_z, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                                reg.setblock(rowx[(j//6)]-2*k-2, rowy[(j//6)]-1, (note_tick[i]//32)*8+init_z, noteblock_instruments_BlockState[note_instrument[i]])
                                if note_instrument[i] == 3:
                                    reg.setblock(rowx[(j//6)]-2*k-2, rowy[(j//6)]-2, (note_tick[i]//32)*8+init_z, prismarine_slab)
                                reg.setblock(rowx[(j//6)]-2*k, rowy[(j//6)], (note_tick[i]//32)*8+init_z, redstone)
                                
                            if j % 6 == 5:
                                reg.setblock(rowx[(j//6)]-2*k-1, rowy[(j//6)], (note_tick[i]//32)*8+init_z-1, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                                reg.setblock(rowx[(j//6)]-2*k-1, rowy[(j//6)]-1, (note_tick[i]//32)*8+init_z-1, noteblock_instruments_BlockState[note_instrument[i]])
                                if note_instrument[i] == 3:
                                    reg.setblock(rowx[(j//6)]-2*k-1, rowy[(j//6)]-2, (note_tick[i]//32)*8+init_z-1, prismarine_slab)
                                reg.setblock(rowx[(j//6)]-2*k, rowy[(j//6)], (note_tick[i]//32)*8+init_z, redstone)
                                
                    if (note_tick[i]-3) % 32 == 2*k and i != 1:
                        if k >= 0 and k < 8:
                            reg.setblock(rowx[(j//6)]-2*k, rowy[(j//6)]-2, ((note_tick[i]-3)//32)*8+init_z, sticky_piston)
                            reg.setblock(rowx[(j//6)]-2*k, rowy[(j//6)]-3, ((note_tick[i]-3)//32)*8+init_z, redstone_block)
                            reg.setblock(rowx[(j//6)]-2*k, rowy[(j//6)]-5, ((note_tick[i]-3)//32)*8+init_z, redstone)
                            reg.setblock(rowx[(j//6)]-2*k, rowy[(j//6)]-6, ((note_tick[i]-3)//32)*8+init_z, prismarine_slab)
                            
                            if j % 6 == 0:
                                reg.setblock(rowx[(j//6)]-2*k, rowy[(j//6)]-5, ((note_tick[i]-3)//32)*8+init_z+1, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                                reg.setblock(rowx[(j//6)]-2*k, rowy[(j//6)]-6, ((note_tick[i]-3)//32)*8+init_z+1, noteblock_instruments_BlockState[note_instrument[i]])
                                if note_instrument[i] == 3:
                                    reg.setblock(rowx[(j//6)]-2*k, rowy[(j//6)]-7, ((note_tick[i]-3)//32)*8+init_z+1, prismarine_slab)
                                reg.setblock(rowx[(j//6)]-2*k, rowy[(j//6)]-5, ((note_tick[i]-3)//32)*8+init_z, redstone)
                                
                            if j % 6 == 1:
                                reg.setblock(rowx[(j//6)]-2*k, rowy[(j//6)]-5, ((note_tick[i]-3)//32)*8+init_z-1, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                                reg.setblock(rowx[(j//6)]-2*k, rowy[(j//6)]-6, ((note_tick[i]-3)//32)*8+init_z-1, noteblock_instruments_BlockState[note_instrument[i]])
                                if note_instrument[i] == 3:
                                    reg.setblock(rowx[(j//6)]-2*k, rowy[(j//6)]-7, ((note_tick[i]-3)//32)*8+init_z-1, prismarine_slab)
                                reg.setblock(rowx[(j//6)]-2*k, rowy[(j//6)]-5, ((note_tick[i]-3)//32)*8+init_z, redstone)
                                
                            if j % 6 == 2:
                                reg.setblock(rowx[(j//6)]-2*k, rowy[(j//6)]-5, ((note_tick[i]-3)//32)*8+init_z+2, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                                reg.setblock(rowx[(j//6)]-2*k, rowy[(j//6)]-6, ((note_tick[i]-3)//32)*8+init_z+2, noteblock_instruments_BlockState[note_instrument[i]])
                                if note_instrument[i] == 3:
                                    reg.setblock(rowx[(j//6)]-2*k, rowy[(j//6)]-7, ((note_tick[i]-3)//32)*8+init_z+2, prismarine_slab)
                                reg.setblock(rowx[(j//6)]-2*k, rowy[(j//6)]-5, ((note_tick[i]-3)//32)*8+init_z, redstone)
                                
                            if j % 6 == 3:
                                reg.setblock(rowx[(j//6)]-2*k, rowy[(j//6)]-5, ((note_tick[i]-3)//32)*8+init_z-2, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                                reg.setblock(rowx[(j//6)]-2*k, rowy[(j//6)]-6, ((note_tick[i]-3)//32)*8+init_z-2, noteblock_instruments_BlockState[note_instrument[i]])
                                if note_instrument[i] == 3:
                                    reg.setblock(rowx[(j//6)]-2*k, rowy[(j//6)]-7, ((note_tick[i]-3)//32)*8+init_z-2, prismarine_slab)
                                reg.setblock(rowx[(j//6)]-2*k, rowy[(j//6)]-5, ((note_tick[i]-3)//32)*8+init_z, redstone)
                                
                            if j % 6 == 4:
                                reg.setblock(rowx[(j//6)]-2*k-1, rowy[(j//6)]-5, ((note_tick[i]-3)//32)*8+init_z+1, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                                reg.setblock(rowx[(j//6)]-2*k-1, rowy[(j//6)]-6, ((note_tick[i]-3)//32)*8+init_z+1, noteblock_instruments_BlockState[note_instrument[i]])
                                if note_instrument[i] == 3:
                                    reg.setblock(rowx[(j//6)]-2*k-1, rowy[(j//6)]-7, ((note_tick[i]-3)//32)*8+init_z+1, prismarine_slab)
                                reg.setblock(rowx[(j//6)]-2*k, rowy[(j//6)]-5, ((note_tick[i]-3)//32)*8+init_z, redstone)
                                
                            if j % 6 == 5:
                                reg.setblock(rowx[(j//6)]-2*k-1, rowy[(j//6)]-5, ((note_tick[i]-3)//32)*8+init_z-1, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                                reg.setblock(rowx[(j//6)]-2*k-1, rowy[(j//6)]-6, ((note_tick[i]-3)//32)*8+init_z-1, noteblock_instruments_BlockState[note_instrument[i]])
                                if note_instrument[i] == 3:
                                    reg.setblock(rowx[(j//6)]-2*k-1, rowy[(j//6)]-7, ((note_tick[i]-3)//32)*8+init_z-1, prismarine_slab)
                                reg.setblock(rowx[(j//6)]-2*k, rowy[(j//6)]-5, ((note_tick[i]-3)//32)*8+init_z, redstone)
                                
                            
                for k in range (8,16):
                    if note_tick[i] % 32 == 2*k:
                        if k == 8:
                            if j % 6 == 0:
                                reg.setblock(rowx[(j//6)]+2*k-31, rowy[(j//6)], (note_tick[i]//32)*8+init_z+4+1, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                                reg.setblock(rowx[(j//6)]+2*k-31, rowy[(j//6)]-1, (note_tick[i]//32)*8+init_z+4+1, noteblock_instruments_BlockState[note_instrument[i]])
                                if note_instrument[i] == 3:
                                    reg.setblock(rowx[(j//6)]+2*k-31, rowy[(j//6)]-2, (note_tick[i]//32)*8+init_z+4+1, prismarine_slab)
                                reg.setblock(rowx[(j//6)]+2*k-31, rowy[(j//6)], (note_tick[i]//32)*8+init_z+4, redstone)
                                
                            if j % 6 == 1:
                                reg.setblock(rowx[(j//6)]+2*k-31-1, rowy[(j//6)], (note_tick[i]//32)*8+init_z+4, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                                reg.setblock(rowx[(j//6)]+2*k-31-1, rowy[(j//6)]-1, (note_tick[i]//32)*8+init_z+4, noteblock_instruments_BlockState[note_instrument[i]])
                                if note_instrument[i] == 3:
                                    reg.setblock(rowx[(j//6)]+2*k-31-1, rowy[(j//6)]-2, (note_tick[i]//32)*8+init_z+4, prismarine_slab)
                                reg.setblock(rowx[(j//6)]+2*k-31, rowy[(j//6)], (note_tick[i]//32)*8+init_z+4, redstone)
                                
                            if j % 6 == 2:
                                reg.setblock(rowx[(j//6)]+2*k-31+1, rowy[(j//6)], (note_tick[i]//32)*8+init_z+4+1, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                                reg.setblock(rowx[(j//6)]+2*k-31+1, rowy[(j//6)]-1, (note_tick[i]//32)*8+init_z+4+1, noteblock_instruments_BlockState[note_instrument[i]])
                                if note_instrument[i] == 3:
                                    reg.setblock(rowx[(j//6)]+2*k-31+1, rowy[(j//6)]-2, (note_tick[i]//32)*8+init_z+4+1, prismarine_slab)
                                reg.setblock(rowx[(j//6)]+2*k-31, rowy[(j//6)], (note_tick[i]//32)*8+init_z+4, redstone)
                                
                            if j % 6 == 3:
                                reg.setblock(rowx[(j//6)]+2*k-31-2, rowy[(j//6)], (note_tick[i]//32)*8+init_z+4, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                                reg.setblock(rowx[(j//6)]+2*k-31-2, rowy[(j//6)]-1, (note_tick[i]//32)*8+init_z+4, noteblock_instruments_BlockState[note_instrument[i]])
                                if note_instrument[i] == 3:
                                    reg.setblock(rowx[(j//6)]+2*k-31-2, rowy[(j//6)]-2, (note_tick[i]//32)*8+init_z+4, prismarine_slab)
                                reg.setblock(rowx[(j//6)]+2*k-31, rowy[(j//6)], (note_tick[i]//32)*8+init_z+4, redstone)
                                
                            if j % 6 == 4:
                                reg.setblock(rowx[(j//6)]+2*k-31, rowy[(j//6)], (note_tick[i]//32)*8+init_z+4+2, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                                reg.setblock(rowx[(j//6)]+2*k-31, rowy[(j//6)]-1, (note_tick[i]//32)*8+init_z+4+2, noteblock_instruments_BlockState[note_instrument[i]])
                                if note_instrument[i] == 3:
                                    reg.setblock(rowx[(j//6)]+2*k-31, rowy[(j//6)]-2, (note_tick[i]//32)*8+init_z+4+2, prismarine_slab)
                                reg.setblock(rowx[(j//6)]+2*k-31, rowy[(j//6)], (note_tick[i]//32)*8+init_z+4, redstone)
                                
                            if j % 6 == 5:
                                reg.setblock(rowx[(j//6)]+2*k-31-1, rowy[(j//6)], (note_tick[i]//32)*8+init_z+4+1, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                                reg.setblock(rowx[(j//6)]+2*k-31-1, rowy[(j//6)]-1, (note_tick[i]//32)*8+init_z+4+1, noteblock_instruments_BlockState[note_instrument[i]])
                                if note_instrument[i] == 3:
                                    reg.setblock(rowx[(j//6)]+2*k-31-1, rowy[(j//6)]-2, (note_tick[i]//32)*8+init_z+4+1, prismarine_slab)
                                reg.setblock(rowx[(j//6)]+2*k-31, rowy[(j//6)], (note_tick[i]//32)*8+init_z+4, redstone)
                                
                        if k > 8 and k < 15:
                            if j % 6 == 0:
                                reg.setblock(rowx[(j//6)]+2*k-31, rowy[(j//6)], (note_tick[i]//32)*8+init_z+4-1, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                                reg.setblock(rowx[(j//6)]+2*k-31, rowy[(j//6)]-1, (note_tick[i]//32)*8+init_z+4-1, noteblock_instruments_BlockState[note_instrument[i]])
                                if note_instrument[i] == 3:
                                    reg.setblock(rowx[(j//6)]+2*k-31, rowy[(j//6)]-2, (note_tick[i]//32)*8+init_z+4-1, prismarine_slab)
                                reg.setblock(rowx[(j//6)]+2*k-31, rowy[(j//6)], (note_tick[i]//32)*8+init_z+4, redstone)
                                
                            if j % 6 == 1:
                                reg.setblock(rowx[(j//6)]+2*k-31, rowy[(j//6)], (note_tick[i]//32)*8+init_z+4+1, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                                reg.setblock(rowx[(j//6)]+2*k-31, rowy[(j//6)]-1, (note_tick[i]//32)*8+init_z+4+1, noteblock_instruments_BlockState[note_instrument[i]])
                                if note_instrument[i] == 3:
                                    reg.setblock(rowx[(j//6)]+2*k-31, rowy[(j//6)]-2, (note_tick[i]//32)*8+init_z+4+1, prismarine_slab)
                                reg.setblock(rowx[(j//6)]+2*k-31, rowy[(j//6)], (note_tick[i]//32)*8+init_z+4, redstone)
                                
                            if j % 6 == 2:
                                reg.setblock(rowx[(j//6)]+2*k-31, rowy[(j//6)], (note_tick[i]//32)*8+init_z+4-2, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                                reg.setblock(rowx[(j//6)]+2*k-31, rowy[(j//6)]-1, (note_tick[i]//32)*8+init_z+4-2, noteblock_instruments_BlockState[note_instrument[i]])
                                if note_instrument[i] == 3:
                                    reg.setblock(rowx[(j//6)]+2*k-31, rowy[(j//6)]-2, (note_tick[i]//32)*8+init_z+4-2, prismarine_slab)
                                reg.setblock(rowx[(j//6)]+2*k-31, rowy[(j//6)], (note_tick[i]//32)*8+init_z+4, redstone)
                                
                            if j % 6 == 3:
                                reg.setblock(rowx[(j//6)]+2*k-31, rowy[(j//6)], (note_tick[i]//32)*8+init_z+4+2, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                                reg.setblock(rowx[(j//6)]+2*k-31, rowy[(j//6)]-1, (note_tick[i]//32)*8+init_z+4+2, noteblock_instruments_BlockState[note_instrument[i]])
                                if note_instrument[i] == 3:
                                    reg.setblock(rowx[(j//6)]+2*k-31, rowy[(j//6)]-2, (note_tick[i]//32)*8+init_z+4+2, prismarine_slab)
                                reg.setblock(rowx[(j//6)]+2*k-31, rowy[(j//6)], (note_tick[i]//32)*8+init_z+4, redstone)
                                
                            if j % 6 == 4:
                                reg.setblock(rowx[(j//6)]+2*k-31+1, rowy[(j//6)], (note_tick[i]//32)*8+init_z+4-1, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                                reg.setblock(rowx[(j//6)]+2*k-31+1, rowy[(j//6)]-1, (note_tick[i]//32)*8+init_z+4-1, noteblock_instruments_BlockState[note_instrument[i]])
                                if note_instrument[i] == 3:
                                    reg.setblock(rowx[(j//6)]+2*k-31+1, rowy[(j//6)]-2, (note_tick[i]//32)*8+init_z+4-1, prismarine_slab)
                                reg.setblock(rowx[(j//6)]+2*k-31, rowy[(j//6)], (note_tick[i]//32)*8+init_z+4, redstone)
                                
                            if j % 6 == 5:
                                reg.setblock(rowx[(j//6)]+2*k-31+1, rowy[(j//6)], (note_tick[i]//32)*8+init_z+4+1, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                                reg.setblock(rowx[(j//6)]+2*k-31+1, rowy[(j//6)]-1, (note_tick[i]//32)*8+init_z+4+1, noteblock_instruments_BlockState[note_instrument[i]])
                                if note_instrument[i] == 3:
                                    reg.setblock(rowx[(j//6)]+2*k-31+1, rowy[(j//6)]-2, (note_tick[i]//32)*8+init_z+4+1, prismarine_slab)
                                reg.setblock(rowx[(j//6)]+2*k-31, rowy[(j//6)], (note_tick[i]//32)*8+init_z+4, redstone)
                                
                        if k == 15:
                            if j % 6 == 0:
                                reg.setblock(rowx[(j//6)]+2*k-31, rowy[(j//6)], (note_tick[i]//32)*8+init_z+4-1, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                                reg.setblock(rowx[(j//6)]+2*k-31, rowy[(j//6)]-1, (note_tick[i]//32)*8+init_z+4-1, noteblock_instruments_BlockState[note_instrument[i]])
                                if note_instrument[i] == 3:
                                    reg.setblock(rowx[(j//6)]+2*k-31, rowy[(j//6)]-2, (note_tick[i]//32)*8+init_z+4-1, prismarine_slab)
                                reg.setblock(rowx[(j//6)]+2*k-31, rowy[(j//6)], (note_tick[i]//32)*8+init_z+4, redstone)
                                
                            if j % 6 == 1:
                                reg.setblock(rowx[(j//6)]+2*k-31+1, rowy[(j//6)], (note_tick[i]//32)*8+init_z+4, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                                reg.setblock(rowx[(j//6)]+2*k-31+1, rowy[(j//6)]-1, (note_tick[i]//32)*8+init_z+4, noteblock_instruments_BlockState[note_instrument[i]])
                                if note_instrument[i] == 3:
                                    reg.setblock(rowx[(j//6)]+2*k-31+1, rowy[(j//6)]-2, (note_tick[i]//32)*8+init_z+4, prismarine_slab)
                                reg.setblock(rowx[(j//6)]+2*k-31, rowy[(j//6)], (note_tick[i]//32)*8+init_z+4, redstone)
                                
                            if j % 6 == 2:
                                reg.setblock(rowx[(j//6)]+2*k-31, rowy[(j//6)], (note_tick[i]//32)*8+init_z+4-2, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                                reg.setblock(rowx[(j//6)]+2*k-31, rowy[(j//6)]-1, (note_tick[i]//32)*8+init_z+4-2, noteblock_instruments_BlockState[note_instrument[i]])
                                if note_instrument[i] == 3:
                                    reg.setblock(rowx[(j//6)]+2*k-31, rowy[(j//6)]-2, (note_tick[i]//32)*8+init_z+4-2, prismarine_slab)
                                reg.setblock(rowx[(j//6)]+2*k-31, rowy[(j//6)], (note_tick[i]//32)*8+init_z+4, redstone)
                                
                            if j % 6 == 3:
                                reg.setblock(rowx[(j//6)]+2*k-31+1, rowy[(j//6)], (note_tick[i]//32)*8+init_z+4+1, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                                reg.setblock(rowx[(j//6)]+2*k-31+1, rowy[(j//6)]-1, (note_tick[i]//32)*8+init_z+4+1, noteblock_instruments_BlockState[note_instrument[i]])
                                if note_instrument[i] == 3:
                                    reg.setblock(rowx[(j//6)]+2*k-31+1, rowy[(j//6)]-2, (note_tick[i]//32)*8+init_z+4+1, prismarine_slab)
                                reg.setblock(rowx[(j//6)]+2*k-31, rowy[(j//6)], (note_tick[i]//32)*8+init_z+4, redstone)
                                
                            if j % 6 == 4:
                                reg.setblock(rowx[(j//6)]+2*k-31+1, rowy[(j//6)], (note_tick[i]//32)*8+init_z+4-1, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                                reg.setblock(rowx[(j//6)]+2*k-31+1, rowy[(j//6)]-1, (note_tick[i]//32)*8+init_z+4-1, noteblock_instruments_BlockState[note_instrument[i]])
                                if note_instrument[i] == 3:
                                    reg.setblock(rowx[(j//6)]+2*k-31+1, rowy[(j//6)]-2, (note_tick[i]//32)*8+init_z+4-1, prismarine_slab)
                                reg.setblock(rowx[(j//6)]+2*k-31, rowy[(j//6)], (note_tick[i]//32)*8+init_z+4, redstone)
                                
                            if j % 6 == 5:
                                reg.setblock(rowx[(j//6)]+2*k-31+2, rowy[(j//6)], (note_tick[i]//32)*8+init_z+4, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                                reg.setblock(rowx[(j//6)]+2*k-31+2, rowy[(j//6)]-1, (note_tick[i]//32)*8+init_z+4, noteblock_instruments_BlockState[note_instrument[i]])
                                if note_instrument[i] == 3:
                                    reg.setblock(rowx[(j//6)]+2*k-31+2, rowy[(j//6)]-2, (note_tick[i]//32)*8+init_z+4, prismarine_slab)
                                reg.setblock(rowx[(j//6)]+2*k-31, rowy[(j//6)], (note_tick[i]//32)*8+init_z+4, redstone)
                                
                    if (note_tick[i]-3) % 32 == 2*k:
                        if k > 7 and k < 16:
                            reg.setblock(rowx[(j//6)]+2*k-31, rowy[(j//6)]-2, ((note_tick[i]-3)//32)*8+init_z+4, sticky_piston)
                            reg.setblock(rowx[(j//6)]+2*k-31, rowy[(j//6)]-3, ((note_tick[i]-3)//32)*8+init_z+4, redstone_block)
                            reg.setblock(rowx[(j//6)]+2*k-31, rowy[(j//6)]-5, ((note_tick[i]-3)//32)*8+init_z+4, redstone)
                            reg.setblock(rowx[(j//6)]+2*k-31, rowy[(j//6)]-6, ((note_tick[i]-3)//32)*8+init_z+4, prismarine_slab)
                            if j % 6 == 0:
                                reg.setblock(rowx[(j//6)]+2*k-31, rowy[(j//6)]-5, ((note_tick[i]-3)//32)*8+init_z+4+1, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                                reg.setblock(rowx[(j//6)]+2*k-31, rowy[(j//6)]-6, ((note_tick[i]-3)//32)*8+init_z+4+1, noteblock_instruments_BlockState[note_instrument[i]])
                                if note_instrument[i] == 3:
                                    reg.setblock(rowx[(j//6)]+2*k-31, rowy[(j//6)]-7, ((note_tick[i]-3)//32)*8+init_z+4+1, prismarine_slab)
                                reg.setblock(rowx[(j//6)]+2*k-31, rowy[(j//6)]-5, ((note_tick[i]-3)//32)*8+init_z+4, redstone)
                                
                            if j % 6 == 1:
                                reg.setblock(rowx[(j//6)]+2*k-31, rowy[(j//6)]-5, ((note_tick[i]-3)//32)*8+init_z+4-1, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                                reg.setblock(rowx[(j//6)]+2*k-31, rowy[(j//6)]-6, ((note_tick[i]-3)//32)*8+init_z+4-1, noteblock_instruments_BlockState[note_instrument[i]])
                                if note_instrument[i] == 3:
                                    reg.setblock(rowx[(j//6)]+2*k-31, rowy[(j//6)]-7, ((note_tick[i]-3)//32)*8+init_z+4-1, prismarine_slab)
                                reg.setblock(rowx[(j//6)]+2*k-31, rowy[(j//6)]-5, ((note_tick[i]-3)//32)*8+init_z+4, redstone)
                                
                            if j % 6 == 2:
                                reg.setblock(rowx[(j//6)]+2*k-31, rowy[(j//6)]-5, ((note_tick[i]-3)//32)*8+init_z+4+2, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                                reg.setblock(rowx[(j//6)]+2*k-31, rowy[(j//6)]-6, ((note_tick[i]-3)//32)*8+init_z+4+2, noteblock_instruments_BlockState[note_instrument[i]])
                                if note_instrument[i] == 3:
                                    reg.setblock(rowx[(j//6)]+2*k-31, rowy[(j//6)]-7, ((note_tick[i]-3)//32)*8+init_z+4+2, prismarine_slab)
                                reg.setblock(rowx[(j//6)]+2*k-31, rowy[(j//6)]-5, ((note_tick[i]-3)//32)*8+init_z+4, redstone)
                                
                            if j % 6 == 3:
                                reg.setblock(rowx[(j//6)]+2*k-31, rowy[(j//6)]-5, ((note_tick[i]-3)//32)*8+init_z+4-2, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                                reg.setblock(rowx[(j//6)]+2*k-31, rowy[(j//6)]-6, ((note_tick[i]-3)//32)*8+init_z+4-2, noteblock_instruments_BlockState[note_instrument[i]])
                                if note_instrument[i] == 3:
                                    reg.setblock(rowx[(j//6)]+2*k-31, rowy[(j//6)]-7, ((note_tick[i]-3)//32)*8+init_z+4-2, prismarine_slab)
                                reg.setblock(rowx[(j//6)]+2*k-31, rowy[(j//6)]-5, ((note_tick[i]-3)//32)*8+init_z+4, redstone)
                                
                            if j % 6 == 4:
                                reg.setblock(rowx[(j//6)]+2*k-31+1, rowy[(j//6)]-5, ((note_tick[i]-3)//32)*8+init_z+4+1, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                                reg.setblock(rowx[(j//6)]+2*k-31+1, rowy[(j//6)]-6, ((note_tick[i]-3)//32)*8+init_z+4+1, noteblock_instruments_BlockState[note_instrument[i]])
                                if note_instrument[i] == 3:
                                    reg.setblock(rowx[(j//6)]+2*k-31+1, rowy[(j//6)]-7, ((note_tick[i]-3)//32)*8+init_z+4+1, prismarine_slab)
                                reg.setblock(rowx[(j//6)]+2*k-31, rowy[(j//6)]-5, ((note_tick[i]-3)//32)*8+init_z+4, redstone)
                                
                            if j % 6 == 5:
                                reg.setblock(rowx[(j//6)]+2*k-31+1, rowy[(j//6)]-5, ((note_tick[i]-3)//32)*8+init_z+4-1, BlockState('minecraft:note_block', {'instrument' : noteblock_instruments[note_instrument[i]], 'note' : noteblock_keys[note_key[i]-33]}))
                                reg.setblock(rowx[(j//6)]+2*k-31+1, rowy[(j//6)]-6, ((note_tick[i]-3)//32)*8+init_z+4-1, noteblock_instruments_BlockState[note_instrument[i]])
                                if note_instrument[i] == 3:
                                    reg.setblock(rowx[(j//6)]+2*k-31+1, rowy[(j//6)]-7, ((note_tick[i]-3)//32)*8+init_z+4-1, prismarine_slab)
                                reg.setblock(rowx[(j//6)]+2*k-31, rowy[(j//6)]-5, ((note_tick[i]-3)//32)*8+init_z+4, redstone)
                                

print("layer_maximum = ",layer_maximum)

################################
####################
##########

#save .litematic file

schem.save(file_name + ".litematic")