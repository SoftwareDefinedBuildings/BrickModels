from rdflib import Graph, Namespace, URIRef, Literal
import rdflib
import json
import random
import re
RDF = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
RDFS = Namespace('http://www.w3.org/2000/01/rdf-schema#')
OWL = Namespace('http://www.w3.org/2002/07/owl#')
BRICK = Namespace('https://brickschema.org/schema/1.0.1/Brick#')
BF = Namespace('https://brickschema.org/schema/1.0.1/BrickFrame#')
BRICKTAG = Namespace('https://brickschema.org/schema/1.0.1/BrickTag#')
SDH = Namespace('http://buildsys.org/ontologies/sutardja_dai_hall#')
g = rdflib.Graph()
g.bind('rdf', RDF)
g.bind('rdfs', RDFS)
g.bind('brick', BRICK)
g.bind('bf', BF)
g.bind('btag', BRICKTAG)
g.bind('sdh', SDH)



#####################################
##
## Spatial Structure: Floors + Rooms
##
#####################################

# add floors + rooms
flr2rm = {
    "Floor1": {
                '132': 'Mech Steam',
                '148': 'Laser Lab',
                '170': 'Elevator Lobby',
                '149': 'MDC Mech',
                '171': 'Riser Closet',
                '175': 'Electrical',
                '177': 'Womens Bath',
                '160': 'Corridor',
                '168': 'Plumbing',
                '148': 'Laser Lab'
              },
    "Floor2": {
                '212': 'Vestibule',
                '222': 'Womens Bath',
                '238': 'Breakout',
                '240': 'Classroom',
                '250': 'Classroom',
                '270': 'Elevator Lobby',
                '271': 'Riser Closet',
                '275': 'Electrical',
                '266C': 'Office',
                '260': 'Hallway',
                '266': 'Receiving',
                '277': 'Mens Bath',
                '210': 'Cybercafe',
                '214': 'Kitchen',
                '200': 'Computer Lab',
              },
    "Floor3": {
                '300': 'Prelobby',
                '330F': 'Office',
                '330E': 'Office',
                '330C': 'Office',
                '330B': 'Office',
                '310': 'Auditorium',
                '330': 'Learning',
                '340': 'Lobby',
                '370': 'Elevator Lobby',
                '371': 'IDF Closet',
                '375': 'Electrical',
                '345': 'Display',
                '356D': 'Open Office',
                '377': 'Womens Bath',
                '356F': 'Office',
                '361': 'Exit Passage',
                '368': 'Conference',
              },
    "Floor4": {
                '410': 'Hallway',
                '413': 'Office',
                '430': 'Pantry',
                '432': 'Open Office',
                '434': 'Open Office',
                '440': 'Open Office',
                '446': 'Office',
                '444': 'Office',
                '442': 'Office',
                '421': 'Office',
                '419': 'Office',
                '417': 'Office',
                '415': 'Office',
                '424': 'Office',
                '426': 'Office',
                '422': 'Office',
                '418': 'Storage',
                '410': 'Hallway',
                '423': 'Office',
                '425': 'Office',
                '452': 'Office',
                '454': 'Office',
                '456': 'Office',
                '448': 'Office',
                '427': 'Emergency Elec',
                '470': 'Elevator Lobby',
                '450': 'Open Office',
                '471': 'Riser',
                '458': 'Conference',
                '464': 'Office',
                '462': 'Copy Room',
                '475': 'Elec',
                '460': 'Open Office',
                '468': 'Open Office',
                '479': "Men's Bathroom",
                '477': "Women's Bathroom",
                '466': 'Open Office',
                '468': 'Open Office',
                '472': 'Lobby',
               },
    "Floor5": {
                '510': 'Office',
                '511': 'Office',
                '532': 'Open Office',
                '538': 'Open Office',
                '515': 'Office',
                '548': 'Open Office',
                '520': 'Microfab Office',
                '500': 'Hallway',
                '520C': 'Microfab Office',
                '570': 'Elevator Lobby',
                '550': 'Open Office',
                '548': 'Open Office',
                '554': 'Conference Room',
                '571': 'Riser Closet',
                '558': 'Office',
                '575': 'Electrical',
                '568': 'Open Office',
                '577': 'Womens Bath',
                '566': 'Open Office',
                '568': 'Open Office',
              },
    "Floor6": {
                '630': 'Conference',
                '640': 'Office',
                '646': 'Office',
                '630B': 'Pantry',
                '630A': 'Lounge',
                '621C': 'Office',
                '621A': 'Office',
                '621': 'Open Research',
                '629': 'Emergency Electrical',
                '670': 'Elevator Lobby',
                '652': 'Cubicles',
                '652A': 'Office',
                '671': 'IDF Closet',
                '656B': 'Office',
                '675': 'Electrical',
                '656': 'Cubicles',
                '677': 'Womens Bath',
                '650': 'Hallway',
                '668': 'Research',
              },
    "Floor7": {
                '736': 'Open Office',
                '730': 'Conference',
                '738': 'Open Office',
                '725': 'Office',
                '721': 'Office',
                '770': 'Elevator Lobby',
                '722': 'Office',
                '750': 'Open Office',
                '771': 'Riser Closet',
                '775': 'Electrical',
                '756': 'Office',
                '766': 'Office',
                '777': 'Womens Bath',
                '768': 'Open Office',
              },
}

