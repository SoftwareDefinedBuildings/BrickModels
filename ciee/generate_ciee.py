from rdflib import Graph, Namespace, URIRef, Literal
import rdflib
import re

RDF = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
RDFS = Namespace('http://www.w3.org/2000/01/rdf-schema#')
BRICK = Namespace('http://buildsys.org/ontologies/Brick#')
BRICKFRAME = Namespace('http://buildsys.org/ontologies/BrickFrame#')
BF = BRICKFRAME
OWL = Namespace('http://www.w3.org/2002/07/owl#')
CIEE = Namespace('http://buildsys.org/ontologies/ciee#')

g = rdflib.Graph()
g.bind('rdf', RDF)
g.bind('rdfs', RDFS)
g.bind('brick', BRICK)
g.bind('bf', BRICKFRAME)
g.bind('bldg', CIEE)

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


# add zone temperature sensors
g.add((CIEE.hamilton_005C, RDF.type, BRICK.Zone_Temperature_Sensor))
g.add((CIEE.hamilton_005C, BF.uri,  Literal("gvnMwdNvhD5ClAuF8SQzrp-Ywcjx9c1m4du9N5MRCXs=/sensors/s.hamilton/00126d070000005C/i.temperature/signal/operative")))

g.add((CIEE.hamilton_005D, RDF.type, BRICK.Zone_Temperature_Sensor))
g.add((CIEE.hamilton_005D, BF.uri,  Literal("gvnMwdNvhD5ClAuF8SQzrp-Ywcjx9c1m4du9N5MRCXs=/sensors/s.hamilton/00126d070000005D/i.temperature/signal/operative")))

g.add((CIEE.hamilton_0027, RDF.type, BRICK.Zone_Temperature_Sensor))
g.add((CIEE.hamilton_0027, BF.uri,  Literal("gvnMwdNvhD5ClAuF8SQzrp-Ywcjx9c1m4du9N5MRCXs=/sensors/s.hamilton/00126d0700000027/i.temperature/signal/operative")))

g.add((CIEE.hamilton_002B, RDF.type, BRICK.Zone_Temperature_Sensor))
g.add((CIEE.hamilton_002B, BF.uri,  Literal("gvnMwdNvhD5ClAuF8SQzrp-Ywcjx9c1m4du9N5MRCXs=/sensors/s.hamilton/00126d070000002B/i.temperature/signal/operative")))

g.add((CIEE.hamilton_002E, RDF.type, BRICK.Zone_Temperature_Sensor))
g.add((CIEE.hamilton_002E, BF.uri,  Literal("gvnMwdNvhD5ClAuF8SQzrp-Ywcjx9c1m4du9N5MRCXs=/sensors/s.hamilton/00126d070000002E/i.temperature/signal/operative")))

g.add((CIEE.hamilton_002A, RDF.type, BRICK.Zone_Temperature_Sensor))
g.add((CIEE.hamilton_002A, BF.uri,  Literal("gvnMwdNvhD5ClAuF8SQzrp-Ywcjx9c1m4du9N5MRCXs=/sensors/s.hamilton/00126d070000002A/i.temperature/signal/operative")))

g.add((CIEE.hamilton_005E, RDF.type, BRICK.Zone_Temperature_Sensor))
g.add((CIEE.hamilton_005E, BF.uri,  Literal("gvnMwdNvhD5ClAuF8SQzrp-Ywcjx9c1m4du9N5MRCXs=/sensors/s.hamilton/00126d070000005E/i.temperature/signal/operative")))

g.add((CIEE.hamilton_005A, RDF.type, BRICK.Zone_Temperature_Sensor))
g.add((CIEE.hamilton_005A, BF.uri,  Literal("gvnMwdNvhD5ClAuF8SQzrp-Ywcjx9c1m4du9N5MRCXs=/sensors/s.hamilton/00126d070000005A/i.temperature/signal/operative")))

g.add((CIEE.hamilton_0060, RDF.type, BRICK.Zone_Temperature_Sensor))
g.add((CIEE.hamilton_0060, BF.uri,  Literal("gvnMwdNvhD5ClAuF8SQzrp-Ywcjx9c1m4du9N5MRCXs=/sensors/s.hamilton/00126d0700000060/i.temperature/signal/operative")))

g.add((CIEE.hamilton_0028, RDF.type, BRICK.Zone_Temperature_Sensor))
g.add((CIEE.hamilton_0028, BF.uri,  Literal("gvnMwdNvhD5ClAuF8SQzrp-Ywcjx9c1m4du9N5MRCXs=/sensors/s.hamilton/00126d0700000028/i.temperature/signal/operative")))

