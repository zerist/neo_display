from django.db import models
from py2neo import Graph, Node, Relationship, NodeMatcher,Database
from neomodel import StructuredNode, StringProperty, IntegerProperty, DateProperty

graph = Graph("http://localhost:7474", auth=("neo4j", "123456"))
matcher = NodeMatcher(graph)
db = Database("http://localhost:7474", user="neo4j", password="123456")
# Create your models here.

class AnimalNode(StructuredNode):
    name = StringProperty(unique_index=True)
    name_en = StringProperty(unique_index=True)
    name_cn = StringProperty(unique_index=True)
    belong = StringProperty()
    alias = StringProperty()
    position = StringProperty()
    info = StringProperty()
    code = StringProperty(unique_index=True)

    class Meta:
        app_label = 'animal'

class PlantNode(StructuredNode):
    name = StringProperty(unique_index=True)
    name_cn = StringProperty(unique_index=True)
    name_en = StringProperty(unique_index=True)
    belong = StringProperty()
    shape = StringProperty()
    document = StringProperty()
    position = StringProperty()
    behavior = StringProperty()
    environment = StringProperty()

    class Meta:
        app_label = 'plant'

class RootNode(StructuredNode):
    color = StringProperty()
    old = StringProperty()
    length = IntegerProperty()

    class Meta:
        app_label = 'root'

class StemNode(StructuredNode):
    color = StringProperty()
    old = StringProperty()
    length = IntegerProperty()

    class Meta:
        app_label = 'stem'

class FlowerNode(StructuredNode):
    color = StringProperty()
    old = StringProperty()
    time = DateProperty()

    class Meta:
        app_label = 'flower'

class LeafNode(StructuredNode):
    color = StringProperty()
    old = StringProperty()
    length = IntegerProperty()

    class Meta:
        app_label = 'leaf'

class FruitNode(StructuredNode):
    color = StringProperty()
    old = StringProperty()
    length = IntegerProperty()

    class Meta:
        app_label = 'fruit'

def getDbConfig():
    return db

def getTestData():
    data = matcher.match("plant").limit(20)
    return data

def searchNodesByName(name):
    data = matcher.match("plant").where("_.name=~'.*" + name +".*'")
    return data

def searchNodesByLabel(type, old):
    label = "leaf"
    if type == "2":
        label = "leaf"
    elif type == "3":
        label = "root"
    elif type == "4":
        label = "fruit"
    elif type == "5":
        label = "stem"
    data = graph.run("match (n:plant)-[r:has]->(m:"+label+") where m.old contains '"+old+"' return n").data()
    return data

def searchNodeByCode(code):
    data = matcher.match("plant", name=code).first()
    return data

#get near nodes by relation
#Database: first
def getNearNodes(code):
    data = graph.run("match (n:animal)-[r:属于]->(d:animal) where d.code='" + code + "' return n,r,d").data()
    return data

#Database: second
def getNearNodesByCategory(category):
    data = matcher.match("plant", category=category)
    return data

#Database: third
def getNearNodesByBelong(belong):
    data = matcher.match("plant", belong=belong)
    return data

#Database: third
def getSubNodesByName(name):
    data = graph.run("match (n:plant)-[r:has]->(d) where n.name='"+ name +"' return n,r,d").data()
    return data