from django.shortcuts import render
from django.http import HttpResponse, Http404
from . import models
import json

# Create your views here.
def index(request):
    return HttpResponse("Hello world")

def test(request):
    rst = models.getTestData()
    context = {
        "nodes_count": len(rst)
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
    context = {
        'node': node,
        'level': 1
    }
    return render(request, 'display/detail.html', context)

def nearNode(request, code, level=1):
    data = models.getNearNodes(code)
    rst = []
    for i in data:
        rst.append(i['n'])
    return HttpResponse(json.dumps(rst))