from django.shortcuts import render
from django.http import HttpResponse, Http404
from . import models
import json

# Create your views here.
def index(request):
    return HttpResponse("Hello world")


def test(request):
    rst = models.getTestData()
    db = models.getDbConfig()
    context = {
        "nodes_count": len(rst),
        "db_version": db.product,
        "create_time": db.store_creation_time,
        "time_zone": db.config['dbms.logs.timezone'],
        "thread_count": db.config['dbms.threads.worker_count']
    }

    return render(request, "display/test.html", context)


def search(request, text):
    nodes = list(models.searchNodesByName(text))
    context = {
        "nodes": nodes
    }
    return render(request, "display/search.html", context)


def detail(request, code):
    node = models.searchNodeByCode(code)
    if not node:
        raise Http404("Node not found!")

    #相邻节点 by category
    near_nodes = list(models.getNearNodesByBelong(node['belong']))
    context = {
        'node': node,
        'level': 1,
        'near_nodes': near_nodes
    }
    return render(request, 'display/node.html', context)


def getNodeJSON(request, name):
    node = models.searchNodeByCode(name)
    return HttpResponse(json.dumps(node))


# By Code
# Database: first
def nearNode(request, code, level=1):
    data = models.getNearNodes(code)
    rst = []
    for i in data:
        rst.append(i['n'])
    return HttpResponse(json.dumps(rst))


# by belong
# database: third
def nearNodeByCategory(request, category):
    data = models.getNearNodesByCategory(category)
    return HttpResponse(json.dumps(data))


def svgMode(request, code):
    node = models.searchNodeByCode(code)
    if not node:
        raise Http404("Node not found!")

    # 相邻节点 by category
    near_nodes = list(models.getNearNodesByBelong(node['belong']))
    for i in near_nodes:
        i['code'] = i.identity
    context = {
        'node': node,
        'near_nodes': json.dumps(near_nodes),
        'data': near_nodes
    }
    return render(request, 'display/svg_l.html', context)