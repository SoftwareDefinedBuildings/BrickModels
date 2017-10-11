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

g.serialize(destination='chiller.ttl',format='turtle')
print len(g)