for floor, roomlist in flr2rm.items():
    g.add((SDH[floor], RDF.type, BRICK.Floor))
    for room, label in roomlist.items():
        room = 'R'+room
        g.add((SDH[room], RDF.type, BRICK.Room))
        g.add((SDH[room], BF.isPartOf, SDH[floor]))
        g.add((SDH[room], RDFS.label, Literal(label)))

#####################################
##
## Air Handling Units
##
#####################################

# instantiate the AHUs themselves
g.add((SDH['AH1'], RDF.type, BRICK.Air_Handler_Unit))
g.add((SDH['AH2A'], RDF.type, BRICK.Air_Handler_Unit))
g.add((SDH['AH2B'], RDF.type, BRICK.Air_Handler_Unit))

# add points to AHUs
import generate_ahu
for r in generate_ahu.g:
    g.add(r)

#####################################
##
## Chillers
##
#####################################

# We have 2 chillers: CH1, CH2.


#####################################
##
## VAVs with Reheat (nano fab lab)
##
#####################################

# create the class
g.add((BRICK.VAV_With_Reheat, RDF.type, OWL.Class))
g.add((BRICK.VAV_With_Reheat, RDFS.subClassOf, BRICK.VAV))

# the JSON files groups all RAH VAV points together,
# so we just loop through this file and generate the RAH VAV
# and its points as we go along.
rah_points = json.load(open('rah_points.json'))
for doc in rah_points:
    description = doc.pop('Description')
    pointname = doc.keys()[0]
    uuid = doc[pointname]
    rah = re.match(r'.*(RAH[0-9]+).*', pointname)
    g.add((SDH[rah], RDF.type, BRICK.VAV_With_Reheat))
    if rah is None: continue
    rah = rah.groups()[0]
    rah_room = re.match(r'.*RAH[0-9]+_([0-9]+).*', pointname)
    if rah_room is not None:
        roomname = 'R' + rah_room.groups()[0]
        # if the pointname contains a room identifier, then
        # we add that room to a zone and associate the RVAV
        zone = 'Zone_{0}'.format(rah)
        g.add((SDH[zone], RDF.type, BRICK.HVAC_Zone))
        g.add((SDH[rah], BF.feeds, SDH[zone]))
        g.add((SDH[roomname], RDF.type, BRICK.Room))
        g.add((SDH[zone], BF.hasPart, SDH[roomname]))

    if description == "CFM":
        klass = BRICK.Air_Flow_Sensor
    elif description == "CFM SETPOINT":
        klass = BRICK.Air_Flow_Setpoint
    elif description == "COOLING COIL VLV":
        klass = BRICK.Cooling_Valve_Command
    elif description == "OCCUPIED":
        klass = BRICK.Occupancy_Sensor
    elif description == "SAT SETPOINT":
        klass = BRICK.Supply_Air_Temperature_Setpoint
    elif description == "SF SPEED":
        klass = BRICK.Supply_Fan_VFD_Speed
    elif description == "SUPPLY AIR TEMP":
        klass = BRICK.Supply_Air_Temperature_Sensor
    elif description == "TEMP STPT":
        klass = BRICK.Temperature_Setpoint
    else:
        continue
    g.add((SDH[pointname], RDF.type, klass))
    g.add((SDH[rah], BF.hasPoint, SDH[pointname]))
    g.add((SDH[pointname], BF.uuid, Literal(uuid)))


