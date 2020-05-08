from django.db import models
from py2neo import Graph, Node, Relationship, NodeMatcher,Database

graph = Graph("http://localhost:7474", auth=("neo4j", "123456"))
matcher = NodeMatcher(graph)
db = Database("http://localhost:7474", user="neo4j", password="123456")
# Create your models here.
def getDbConfig():
    return db

def getTestData():
    data = matcher.match("plant").limit(20)
    return data

def searchNodesByName(name):
    data = matcher.match("plant").where("_.name=~'.*" + name +".*'")
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