from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
	context = {'item1':"My first string"}
	return render(request,'attendance/list.html',context)	

def classDetail(request,classSection):
	neatSection = classSection[1:-1] + " " + classSection[-1]
	strippedSection = classSection[1:]
	context = {'classSection':classSection,'neatSection':neatSection,'strippedSection':strippedSection}
	return render(request,'attendance/index.html',context)