#####################################
##
## RHC (Reheat coil points)
## NOTE: These are associated with AH1A/B and are probably related to the RVAVs, but
## I'm not sure what the exact associations are, so I'm just connecting these to the AHU
##
#####################################

for i in range(1,10):
    rhc = 'RHC-{0}'.format(i)
    g.add((SDH[rhc], RDF.type, BRICK.Reheat_Coil))
    g.add((SDH['AH1'], BF.hasPart, SDH[rhc]))

rhc_points = json.load(open('rhc_point.json'))
for pname, uuid in rhc_points.items():
    rhc = re.match(r'.*(RHC-[0-9]).*', pname).groups()[0]
    point = pname.split(':')[1]
    # TODO: what room is this a temperature setpoint for?
    if point == 'CTL STPT':
        klass = BRICK.Temperature_Setpoint
    elif point == 'HEAT.COOL':
        klass = BRICK.Heating_Command
    # TODO: find out what room this is measuring
    elif point == 'ROOM TEMP':
        klass = BRICK.Zone_Air_Temperature_Sensor
    else:
        print(point)
        continue
    name = (rhc+point).replace(' ','_')
    g.add((SDH[name], RDF.type, klass))
    g.add((SDH[rhc], BF.hasPoint, SDH[name]))
    g.add((SDH[name], BF.uuid, Literal(uuid)))

#####################################
##
## Office VAVs
## Note: be aware of constant volume terminal units
##
#####################################

# generate all of the labels
s1vavs = ['S1-{:02d}'.format(i) for i in range(1,21)]
s2vavs = ['S2-{:02d}'.format(i) for i in range(1,22)]
s3vavs = ['S3-{:02d}'.format(i) for i in range(1,22)]
s4vavs = ['S4-{:02d}'.format(i) for i in range(1,22)]
s5vavs = ['S5-{:02d}'.format(i) for i in range(1,22)]
s6vavs = ['S6-{:02d}'.format(i) for i in range(1,21)]
s7vavs = ['S7-{:02d}'.format(i) for i in range(1,17)]

# instantiate them
for vavlabel in s1vavs+s2vavs+s3vavs+s4vavs+s5vavs+s6vavs+s7vavs:
    zone = 'Zone{0}'.format(vavlabel)
    g.add((SDH[vavlabel], RDF.type, BRICK.VAV))
    g.add((SDH[zone], RDF.type, BRICK.HVAC_Zone))
    g.add((SDH[vavlabel], BF.feeds, SDH[zone]))

# add points to the vavs
vavsensors = json.load(open('vavsensors.json'))
# TODO: where are the temperature sensors?
for sensor in vavsensors:
    vav = sensor.pop('vav')
    name = sensor.keys()[0]
    uuid = sensor.values()[0]
    pointname = vav+name.replace(' ','_')
    if name == "room temperature":
        print pointname
        klass = BRICK.Zone_Air_Temperature_Sensor
    elif name == "room airflow":
        klass = BRICK.Supply_Air_Flow_Sensor
    elif name == "room damper position":
        klass = BRICK.Damper_Position_Sensor
        # damper!
        g.add((SDH[vav+"damper"], RDF.type, BRICK.Damper))
        g.add((SDH[vav], BF.hasPart, SDH[vav+"damper"]))
        g.add((SDH[vav+"damper"], BF.hasPoint, SDH[pointname]))
    elif name == "room heating":
        klass = BRICK.Zone_Heating_Temperature_Setpoint
    elif name == "room cooling":
        klass = BRICK.Zone_Cooling_Temperature_Setpoint
    elif name == "room maximum airflow":
        klass = BRICK.Max_Supply_Air_Flow_Setpoint
    elif name == "room minimum airflow":
        klass = BRICK.Min_Supply_Air_Flow_Setpoint
    elif name == "room setpoint":
        klass = BRICK.Zone_Temperature_Setpoint
    elif name == "room valve position":
        klass = BRICK.Heating_Valve_Command
    else:
        print(name)
        continue
    g.add((SDH[pointname], RDF.type, klass))
    g.add((SDH[vav], BF.hasPoint, SDH[pointname]))
    g.add((SDH[pointname], BF.uuid, Literal(uuid)))

