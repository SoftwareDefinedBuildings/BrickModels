#!/usr/bin/env python
import sys
import uuid
import random
import os
import rdflib

RDF = rdflib.Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
RDFS = rdflib.Namespace('http://www.w3.org/2000/01/rdf-schema#')
BRICK = rdflib.Namespace('https://brickschema.org/schema/1.0.1/Brick#')
BF = rdflib.Namespace('https://brickschema.org/schema/1.0.1/BrickFrame#')
BRICKTAG = rdflib.Namespace('https://brickschema.org/schema/1.0.1/BrickTag#')
OWL = rdflib.Namespace('http://www.w3.org/2002/07/owl#')
SODA = rdflib.Namespace('http://buildsys.org/ontologies/building_example#')

def new_graph():
    g = rdflib.Graph()
    g.bind( 'rdf', RDF)
    g.bind( 'rdfs', RDFS)
    g.bind( 'brick', BRICK)
    g.bind( 'bf', BF)
    g.bind( 'btag', BRICKTAG)
    g.bind( 'owl', OWL)
    g.bind( 'soda', SODA)
    #g.parse('/home/gabe/src/Brick/dist/Brick.ttl', format='turtle')
    #g.parse('/home/gabe/src/Brick/dist/BrickFrame.ttl', format='turtle')
    #g.parse('../Brick/BrickTag.ttl', format='turtle')
    return g

g = new_graph()
g.parse(sys.argv[1], format='turtle')

sensors = g.query('SELECT ?s WHERE { ?s rdf:type brick:Zone_Temperature_Sensor . }')
for s in sensors:
    s = s[0].split('#')[-1]
    print(s)
    g.add((SODA[s], BF.uuid, rdflib.Literal(str(uuid.uuid4()))))
sensors = g.query('SELECT ?s WHERE { ?s rdf:type brick:Reheat_Valve_Command . }')
for s in sensors:
    s = s[0].split('#')[-1]
    print(s)
    g.add((SODA[s], BF.uuid, rdflib.Literal(str(uuid.uuid4()))))
sensors = g.query('SELECT ?s WHERE { ?s rdf:type brick:Mixed_Air_Damper_Position_Sensor . }')
for s in sensors:
    s = s[0].split('#')[-1]
    print(s)
    g.add((SODA[s], BF.uuid, rdflib.Literal(str(uuid.uuid4()))))
sensors = g.query('SELECT ?s WHERE { ?s rdf:type brick:Zone_Temperature_Setpoint . }')
for s in sensors:
    s = s[0].split('#')[-1]
    print(s)
    g.add((SODA[s], BF.uuid, rdflib.Literal(str(uuid.uuid4()))))

rooms = list(g.query("SELECT ?s WHERE {?s rdf:type brick:Room .}"))
rooms = [r for r in rooms if 'floor' not in r]
sensors = g.query('SELECT ?s WHERE { ?s rdf:type brick:Zone_Temperature_Sensor . }')
for sensor in sensors:
    sensor = str(sensor[0]).split('#')[-1]
    room = random.choice(rooms)[0].split('#')[-1]
    print(sensor)
    g.add((SODA[sensor], BF.isLocatedIn, SODA[room]))

print(sys.argv[1])
g.serialize(destination=sys.argv[1], format='turtle')
