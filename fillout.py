#!/usr/bin/env python
import sys
import os
import rdflib

RDF = rdflib.Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
RDFS = rdflib.Namespace('http://www.w3.org/2000/01/rdf-schema#')
BRICK = rdflib.Namespace('https://brickschema.org/schema/1.0.1/Brick#')
BRICKFRAME = rdflib.Namespace('https://brickschema.org/schema/1.0.1/BrickFrame#')
BRICKTAG = rdflib.Namespace('https://brickschema.org/schema/1.0.1/BrickTag#')
OWL = rdflib.Namespace('http://www.w3.org/2002/07/owl#')

def new_graph():
    g = rdflib.Graph()
    g.bind( 'rdf', RDF)
    g.bind( 'rdfs', RDFS)
    g.bind( 'brick', BRICK)
    g.bind( 'bf', BRICKFRAME)
    g.bind( 'btag', BRICKTAG)
    g.bind( 'owl', OWL)
    #g.parse('../Brick/Brick.ttl', format='turtle')
    #g.parse('../Brick/BrickFrame.ttl', format='turtle')
    #g.parse('../Brick/BrickTag.ttl', format='turtle')
    return g

g = new_graph()
g.parse(sys.argv[1], format='turtle')

# ADD INVERSE RELATIONSHIPS
res = g.query("SELECT ?a ?b WHERE { ?a bf:hasPart ?b .}")
for row in res:
    g.add((row[1], BRICKFRAME.isPartOf, row[0]))
res = g.query("SELECT ?a ?b WHERE { ?a bf:isPartOf ?b .}")
for row in res:
    g.add((row[1], BRICKFRAME.hasPart, row[0]))

res = g.query("SELECT ?a ?b WHERE {?a bf:hasPoint ?b .}")
for row in res:
    g.add((row[1], BRICKFRAME.isPointOf, row[0]))
res = g.query("SELECT ?a ?b WHERE {?a bf:isPointOf ?b .}")
for row in res:
    g.add((row[1], BRICKFRAME.hasPoint, row[0]))

res = g.query("SELECT ?a ?b WHERE {?a bf:feeds ?b .}")
for row in res:
    g.add((row[1], BRICKFRAME.isFedBy, row[0]))
res = g.query("SELECT ?a ?b WHERE {?a bf:isFedBy ?b .}")
for row in res:
    g.add((row[1], BRICKFRAME.feeds, row[0]))

res = g.query("SELECT ?a ?b WHERE {?a bf:contains ?b .}")
for row in res:
    g.add((row[1], BRICKFRAME.isLocatedIn, row[0]))
res = g.query("SELECT ?a ?b WHERE {?a bf:isLocatedIn ?b .}")
for row in res:
    g.add((row[1], BRICKFRAME.contains, row[0]))

res = g.query("SELECT ?a ?b WHERE {?a bf:controls ?b .}")
for row in res:
    g.add((row[1], BRICKFRAME.isControlledBy, row[0]))
res = g.query("SELECT ?a ?b WHERE {?a bf:isControlledBy ?b .}")
for row in res:
    g.add((row[1], BRICKFRAME.controls, row[0]))

res = g.query("SELECT ?a ?b WHERE {?a bf:hasOutput ?b .}")
for row in res:
    g.add((row[1], BRICKFRAME.isOutputOf, row[0]))

res = g.query("SELECT ?a ?b WHERE {?a bf:hasInput ?b .}")
for row in res:
    g.add((row[1], BRICKFRAME.isInputOf, row[0]))

res = g.query("SELECT ?a ?b WHERE {?a bf:hasTagSet ?b .}")
for row in res:
    g.add((row[1], BRICKFRAME.isTagSetOf, row[0]))

res = g.query("SELECT ?a ?b WHERE {?a bf:hasToken ?b .}")
for row in res:
    g.add((row[1], BRICKFRAME.isTokenOf, row[0]))

res = g.query("SELECT ?a ?b WHERE {?a bf:adjacentTo ?b .}")
for row in res:
    g.add((row[1], BRICKFRAME.adjacentTo, row[0]))

name = sys.argv[1].replace(".ttl", "-withinverse.ttl")
print(name)
g.serialize(destination=name, format='turtle')
sys.exit(0)
