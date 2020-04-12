from django.db import models
from py2neo import Graph, Node, Relationship, NodeMatcher

graph = Graph("http://localhost:7474", auth=("neo4j", "123456"))
matcher = NodeMatcher(graph)
# Create your models here.
def getTestData():
    data = matcher.match("animal").limit(20)
    return data

def searchNodesByName(name):
    data = matcher.match("animal").where("_.name=~'.*" + name +".*'")
    print(list(data))
    return data