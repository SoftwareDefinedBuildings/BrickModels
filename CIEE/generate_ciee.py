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
            g.add((CIEE[name]+"_air_temp", BF.uuid, Literal(uuid[0])))

        uuid = client.uuids('name = "pir" and Deployment = "CIEE" and uri like "{0}"'.format(sensor))
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
for t in generator.add_xbos_thermostat(CIEE.openoffice_tstat,"ciee/devices/venstar/s.venstar/OpenSpace/i.xbos.thermostat", CIEE.RTU3):
    g.add(t)
for t in generator.add_xbos_thermostat(CIEE.conference_tstat,"ciee/devices/venstar/s.venstar/ConferenceRoom/i.xbos.thermostat", CIEE.RTU1):
    g.add(t)
for t in generator.add_xbos_thermostat(CIEE.carl_tstat,"ciee/devices/pelican/s.pelican/SouthEastCorner/i.xbos.thermostat", CIEE.RTU2):
    g.add(t)

# add Lighting

# save building
g.serialize(destination='ciee.ttl',format='turtle')
print len(g), "triples"
