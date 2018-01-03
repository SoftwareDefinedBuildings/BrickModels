from rdflib import Graph, Namespace, URIRef, Literal
import rdflib
import re
from xbos.services.brick import Generator

RDF = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
RDFS = Namespace('http://www.w3.org/2000/01/rdf-schema#')
BRICK = Namespace('https://brickschema.org/schema/1.0.1/Brick#')
BRICKFRAME = Namespace('https://brickschema.org/schema/1.0.1/BrickFrame#')
BF = BRICKFRAME
OWL = Namespace('http://www.w3.org/2002/07/owl#')
CIEE = Namespace('http://buildsys.org/ontologies/ciee#')

g = rdflib.Graph()
g.bind('rdf', RDF)
g.bind('rdfs', RDFS)
g.bind('brick', BRICK)
g.bind('bf', BRICKFRAME)
g.bind('bldg', CIEE)


BOSSWAVE=True

if BOSSWAVE:
    from bw2dataclient import DataClient
    client = DataClient(archivers=["ucberkeley"])
    generator = Generator(CIEE, client)

# add floors
g.add((CIEE.floor_1, RDF.type, BRICK.Floor))
g.add((CIEE.floor_mezz, RDF.type, BRICK.Floor))
g.add((CIEE.floor_2, RDF.type, BRICK.Floor))

# add rooms
rooms = {
    200: "Women's Bathroom",
    201: "Men's Bathroom",
    203: "Office",
    205: "Office",
    206: "Office",
    207: "Office",
    208: "Conference Room",
    209: "Office",
    210: "Office",
    211: "Office",
    212: "Office",
    213: "Office",
    214: "Office",
    215: "Office",
    216: "Office",
    217: "Office",
    218: "Open Office NorthEast",
    219: "Open Office SouthEast",
    220: "Open Office NorthWest",
    221: "Open Office SouthWest",
    222: "Office",
    223: "Office",
    224: "Office",
    225: "Office",
    226: "Office",
}
for room, label in rooms.items():
    g.add((CIEE['R'+str(room)], RDF.type, BRICK.Room))
    g.add((CIEE['R'+str(room)], RDFS.label, Literal(label)))
    g.add((CIEE['R'+str(room)], BF.isPartOf, CIEE.floor_2))
g.add((CIEE.ServerRoom, RDF.type, BRICK.Room))
g.add((CIEE.ServerRoom, RDF.label, Literal("Server Room")))
g.add((CIEE.floor_mezz, BF.hasPart, CIEE.ServerRoom))

# adjacency
adjacency = {
    200: [201,203],
    201: [200,203],
    203: [200,201,205,206,204],
    204: [203,207,225,208,205,223,225],
    205: [203,206],
    206: [203,205,207],
    207: [203,204,206,208],
    208: [204,207,209],
    209: [208,205,210],
    210: [209,205,211],
    211: [210,212, 205, 219],
    212: [211,213,205,219],
    213: [212, 214, 219, 205],
    214: [213, 215,219],
    215: [214,216,218,219],
    216: [215,217,218],
    217: [216,218],
    218: [217,216,219,220,221],
    219: [218,220,221,215,214,213,212,211],
    220: [218,219,221,224,222,223],
    221: [220,218,219,222,223],
    222: [220,221,222,223,224,225],
    223: [222,220,221,225,204],
    224: [222,220,225],
    225: [224,222,223,204],
    226: [201,224,225,204,203],
}
for room, adjlist in adjacency.items():
    for adjroom in adjlist:
        g.add((CIEE['R'+str(room)], BF.adjacentTo, CIEE['R'+str(adjroom)]))
        g.add((CIEE['R'+str(adjroom)], BF.adjacentTo, CIEE['R'+str(room)]))

# add meter
g.add((BRICK.Building_Electric_Meter, RDF.type, OWL.Class))
g.add((BRICK.Building_Electric_Meter, RDFS.subClassOf, BRICK.Electric_Meter))

#g.add((CIEE.building_meter, RDF.type, BRICK.Building_Electric_Meter))
#g.add((CIEE.building_meter, BF.uri, Literal("ciee/devices/s.eagle/0xd8d5b9000000a110/i.meter")))
#g.add((CIEE.building_meter, BF.uuid, Literal("4d6e251a-48e1-3bc0-907d-7d5440c34bb9")))

