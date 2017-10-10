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

def get_partial_name(d, name, default=None):
    for k in d.keys():
        if name in k:
            return d.get(name, default)
    return None

# ITS NOT A DAMPER; just FAN + sensor?
def make_damper(name, prefix, definitions, ahuname):
    """ e.g. "Return Air"; then it finds the points"""
    damper_defs = {k:v for k,v in definitions.items() if name in k}
    damper = prefix+"_"+definitions[name + " Damper"].get('PointName')
    flow_sensor = definitions[name + " Damper"].get('PointName')
    flow_sensor_uuid = definitions[name + " Damper"].get("uuid")

    damper_classname = name.replace(' ','_')+'_Damper'
    flow_classname = name.replace(' ','_')+'_Air_Flow_Sensor'
    g.add((SDH[damper], RDF.type, BRICK[damper_classname]))
    g.add((SDH[flow_sensor], RDF.type, BRICK[flow_classname]))
    g.add((SDH[flow_sensor], BF.uuid, Literal(flow_sensor_uuid)))
    g.add((SDH[damper], BF.hasPoint, SDH[flow_sensor]))
    g.add((SDH[ahuname], BF.hasPart, SDH[damper]))
    return damper

ahujson = json.load(open('ahu.json'))

for ahuname, points in ahujson.items():
    g.add((SDH[ahuname], RDF.type, BRICK.Air_Handling_Unit))

    # instantiate dampers
    if get_partial_name(points, 'Exhaust Air Damper') is not None:
        ead = make_damper('Exhaust Air', 'EAD', points, ahuname)
    if get_partial_name(points, 'Return Air Damper') is not None:
        rad = make_damper('Return Air', 'RAD', points, ahuname)
    if get_partial_name(points, 'Supply Air Damper') is not None:
        sad = make_damper('Supply Air', 'RAD', points, ahuname)
    if get_partial_name(points, 'Isolation Damper') is not None:
        iso_damper = make_damper('Isolation', 'ID', points, ahuname)
    if get_partial_name(points, 'Outside Air Damper') is not None:
        oad = make_damper('Outside Air', 'OAD', points, ahuname)
        min_pos = points['Minimum Outside Air Damper Position']
        mpo_name = min_pos.get('PointName')
        mpo_uuid = min_pos.get('uuid')
        g.add((SDH[mpo_name], RDF.type, BRICK.Minimum_Outside_Air_Damper_Position))
        g.add((SDH[mpo_name], BF.uuid, Literal(mpo_uuid)))
        g.add((SDH[oad], BF.hasPoint, SDH[mpo_name]))

    mixed_air_temp_sensor = points['Mixed Air Temperature Sensor']['PointName']
    mat_uuid = points['Mixed Air Temperature Sensor']['uuid']
    g.add((SDH[mixed_air_temp_sensor], RDF.type, BRICK.Mixed_Air_Temperature_Sensor))
    g.add((SDH[mixed_air_temp_sensor], BF.uuid, Literal(mat_uuid)))
    g.add((SDH[ahuname], BF.hasPoint, SDH[mixed_air_temp_sensor]))

    cooling_valve = points['Cooling Coil Valve Percentage']['PointName']
    ccv_uuid = points['Cooling Coil Valve Percentage']['uuid']
    cooling_valve_percentage = cooling_valve + '_valve'
    g.add((SDH[cooling_valve], RDF.type, BRICK.Cooling_Valve))
    g.add((SDH[cooling_valve_percentage], RDF.type, BRICK.Cooling_Valve_Command))
    g.add((SDH[cooling_valve_percentage], BF.uuid, Literal(ccv_uuid)))
    g.add((SDH[cooling_valve], BF.hasPoint, SDH[cooling_valve_percentage]))
    g.add((SDH[ahuname], BF.hasPart, SDH[cooling_valve]))

    supply_fan_speed = points['Supply Fan Speed']
    supply_fan_power = points['Supply Fan Power']
    supply_fan_speed_name = supply_fan_speed['PointName'].replace(' ','_')
    supply_fan_power_name = supply_fan_power['PointName'].replace(' ','_')
    supply_fan_speed_uuid = supply_fan_speed['uuid']
    supply_fan_power_uuid = supply_fan_power['uuid']
    supply_fan = supply_fan_speed['PointName'].split(':')[0]
    g.add((SDH[supply_fan], RDF.type, BRICK.Supply_Fan))
    g.add((SDH[supply_fan_speed_name], RDF.type, BRICK.Fan_Speed_Command))
    g.add((SDH[supply_fan_power_name], RDF.type, BRICK.Power_Meter))
    g.add((SDH[supply_fan_speed_name], BF.uuid, Literal(supply_fan_speed_uuid)))
    g.add((SDH[supply_fan_power_name], BF.uuid, Literal(supply_fan_power_uuid)))
    g.add((SDH[supply_fan], BF.hasPoint, SDH[supply_fan_speed_name]))
    g.add((SDH[supply_fan], BF.hasPoint, SDH[supply_fan_power_name]))
    g.add((SDH[ahuname], BF.hasPart, SDH[supply_fan]))

    return_fan_speed = points['Return Fan Speed']
    return_fan_power = points['Return Fan Power']
    return_fan_speed_name = return_fan_speed['PointName'].replace(' ','_')
    return_fan_power_name = return_fan_power['PointName'].replace(' ','_')
    return_fan_speed_uuid = points['Return Fan Speed']['uuid']
    return_fan_power_uuid = points['Return Fan Power']['uuid']
    return_fan = return_fan_speed['PointName'].split(':')[0]
    g.add((SDH[return_fan], RDF.type, BRICK.Return_Fan))
    g.add((SDH[return_fan_speed_name], RDF.type, BRICK.Fan_Speed_Command))
    g.add((SDH[return_fan_power_name], RDF.type, BRICK.Power_Meter))
    g.add((SDH[return_fan_speed_name], BF.uuid, Literal(return_fan_speed_uuid)))
    g.add((SDH[return_fan_power_name], BF.uuid, Literal(return_fan_power_uuid)))
    g.add((SDH[return_fan], BF.hasPoint, SDH[return_fan_speed_name]))
    g.add((SDH[return_fan], BF.hasPoint, SDH[return_fan_power_name]))
    g.add((SDH[ahuname], BF.hasPart, SDH[return_fan]))

    # other points
    sat_sensor_def = points["Supply Air Temperature Sensor"]
    sat_sensor = sat_sensor_def['PointName'].replace(' ','_')
    g.add((SDH[sat_sensor], RDF.type, BRICK.Supply_Air_Temperature_Sensor))
    g.add((SDH[sat_sensor], BF.uuid, Literal(sat_sensor_def['uuid'])))
    g.add((SDH[ahuname], BF.hasPoint, SDH[sat_sensor]))

    sat_setpoint_def = points["Supply Air Temperature Setpoint"]
    sat_setpoint = sat_setpoint_def['PointName'].replace(' ','_')
    g.add((SDH[sat_setpoint], RDF.type, BRICK.Supply_Air_Temperature_Setpoint))
    g.add((SDH[sat_setpoint], BF.uuid, Literal(sat_setpoint_def['uuid'])))
    g.add((SDH[ahuname], BF.hasPoint, SDH[sat_setpoint]))

    sdsp_def = points["Supply Duct Static Pressure Sensor"]
    sdsp = sdsp_def['PointName'].replace(' ','_')
    g.add((SDH[sdsp], RDF.type, BRICK.Supply_Air_Static_Pressure_Sensor))
    g.add((SDH[sdsp], BF.uuid, Literal(sdsp_def['uuid'])))
    g.add((SDH[ahuname], BF.hasPoint, SDH[sdsp]))

    saf_sensor_def = points["Supply Air Flow Sensor"]
    saf_sensor = saf_sensor_def['PointName'].replace(' ','_')
    g.add((SDH[saf_sensor], RDF.type, BRICK.Supply_Air_Flow_Sensor))
    g.add((SDH[saf_sensor], BF.uuid, Literal(saf_sensor_def['uuid'])))
    g.add((SDH[ahuname], BF.hasPoint, SDH[saf_sensor]))

    rat_sensor_def = points["Return Air Temperature Sensor"]
    rat_sensor = rat_sensor_def['PointName'].replace(' ','_')
    g.add((SDH[rat_sensor], RDF.type, BRICK.Return_Air_Temperature_Sensor))
    g.add((SDH[rat_sensor], BF.uuid, Literal(rat_sensor_def['uuid'])))
    g.add((SDH[ahuname], BF.hasPoint, SDH[rat_sensor]))

    rah_sensor_def = points["Return Air Humidity Sensor"]
    rah_sensor = rah_sensor_def['PointName'].replace(' ','_')
    g.add((SDH[rah_sensor], RDF.type, BRICK.Return_Air_Humidity_Sensor))
    g.add((SDH[rah_sensor], BF.uuid, Literal(rah_sensor_def['uuid'])))
    g.add((SDH[ahuname], BF.hasPoint, SDH[rah_sensor]))

    rdsp_def = points["Return Duct Static Pressure Sensor"]
    rdsp = rdsp_def['PointName'].replace(' ','_')
    g.add((SDH[rdsp], RDF.type, BRICK.Return_Air_Static_Pressure_Sensor))
    g.add((SDH[rdsp], BF.uuid, Literal(rdsp_def['uuid'])))
    g.add((SDH[ahuname], BF.hasPoint, SDH[rdsp]))

    raf_sensor_def = points["Return Air Flow Sensor"]
    raf_sensor = raf_sensor_def['PointName'].replace(' ','_')
    g.add((SDH[raf_sensor], RDF.type, BRICK.Return_Air_Flow_Sensor))
    g.add((SDH[raf_sensor], BF.uuid, Literal(raf_sensor_def['uuid'])))
    g.add((SDH[ahuname], BF.hasPoint, SDH[raf_sensor]))

    # wire things together here
    g.add((SDH[rad], BF.feeds, SDH[return_fan]))
    g.add((SDH[return_fan], BF.feeds, SDH[cooling_valve]))
    g.add((SDH[return_fan], BF.feeds, SDH[ahuname]))

    g.add((SDH[oad], BF.feeds, SDH[cooling_valve]))
    g.add((SDH[cooling_valve], BF.feeds, SDH[supply_fan]))
    g.add((SDH[supply_fan], BF.feeds, SDH[iso_damper]))
    #TODO: where does supply air damper go?

    g.add((SDH[ahuname], BF.feeds, SDH[ead]))

g.serialize(destination='ahu.ttl',format='turtle')
print len(g)
