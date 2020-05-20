from django.test import TestCase

# Create your tests here.

from functools import wraps
import cProfile
#from line_profiler import LineProfiler
import time
from py2neo import Graph, Node, Relationship, NodeMatcher,Database

def func_time(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        end = time.time()
        print(f.__name__, 'took', end - start, 'seconds')
        return result

    return wrapper


def func_cprofile(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        profile = cProfile.Profile()
        try:
            profile.enable()
            result = f(*args, **kwargs)
            profile.disable()
            return result
        finally:
            profile.print_stats(sort='time')

    return wrapper


graph = Graph("http://localhost:7474", auth=("neo4j", "123456"))
matcher = NodeMatcher(graph)

# 单例创建节点测试
@func_cprofile
@func_time
def test_create_node(num):
    for i in range(num):
        node = Node("alone_create_test", name="test", age="11")
        graph.create(node)

# 批量创建节点测试
@func_cprofile
@func_time
def test_create_batch_node(batch):
    s = Node("batch_create_test", name="test", age="11")
    for i in range(batch - 1):
        n = Node("batch_create_test", name="test", age="11")
        s = s | n
    graph.create(s)

# 单例删除测试
@func_time
@func_cprofile
def test_delete_node(num):
    for i in range(num):
        n = matcher.match("alone_create_test").limit(1).first()
        graph.delete(n)

# 批量删除测试
@func_time
@func_cprofile
def test_delete_batch_node(batch):
    s = Node("batch_create_test", name="test")
    nodes = matcher.match("batch_create_test").limit(batch)
    for i in list(nodes):
        s = s | i
    graph.delete(s)

# 查询测试
@func_time
@func_cprofile
def getNearNodesByCategory(category):
    data = matcher.match("plant", category=category)
    return data


@func_time
@func_cprofile
def searchNodesByName(name):
    data = matcher.match("plant").where("_.name=~'.*" + name +".*'")
    return data
# test_create_node(1000)
# # test_create_batch_node(1000)
# #
# # test_delete_node(1000)
# # test_delete_batch_node(1000)
# category = "裸子植物门|Gymnospermae 松科|Pinaceae 冷杉属|Abies"
# a = getNearNodesByCategory(category)
# b = searchNodesByName("松")