meters = {}
result = client.query('select uuid, path where uri like "ciee" and originaluri like "eagle" and name = "demand";')
for doc in result['metadata']:
    print doc
    path = doc['path']
    meter_name = 'building_meter'
    g.add((CIEE[meter_name], RDF.type, BRICK.Building_Electric_Meter))
    g.add((CIEE[meter_name], BF.uuid, Literal(doc['uuid'])))
    urisuffix = re.match(r'[^/]+(/.*/i.meter)', path)
    if urisuffix is not None:
        urisuffix = urisuffix.groups()[0]
    else:
        continue
    print 'Tstat URI: ', urisuffix
    g.add((CIEE[meter_name], BF.uri, Literal("ciee" + urisuffix)))

sensors2rooms = {
    '0029': CIEE.R203,
    '0027': CIEE.R206,
    '005c': CIEE.R207,
    '005d': CIEE.R208,
    '002b': CIEE.R208,
    '002e': CIEE.R209,
    '002a': CIEE.R210,
    '005e': CIEE.R211,
    '005a': CIEE.R212,
    '0060': CIEE.R213,
    '0028': CIEE.R214,
    '002c': CIEE.R215,
    '0022': CIEE.R216,
    '005b': CIEE.R217,
    '0025': CIEE.EastOpen,
}

g.add((BRICK.Illumination_Sensor, RDFS.subClassOf, BRICK.Sensor))
g.add((BRICK.Illumination_Sensor, RDF.type, OWL.Class))
for sensor, room in sensors2rooms.items():
    name = "hamilton_"+sensor
    g.add((CIEE[name]+"_air_temp", RDF.type, BRICK.Zone_Temperature_Sensor))
    g.add((CIEE[name]+"_air_temp", BF.uri, Literal("ciee/sensors/s.hamilton/00126d070000{0}/i.temperature/signal/operative".format(sensor))))
    g.add((CIEE[name]+"_air_temp", BF.isLocatedIn, room))
    g.add((CIEE[name]+"_air_temp", BF.isPointOf, room))

    g.add((CIEE[name]+"_pir", RDF.type, BRICK.Occupancy_Sensor))
    g.add((CIEE[name]+"_pir", BF.uri, Literal("ciee/sensors/s.hamilton/00126d070000{0}/i.temperature/signal/operative".format(sensor))))
    g.add((CIEE[name]+"_pir", BF.isLocatedIn, room))
    g.add((CIEE[name]+"_pir", BF.isPointOf, room))

    g.add((CIEE[name]+"_air_rh", RDF.type, BRICK.Relative_Humidity_Sensor))
    g.add((CIEE[name]+"_air_rh", BF.uri, Literal("ciee/sensors/s.hamilton/00126d070000{0}/i.temperature/signal/operative".format(sensor))))
    g.add((CIEE[name]+"_air_rh", BF.isLocatedIn, room))
    g.add((CIEE[name]+"_air_rh", BF.isPointOf, room))

    g.add((CIEE[name]+"_lux", RDF.type, BRICK.Illumination_Sensor))
    g.add((CIEE[name]+"_lux", BF.uri, Literal("ciee/sensors/s.hamilton/00126d070000{0}/i.temperature/signal/operative".format(sensor))))
    g.add((CIEE[name]+"_lux", BF.isLocatedIn, room))
    g.add((CIEE[name]+"_lux", BF.isPointOf, room))

    if BOSSWAVE:
        uuid = client.uuids('name = "air_temp" and Deployment = "CIEE" and uri like "{0}"'.format(sensor))
        if len(uuid) > 0:
            print uuid
            g.add((CIEE[name]+"_air_temp", BF.uuid, Literal(uuid[0])))

        uuid = client.uuids('name = "presence" and Deployment = "CIEE" and uri like "{0}"'.format(sensor))
        if len(uuid) > 0:
            g.add((CIEE[name]+"_pir", BF.uuid, Literal(uuid[0])))

        uuid = client.uuids('name = "air_rh" and Deployment = "CIEE" and uri like "{0}"'.format(sensor))
        if len(uuid) > 0:
            g.add((CIEE[name]+"_air_rh", BF.uuid, Literal(uuid[0])))

        uuid = client.uuids('name = "lux" and Deployment = "CIEE" and uri like "{0}"'.format(sensor))
        if len(uuid) > 0:
            g.add((CIEE[name]+"_lux", BF.uuid, Literal(uuid[0])))


# add HVAC zones
g.add((CIEE.SouthZone, RDF.type, BRICK.HVAC_Zone))
g.add((CIEE.EastZone, RDF.type, BRICK.HVAC_Zone))
g.add((CIEE.CentralZone, RDF.type, BRICK.HVAC_Zone))
g.add((CIEE.NorthZone, RDF.type, BRICK.HVAC_Zone))