g.add((CIEE.hamilton_002C, RDF.type, BRICK.Zone_Temperature_Sensor))
g.add((CIEE.hamilton_002C, BF.uri,  Literal("gvnMwdNvhD5ClAuF8SQzrp-Ywcjx9c1m4du9N5MRCXs=/sensors/s.hamilton/00126d070000002C/i.temperature/signal/operative")))

g.add((CIEE.hamilton_0022, RDF.type, BRICK.Zone_Temperature_Sensor))
g.add((CIEE.hamilton_0022, BF.uri,  Literal("gvnMwdNvhD5ClAuF8SQzrp-Ywcjx9c1m4du9N5MRCXs=/sensors/s.hamilton/00126d0700000022/i.temperature/signal/operative")))

g.add((CIEE.hamilton_005B, RDF.type, BRICK.Zone_Temperature_Sensor))
g.add((CIEE.hamilton_005B, BF.uri,  Literal("gvnMwdNvhD5ClAuF8SQzrp-Ywcjx9c1m4du9N5MRCXs=/sensors/s.hamilton/00126d070000005B/i.temperature/signal/operative")))

g.add((CIEE.hamilton_0025, RDF.type, BRICK.Zone_Temperature_Sensor))
g.add((CIEE.hamilton_0025, BF.uri,  Literal("gvnMwdNvhD5ClAuF8SQzrp-Ywcjx9c1m4du9N5MRCXs=/sensors/s.hamilton/00126d0700000025/i.temperature/signal/operative")))

g.add((CIEE.hamilton_005F, RDF.type, BRICK.Zone_Temperature_Sensor))
g.add((CIEE.hamilton_005F, BF.uri,  Literal("gvnMwdNvhD5ClAuF8SQzrp-Ywcjx9c1m4du9N5MRCXs=/sensors/s.hamilton/00126d070000005F/i.temperature/signal/operative")))

g.add((CIEE.hamilton_0029, RDF.type, BRICK.Zone_Temperature_Sensor))
g.add((CIEE.hamilton_0029, BF.uri,  Literal("gvnMwdNvhD5ClAuF8SQzrp-Ywcjx9c1m4du9N5MRCXs=/sensors/s.hamilton/00126d0700000029/i.temperature/signal/operative")))

# add sensors to rooms
g.add((CIEE.R206, BF.hasPoint, CIEE.hamilton_0027))
g.add((CIEE.R208, BF.hasPoint, CIEE.hamilton_002B))
g.add((CIEE.R209, BF.hasPoint, CIEE.hamilton_002E))
g.add((CIEE.R210, BF.hasPoint, CIEE.hamilton_002A))
g.add((CIEE.R211, BF.hasPoint, CIEE.hamilton_005E))
g.add((CIEE.R212, BF.hasPoint, CIEE.hamilton_005A))
g.add((CIEE.R213, BF.hasPoint, CIEE.hamilton_0060))
g.add((CIEE.R214, BF.hasPoint, CIEE.hamilton_0028))
g.add((CIEE.R215, BF.hasPoint, CIEE.hamilton_002C))
g.add((CIEE.R216, BF.hasPoint, CIEE.hamilton_0022))
g.add((CIEE.R217, BF.hasPoint, CIEE.hamilton_005B))
g.add((CIEE.EastOpen, BF.hasPoint, CIEE.hamilton_0025))
g.add((CIEE.WestOpen, BF.hasPoint, CIEE.hamilton_0029))

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
g.add((CIEE.openoffice_tstat, RDF.type, BRICK.Thermostat))
g.add((CIEE.openoffice_tstat, BF.controls, CIEE.RTU3))
g.add((CIEE.openoffice_tstat, BF.uri, Literal("gvnMwdNvhD5ClAuF8SQzrp-Ywcjx9c1m4du9N5MRCXs=/devices/venstar/s.venstar/OpenSpace/i.xbos.thermostat")))

g.add((CIEE.conference_tstat, RDF.type, BRICK.Thermostat))
g.add((CIEE.conference_tstat, BF.controls, CIEE.RTU1))
g.add((CIEE.conference_tstat, BF.uri, Literal("gvnMwdNvhD5ClAuF8SQzrp-Ywcjx9c1m4du9N5MRCXs=/devices/venstar/s.venstar/ConferenceRoom/i.xbos.thermostat")))

g.add((CIEE.carl_tstat, RDF.type, BRICK.Thermostat))
g.add((CIEE.carl_tstat, BF.controls, CIEE.RTU2))
g.add((CIEE.carl_tstat, BF.uri, Literal("gvnMwdNvhD5ClAuF8SQzrp-Ywcjx9c1m4du9N5MRCXs=/devices/venstar/s.venstar/CarlsOffice/i.xbos.thermostat")))

# add Lighting

# save building
g.serialize(destination='ciee.ttl',format='turtle')
print len(g), "triples"
