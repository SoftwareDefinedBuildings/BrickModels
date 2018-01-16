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

chjson = json.load(open('chillers.json'))
pjson = json.load(open('pumps.json'))

g.add((BRICK.Absorption_Chiller, RDF.type, OWL.Class))
g.add((BRICK.Absorption_Chiller, RDFS.subClassOf, BRICK.Chiller))
g.add((BRICK.Centrifugal_Chiller, RDF.type, OWL.Class))
g.add((BRICK.Centrifugal_Chiller, RDFS.subClassOf, BRICK.Chiller))
g.add((BRICK.Current_Sensor, RDF.type, OWL.Class))
g.add((BRICK.Current_Sensor, RDFS.subClassOf, BRICK.Sensor))
g.add((SDH['CH1'], RDF.type, BRICK.Absorption_Chiller))
g.add((SDH['CH2'], RDF.type, BRICK.Centrifugal_Chiller))

def make_point(chiller, pointdesc, pointclass):
    if pointdesc is None:
        return
    pointname = pointdesc['PointName'].replace(' ','_')

    g.add((pointclass, RDF.type, OWL.Class))
    if 'Sensor' in pointclass:
        g.add((pointclass, RDFS.subClassOf, BRICK.Sensor))
    elif 'Command' in pointclass:
        g.add((pointclass, RDFS.subClassOf, BRICK.Command))
    elif 'Setpoint' in pointclass:
        g.add((pointclass, RDFS.subClassOf, BRICK.Setpoint))

    g.add((SDH[pointname], RDF.type, pointclass))
    if 'uuid' in pointdesc:
        g.add((SDH[pointname], BF.uuid, Literal(pointdesc['uuid'])))
        g.add((SDH[pointname], BF.pointname, Literal(pointdesc['PointName'])))
    g.add((SDH[chiller], BF.hasPoint, SDH[pointname]))

for chiller, points in chjson.items():
    if chiller == 'Extra': continue
    make_point(chiller, points['Chilled Water Supply Temperature Sensor'], BRICK.Chilled_Water_Supply_Temperature_Sensor)
    make_point(chiller, points['Chilled Water Supply Temperature Reset'], BRICK.Chilled_Water_Supply_Temperature_Reset_Command)
    make_point(chiller, points['Chilled Water Return Temperature Sensor'], BRICK.Chilled_Water_Return_Temperature_Sensor)
    make_point(chiller, points['Chilled Water Flow'], BRICK.Chilled_Water_Flow_Sensor)
    make_point(chiller, points['Chilled Water Differential Pressure Sensor'], BRICK.Chilled_Water_Differential_Pressure_Sensor)
    make_point(chiller, points['Chilled Water Differential Pressure Setpoint'], BRICK.Chilled_Water_Differential_Pressure_Setpoint)

    # parts
    cooling_tower = chiller+'_CT'
    g.add((SDH[cooling_tower], RDF.type, BRICK.Cooling_Tower))
    condenser = chiller+'_condenser'
    g.add((SDH[condenser], RDF.type, BRICK.Condenser_Heat_Exchanger))
    evaporator = chiller+'_evaporator'
    g.add((SDH[evaporator], RDF.type, BRICK.Evaporator_Heat_Exchanger))

    make_point(condenser, points['Chilled Water Flow'], BRICK.Chilled_Water_Flow_Sensor)
    g.add((SDH[cooling_tower], BF.feeds, SDH[chiller]))
    g.add((SDH[cooling_tower], BF.isFedBy, SDH[chiller]))
    g.add((SDH[chiller], BF.hasPart, SDH[condenser]))
    g.add((SDH[chiller], BF.hasPart, SDH[evaporator]))

    # cooling valve
    chw_bypass_valve_def = points['Chilled Water Bypass Valve']
    chw_bypass_valve = chw_bypass_valve_def['PointName'].replace(' ','_')
    g.add((SDH[chw_bypass_valve], RDF.type, BRICK.Chilled_Water_Bypass_Valve))
    g.add((SDH[chiller], BF.hasPart, SDH[chw_bypass_valve]))

    # all chillers feed all AHUs
    for ahu in ["AH1A","AH1B","AH2A","AH2B"]:
        g.add((SDH[chiller], BF.feeds, SDH[ahu]))
        ccv = "SDH.{0}_CCV".format(ahu) # this is part of ahu
        g.add((SDH[chiller], BF.feeds, SDH[ccv]))

    # pumps
    pumps = pjson[chiller]

    for pump, desc in pumps.items():
        if pump.startswith('CHP'):
            g.add((SDH[pump], RDF.type, BRICK.Chilled_Water_Pump))
            g.add((SDH[chiller], BF.hasPart, SDH[pump]))
        elif pump.startswith('CWP'):
            g.add((SDH[pump], RDF.type, BRICK.Condenser_Water_Pump))
            g.add((SDH[condenser], BF.hasPart, SDH[pump]))

        make_point(pump, desc, BRICK.Current_Sensor)

g.serialize(destination='chiller.ttl',format='turtle')
print len(g)