# add HVAC zone/room mapping
g.add((CIEE.SouthZone, BF.hasPart, CIEE.R205))
g.add((CIEE.SouthZone, BF.hasPart, CIEE.R206))
g.add((CIEE.SouthZone, BF.hasPart, CIEE.R207))
g.add((CIEE.SouthZone, BF.hasPart, CIEE.R208))
g.add((CIEE.SouthZone, BF.hasPart, CIEE.R209))
g.add((CIEE.SouthZone, BF.hasPart, CIEE.R210))
g.add((CIEE.SouthZone, BF.hasPart, CIEE.R211))
g.add((CIEE.SouthZone, BF.hasPart, CIEE.R212))

g.add((CIEE.CentralZone, BF.hasPart, CIEE.R218))
g.add((CIEE.CentralZone, BF.hasPart, CIEE.R219))
g.add((CIEE.CentralZone, BF.hasPart, CIEE.R220))
g.add((CIEE.CentralZone, BF.hasPart, CIEE.R221))
g.add((CIEE.CentralZone, BF.hasPart, CIEE.R225))
g.add((CIEE.CentralZone, BF.hasPart, CIEE.R222))
g.add((CIEE.CentralZone, BF.hasPart, CIEE.R223))

g.add((CIEE.EastZone, BF.hasPart, CIEE.R213))
g.add((CIEE.EastZone, BF.hasPart, CIEE.R214))
g.add((CIEE.EastZone, BF.hasPart, CIEE.R215))
g.add((CIEE.EastZone, BF.hasPart, CIEE.R216))
g.add((CIEE.EastZone, BF.hasPart, CIEE.R217))

g.add((CIEE.NorthZone, BF.hasPart, CIEE.R226))
g.add((CIEE.NorthZone, BF.hasPart, CIEE.EastOpen))
g.add((CIEE.NorthZone, BF.hasPart, CIEE.R224))

# add RTU class
g.add((BRICK.RTU, RDFS.subClassOf, BRICK.AHU))
g.add((BRICK.RTU, RDF.type, OWL.Class))

# add RTUs
g.add((CIEE.RTU1, RDF.type, BRICK.RTU))
g.add((CIEE.RTU2, RDF.type, BRICK.RTU))
g.add((CIEE.RTU3, RDF.type, BRICK.RTU))
g.add((CIEE.RTU4, RDF.type, BRICK.RTU))
g.add((CIEE.RTU5, RDF.type, BRICK.RTU))

# map RTUs to zones
g.add((CIEE.RTU1, BF.feeds, CIEE.SouthZone))
g.add((CIEE.RTU2, BF.feeds, CIEE.EastZone))
g.add((CIEE.RTU3, BF.feeds, CIEE.CentralZone))
g.add((CIEE.RTU4, BF.feeds, CIEE.NorthZone))

# add thermostats
g.add((CIEE.RTU3, BF.hasPoint, CIEE.building_meter))
for t in generator.add_xbos_thermostat(CIEE.openoffice_tstat,"ciee/devices/venstar/s.venstar/OpenSpace/i.xbos.thermostat", CIEE.RTU3):
    g.add(t)

g.add((CIEE.RTU1, BF.hasPoint, CIEE.building_meter))
for t in generator.add_xbos_thermostat(CIEE.conference_tstat,"ciee/devices/venstar/s.venstar/ConferenceRoom/i.xbos.thermostat", CIEE.RTU1):
    g.add(t)

g.add((CIEE.RTU2, BF.hasPoint, CIEE.building_meter))
for t in generator.add_xbos_thermostat(CIEE.carl_tstat,"ciee/devices/pelican/s.pelican/SouthEastCorner/i.xbos.thermostat", CIEE.RTU2):
    g.add(t)

g.add((CIEE.RTU4, BF.hasPoint, CIEE.building_meter))
for t in generator.add_xbos_thermostat(CIEE.clarity_tstat,"ciee/devices/venstar/s.venstar/Clarity/i.xbos.thermostat", CIEE.RTU4):
    g.add(t)

