import cc_dat_utils
import json
import cc_classes

#Part 3
##Load your custom JSON file
input_json_file = "data/xluo1_cc1.json"

with open(input_json_file, "r") as reader:
    game_json_data = json.load(reader)


## Make functions to convert JSON data to CCLevelPack

def get_levels(data):
    levels = data["levels"]
    levelList = []
    for level in levels:
        levelList.append(level)
    
    return levelList

def get_maptitle(level):
    title = cc_classes.CCMapTitleField(level['optional_fields']['map title'])
    return title
    
def get_password(level):
    password = cc_classes.CCEncodedPasswordField(level['optional_fields']['encoded password'])
    return password
    
def get_hint(level):
    hint_text = level['optional_fields']['hint text']
    if hint_text != None:
        hint = cc_classes.CCMapHintField(level['optional_fields']['hint text'])
    else:
        hint = None
    return hint

    
def get_monstermovement(level):
    list_of_coords = level['optional_fields']['moving objects']
    if list_of_coords == None:
        movement = None
    else:
        
        movementList = []
        for coordinate in list_of_coords:
            coordObj = cc_classes.CCCoordinate(coordinate[0],coordinate[1])
            movementList.append(coordObj)
        movement = cc_classes.CCMonsterMovementField(movementList)
        
    return movement

def get_layer(level):
    small_layer =  level['upper_layer']
    num_zeroes = 1024 - len(small_layer)
    add_zeroes = [0]*num_zeroes
    small_layer.extend(add_zeroes)
    layer = small_layer

    return layer


## Make function that calls all functions in order

def get_cclevelpack(data):
    levelList = get_levels(data)
    levelPack = cc_classes.CCLevelPack()
    
    for level in levelList:
        # parse map title
        mapTitle = get_maptitle(level)
        # parse encoded PW
        password = get_password(level)
        # parse hint
        hint = get_hint(level)
        # parse monster movement
        movement = get_monstermovement(level)
        # put in a cclevel object
        level_instance = cc_classes.CCLevel()
        level_instance.level_number = level['level_number']
        level_instance.time = level['time']
        level_instance.num_chips = level['chip_number']
        level_instance.upper_layer = get_layer(level)
        
        # put in optional fields
        level_instance.add_field(mapTitle)
        level_instance.add_field(password)
        
        if hint != None:
            level_instance.add_field(hint)
        if movement != None:
            level_instance.add_field(movement)
        
        levelPack.add_level(level_instance)
        
     
        
    return levelPack

levelPack = get_cclevelpack(game_json_data)    

#Save converted data to DAT file
cc_dat_utils.write_cc_level_pack_to_dat(levelPack,"xluo_cc1.dat")