# associate the VAVs with the AH2A/B air handlers.
# The 2 AHUs for the office space operate in parallel
ahu2vav={'AH2A': [], 'AH2B': []}
ahu2vav['AH2A'].extend(s1vavs)
ahu2vav['AH2A'].extend(s2vavs)
ahu2vav['AH2A'].extend(s3vavs)
ahu2vav['AH2A'].extend(s4vavs)
ahu2vav['AH2A'].extend(s5vavs)
ahu2vav['AH2A'].extend(s6vavs)
ahu2vav['AH2A'].extend(s7vavs)

ahu2vav['AH2B'].extend(s1vavs)
ahu2vav['AH2B'].extend(s2vavs)
ahu2vav['AH2B'].extend(s3vavs)
ahu2vav['AH2B'].extend(s4vavs)
ahu2vav['AH2B'].extend(s5vavs)
ahu2vav['AH2B'].extend(s6vavs)
ahu2vav['AH2B'].extend(s7vavs)

for ahu, vavlist in ahu2vav.items():
    g.add((SDH[ahu], RDF.type, BRICK.AHU))
    for vav in vavlist:
        g.add((SDH[ahu], BF.feeds, SDH[vav]))


#####################################
##
## Map HVAC zones to rooms for the office space
##
#####################################

zone2room = {
    'ZoneS1-01': ['132'],
    'ZoneS1-02': ['148'],
    'ZoneS1-03': ['170'],
    'ZoneS1-04': ['149'],
    'ZoneS1-05': ['171'],
    'ZoneS1-06': ['175'],
    'ZoneS1-07': ['177'],
    'ZoneS1-08': ['160'],
    'ZoneS1-09': ['168'],
    'ZoneS1-10': ['148'],

    'ZoneS2-01': ['212'],
    'ZoneS2-02': ['212'],
    'ZoneS2-03': ['222'],
    'ZoneS2-04': ['238'],
    'ZoneS2-05': ['240'],
    'ZoneS2-06': ['250'],
    'ZoneS2-07': ['270'],
    'ZoneS2-08': ['271'],
    'ZoneS2-09': ['275'],
    'ZoneS2-10': ['266C'],
    'ZoneS2-11': ['254'],
    'ZoneS2-12': ['260'],
    'ZoneS2-13': ['266'],
    'ZoneS2-14': ['277'],
    'ZoneS2-15': ['210'],
    'ZoneS2-16': ['210'],
    'ZoneS2-17': ['210'],
    'ZoneS2-18': ['214'],
    'ZoneS2-19': ['200'],
    'ZoneS2-20': ['200'],
    'ZoneS2-21': ['200'],

    'ZoneS3-01': ['300'],
    'ZoneS3-02': ['306'],
    'ZoneS3-03': ['330F'],
    'ZoneS3-04': ['330E'],
    'ZoneS3-05': ['330C'],
    'ZoneS3-06': ['330B'],
    'ZoneS3-07': ['310'],
    'ZoneS3-08': ['330'],
    'ZoneS3-09': ['310'],
    'ZoneS3-10': ['340'],
    'ZoneS3-11': ['300'],
    'ZoneS3-12': ['370'],
    'ZoneS3-13': ['371'],
    'ZoneS3-14': ['375'],
    'ZoneS3-15': ['345'],
    'ZoneS3-16': ['356D'],
    'ZoneS3-17': ['356'],
    'ZoneS3-18': ['377'],
    'ZoneS3-19': ['356F'],
    'ZoneS3-20': ['361'],
    'ZoneS3-21': ['368'],

    'ZoneS4-01': ['410','413'],
    'ZoneS4-02': ['430','432','432'],
    'ZoneS4-03': ['434'],
    'ZoneS4-04': ['440','432'],
    'ZoneS4-05': ['446','444','442'],
    'ZoneS4-06': ['421','419','417','415'],
    'ZoneS4-07': ['424','426','422','418','410'],
    'ZoneS4-08': ['423','425'],
    'ZoneS4-09': ['452','454','456','448'],
    'ZoneS4-10': ['427'],
    'ZoneS4-11': ['470'],
    'ZoneS4-12': ['450'],
    'ZoneS4-13': ['450'],
    'ZoneS4-14': ['471'],
    'ZoneS4-15': ['458'],
    'ZoneS4-16': ['464','462'],
    'ZoneS4-17': ['475'],
    'ZoneS4-18': ['460','468'],
    'ZoneS4-19': ['479','477'],
    'ZoneS4-20': ['466'],
    'ZoneS4-21': ['468','472'],

    'ZoneS5-01': ['510'],
    'ZoneS5-02': ['511'],
    'ZoneS5-03': ['532'],
    'ZoneS5-04': ['532'],
    'ZoneS5-05': ['538'],
    'ZoneS5-06': ['515'],
    'ZoneS5-07': ['548'],
    'ZoneS5-08': ['520'],
    'ZoneS5-09': ['500'],
    'ZoneS5-00': ['520C'],
    'ZoneS5-11': ['570'],
    'ZoneS5-12': ['550'],
    'ZoneS5-13': ['548'],
    'ZoneS5-14': ['554'],
    'ZoneS5-15': ['571'],
    'ZoneS5-16': ['558'],
    'ZoneS5-17': ['575'],
    'ZoneS5-18': ['568'],
    'ZoneS5-19': ['577'],
    'ZoneS5-20': ['566'],
    'ZoneS5-21': ['568'],

    'ZoneS6-01': ['630'],
    'ZoneS6-02': ['640'],
    'ZoneS6-03': ['646'],
    'ZoneS6-04': ['630B'],
    'ZoneS6-05': ['630A'],
    'ZoneS6-06': ['621C'],
    'ZoneS6-07': ['621A'],
    'ZoneS6-08': ['621'],
    'ZoneS6-09': ['629'],
    'ZoneS6-00': ['621'],
    'ZoneS6-11': ['670'],
    'ZoneS6-12': ['652'],
    'ZoneS6-13': ['652A'],
    'ZoneS6-14': ['671'],
    'ZoneS6-15': ['656B'],
    'ZoneS6-16': ['675'],
    'ZoneS6-17': ['656'],
    'ZoneS6-18': ['677'],
    'ZoneS6-19': ['650'],
    'ZoneS6-20': ['668'],

    'ZoneS7-01': ['736'],
    'ZoneS7-02': ['730'],
    'ZoneS7-03': ['738'],
    'ZoneS7-04': ['738'],
    'ZoneS7-05': ['725'],
    'ZoneS7-06': ['721'],
    'ZoneS7-07': ['770'],
    'ZoneS7-08': ['722'],
    'ZoneS7-09': ['750'],
    'ZoneS7-00': ['750'],
    'ZoneS7-11': ['771'],
    'ZoneS7-12': ['775'],
    'ZoneS7-13': ['756'],
    'ZoneS7-14': ['766'],
    'ZoneS7-15': ['777'],
    'ZoneS7-16': ['768'],
}