# add Lighting
lights2rooms = {
   "Sensor01930e": CIEE.R218,
   "Sensor01935b": CIEE.R218,
   "Sensor019324": CIEE.R218,

   "Sensor02309c": CIEE.R220,
   "Sensor01902e": CIEE.R220,

   "Sensor01942b": CIEE.R221,
   "Sensor01934e": CIEE.R221,
   "Sensor30005f": CIEE.R221,

   "Sensor01907b": CIEE.R219,
   "Sensor018ff9": CIEE.R219,

   "Sensor02d438": CIEE.R208,
   "Sensor02d458": CIEE.R208,
   "Sensor02d429": CIEE.R208,
   "Sensor02d454": CIEE.R208,
   "Sensor02d455": CIEE.R208,
   "Sensor02d444": CIEE.R208,

   "Sensor02d432": CIEE.R208,
   "Sensor013263": CIEE.R208,
   "Sensor02d433": CIEE.R208,

   "Sensor00d56d": CIEE.R203,
}
for lightname, roomname in lights2rooms.items():
    name = "enlighted_"+lightname
    g.add((CIEE[name], RDF.type, BRICK.Lighting_System))
    g.add((CIEE[name], BF.isLocatedIn, roomname))
    url = Literal("ciee/devices/enlighted/s.enlighted/{0}/i.xbos.light".format(lightname))
    for t in generator.add_xbos_light(CIEE[name], url):
        g.add(t)

    metername = "enlighted_"+lightname+"_meter"
    g.add((CIEE[metername], RDF.type, BRICK.Electric_Meter))
    g.add((CIEE[metername], BF.feeds, CIEE.building_meter))
    g.add((CIEE[metername], BF.isPointOf, CIEE[name]))
    uri = "ciee/devices/enlighted/s.enlighted/{0}/i.xbos.meter".format(lightname)
    g.add((CIEE[metername], BF.uri, Literal(uri)))
    if BOSSWAVE:
        rest_of_uri = '/'.join(uri.split("/")[1:])
        namespace = uri.split("/")[0]
        uuid = client.uuids('name = "power" and namespace = "{0}" and originaluri like "{1}"'.format(namespace, rest_of_uri))
        if len(uuid) > 0:
            g.add((CIEE[metername], BF.uuid, Literal(uuid[0])))

    occname = "enlighted_"+lightname+"_occupancy"
    g.add((CIEE[occname], RDF.type, BRICK.Occupancy_Sensor))
    g.add((CIEE[occname], BF.isPointOf, roomname))
    g.add((CIEE[occname], BF.isPointOf, CIEE[name]))
    g.add((CIEE[occname], BF.isLocatedIn, roomname))
    uri = "ciee/devices/enlighted/s.enlighted/{0}/i.xbos.occupancy_sensor".format(lightname)
    g.add((CIEE[occname], BF.uri, Literal(uri)))
    if BOSSWAVE:
        rest_of_uri = '/'.join(uri.split("/")[1:])
        namespace = uri.split("/")[0]
        uuid = client.uuids('name = "occupancy" and namespace = "{0}" and originaluri like "{1}"'.format(namespace, rest_of_uri))
        if len(uuid) > 0:
            g.add((CIEE[occname], BF.uuid, Literal(uuid[0])))

lights2zones = {
   "Sensor01930e": 'north_west_open_office',
   "Sensor01935b": 'north_west_open_office',
   "Sensor019324": 'north_west_open_office',

   "Sensor02309c": 'north_east_open_office',
   "Sensor01902e": 'north_east_open_office',

   "Sensor01942b": 'south_west_open_office',
   "Sensor01934e": 'south_west_open_office',
   "Sensor30005f": 'south_west_open_office',

   "Sensor01907b": 'south_east_open_office',
   "Sensor018ff9": 'south_east_open_office',

   "Sensor02d438": 'conference_room',
   "Sensor02d458": 'conference_room',
   "Sensor02d429": 'conference_room',
   "Sensor02d454": 'conference_room',
   "Sensor02d455": 'conference_room',
   "Sensor02d444": 'conference_room',
   "Sensor02d432": 'conference_room',
   "Sensor013263": 'conference_room',
   "Sensor02d433": 'conference_room',

   "Sensor00d56d": 'copy_room',
}
lightzones = {
    'north_west_open_office': [CIEE.R218],
    'north_east_open_office': [CIEE.R220],
    'south_west_open_office': [CIEE.R221],
    'south_east_open_office': [CIEE.R219],
    'conference_room': [CIEE.R208],
    'copy_room': [CIEE.R203],
}
for lightname, zonename in lights2zones.items():
    name = "enlighted_"+lightname
    g.add((CIEE[zonename], RDF.type, BRICK.Lighting_Zone))
    g.add((CIEE[name], BF.feeds, CIEE[zonename]))
for zone, roomlist in lightzones.items():
    name = "lighting_"+zone
    for room in roomlist:
        g.add((CIEE[zonename], BF.hasPart, room))

lightingzones = {
    "lightingzone1": [CIEE.R207, CIEE.R208],
}
for zone, roomlist in lightingzones.items():
    for room in roomlist:
        g.add((CIEE[zone], BF.hasPart, room))


# save building
g.serialize(destination='ciee.ttl',format='turtle')
print len(g), "triples"
