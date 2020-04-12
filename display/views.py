from django.shortcuts import render
from django.http import HttpResponse
from . import models

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