for zonename, roomlist in zone2room.items():
    for room in roomlist:
        room = 'R'+room
        g.add((SDH[zonename], BF.hasPart, SDH[room]))


#####################################
##
## Room Temperature Sensors
##
#####################################

## Records look like the following
#    {
#        "Description": "310 AUDITORIUM",
#        "Metadata": {
#            "Extra": {
#                "Type": "room temperature",
#                "Vav": "S3-09"
#            },

for record in json.load(open('metadata.json')):
    pointname = record.get('Metadata',{}).get('Extra',{}).get('Type')
    vav = record.get('Metadata',{}).get('Extra',{}).get('Vav')
    description = record.get('Description','')
    uuid = record.get('uuid')
    if pointname is None or vav is None or pointname != 'room temperature':
        continue
    room = re.match(r'([0-9]+) .*', description)
    if room is None:
        continue
    room = 'R'+room.groups()[0]
    name = vav+pointname.replace(' ','_')
    print vav, room, name
    g.add((SDH[name], BF.isLocatedIn, SDH[room]))
    g.add((SDH[name], BF.isPointOf, SDH[room]))

#adjacencies = {
#    "511" :["510","513"],
#    "513" :["511","515"],
#    "515" :["513"],
#    "510" :["511","530"],
#    "530" :["510"],
#    "520" :["520A","520B," "520C," "520D", "532"],
#    "520A":["520","520B"],
#    "520B":["520","520A"],
#    "520C":["520"],
#    "520D":["520"],
#    "532" :["520","538"],
#    "538" :["532"],
#    "548" :["520C"],
#    "552" :["548","554"],
#    "554" :["552","556"],
#    "556" :["554","558"],
#    "558" :["556","562"],
#    "562" :["558","564"],
#    "564" :["562","566"],
#    "566" :["564"],
#    "571" :["573"],
#    "573" :["571","575"],
#    "575" :["573","577"],
#    "577" :["575","579"],
#    "579" :["577"],
#    "580" :["581","582A"],
#    "581" :["580","582A", "582"],
#    "582" :["581","583", "582A"],
#    "582A":["582","581", "580", "591"],
#    "583" :["582","582A", "584", "593"],
#    "584" :["583","585"],
#    "585" :["584","586", "595"],
#    "586" :["585","599", "597"],
#    "599" :["597","586"],
#    "597" :["599","586"],
#    "595" :["585","586", "584"],
#    "593" :["583"],
#    "591" :["582A","580"],
#    "630A":["630B","621E","630"],
#    "630":["630A"],
#    "621E":["630B","630A","621D"],
#    "630B":["621E","630A"],
#    "621D":["621E","621C","621"],
#    "621C":["621D","621B","621"],
#    "621B":["621C","621A","621"],
#    "621A":["621B","621"],
#    "621":["621A","621B","621C","621D","621E"],
#    "671":["673"],
#    "673":["671","675"],
#    "675":["673","677"],
#    "677":["675","679"],
#    "679":["677"],
#    "640":["642"],
#    "642":["640","644"],
#    "644":["642","646"],
#    "646":["644","648"],
#    "648":["646","652A"],
#    "652A":["652","652B"],
#    "652":["652A","652B"],
#    "652B":["652A","652","656A"],
#    "656A":["652B","656","656B"],
#    "656":["652","656A","656B","664"],
#    "656B":["656A","656","666"],
#    "664":["656","666"],
#    "666":["656B","664"],
#    "730":["732","717"],
#    "732":["730","736"],
#    "717":["730","719"],
#    "719":["717","721","718"],
#    "721":["719","723","722"],
#    "723":["721","725","724"],
#    "725":["723","726"],
#    "718":["722","719"],
#    "722":["718","724","721"],
#    "724":["722","726","723"],
#    "726":["724","725"],
#    "736":["732","738"],
#    "738":["736","748","746"],
#    "746":["738","748","754"],
#    "748":["752","746","738"],
#    "752":["748","754","750"],
#    "754":["752","746","750"],
#    "750":["752","754","771","773","775","768"],
#    "771":["773","750"],
#    "773":["771","775","750"],
#    "775":["773","750","777"],
#    "777":["775","779","768"],
#    "779":["777","768"],
#    "768":["750","777","779"],
#}
#for room, adjlist in adjacencies.items():
#    room = 'R'+room
#    for neighbor in adjlist:
#        neighbor = 'R'+neighbor
#        g.add((SDH[room], BF.adjacentTo, SDH[neighbor]))
#
#adjacencies = {
#    '413': {
#            'air': [],
#            'door': ['410'],
#            'wall': ['415'],
#           },
#    '415': {
#            'air': [],
#            'door': ['410'],
#            'wall': ['413','417'],
#           },
#    '417': {
#            'air': [],
#            'door': ['410'],
#            'wall': ['415','419'],
#           },
#    '419': {
#            'air': [],
#            'door': ['410'],
#            'wall': ['417','421'],
#           },
#    '421': {
#            'air': [],
#            'door': ['410'],
#            'wall': ['419','423'],
#           },
#
#    '423': {
#            'air': [],
#            'door': ['410'],
#            'wall': ['421','425'],
#           },
#
#    '425': {
#            'air': [],
#            'door': ['410'],
#            'wall': ['423','470'],
#           },
#    '418': {
#            'air': [],
#            'door': ['410'],
#            'wall': ['422','440','450'],
#           },
#    '422': {
#            'air': [],
#            'door': ['410'],
#            'wall': ['418','424','440','450'],
#           },
#    '424': {
#            'air': [],
#            'door': ['410'],
#            'wall': ['422','426','440','450'],
#           },
#    '426': {
#            'air': [],
#            'door': ['410'],
#            'wall': ['424','470','440','450'],
#           },
#    '427': {
#            'air': [],
#            'door': ['470'],
#            'wall': [],
#           },
#    '430': {
#            'air': [],
#            'door': ['432'],
#            'wall': ['410'],
#    },
#    '432': {
#            'air': ['440','434'],
#            'door': ['430'],
#            'wall': [],
#           },
#    '434': {
#            'air': ['432','440'],
#            'door': [],
#            'wall': ['442'],
#           },
#    '440': {
#            'air': ['432','434','450'],
#            'door': ['442','444','446','448'],
#            'wall': ['418','422','424','426'],
#           },
#    '442': {
#            'air': [],
#            'door': ['440'],
#            'wall': ['434','444'],
#           },
#    '444': {
#            'air': [],
#            'door': ['440'],
#            'wall': ['442','446'],
#           },
#    '446': {
#            'air': [],
#            'door': ['440'],
#            'wall': ['444','448'],
#           },
#    '448': {
#            'air': [],
#            'door': ['440'],
#            'wall': ['446','452','450'],
#           },
#    '450': {
#            'air': ['440','460'],
#            'door': ['470','448','452','454','456','458','462','471','473','475'],
#            'wall': ['418','422','424','426'],
#           },
#    '452': {
#            'air': [],
#            'door': ['450'],
#            'wall': ['448','454'],
#           },
#    '454': {
#            'air': [],
#            'door': ['450'],
#            'wall': ['452','456'],
#           },
#    '456': {
#            'air': [],
#            'door': ['450'],
#            'wall': ['454','458'],
#           },
#    '458': {
#            'air': [],
#            'door': ['450'],
#            'wall': ['456','462'],
#           },
#    '460': {
#            'air': ['450','468','466'],
#            'door': ['479','477','462','464'],
#            'wall': [],
#           },
#    '462': {
#            'air': [],
#            'door': ['460','450'],
#            'wall': ['458','464'],
#           },
#    '464': {
#            'air': [],
#            'door': ['460'],
#            'wall': ['462','466'],
#           },
#    '466': {
#            'air': ['460','468'],
#            'door': [],
#            'wall': ['464'],
#           },
#    '468': {
#            'air': ['460','466'],
#            'door': ['472'],
#            'wall': [],
#           },
#    '470': {
#            'air': [],
#            'door': ['427','450','410'],
#            'wall': ['425','426'],
#    },
#    '471': {
#            'air': [],
#            'door': ['450'],
#            'wall': ['473'],
#           },
#    '472': {
#            'air': [],
#            'door': ['468'],
#            'wall': [],
#           },
#    '473': {
#            'air': [],
#            'door': ['450'],
#            'wall': ['471','475'],
#           },
#    '475': {
#            'air': [],
#            'door': ['450'],
#            'wall': ['479','473'],
#           },
#    '479': {
#            'air': [],
#            'door': ['460'],
#            'wall': ['475','477'],
#           },
#    '477': {
#            'air': [],
#            'door': ['460'],
#            'wall': ['479'],
#           },
#    '410': {
#            'air': [],
#            'door': ['413','415','417','419','421','423','425','418','422','424','426','470'],
#            'wall': ['430'],
#    },
#}
#
#for room, neighbors in adjacencies.items():
#    room = 'R' + room
#    for nb in neighbors['air']:
#        nb = 'R' + nb
#        g.add((SDH[room], BF.adjacentTo, SDH[nb]))
#    for nb in neighbors['door']:
#        nb = 'R' + nb
#        g.add((SDH[room], BF.adjacentTo, SDH[nb]))
#    for nb in neighbors['wall']:
#        nb = 'R' + nb
#        g.add((SDH[room], BF.adjacentTo, SDH[nb]))

g.serialize(destination='sdh.ttl',format='turtle')
print(len(g))
