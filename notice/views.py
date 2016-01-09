from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def index(request):
	context = {'item1':"My first string"}
	return render(request,'notice/list.html',context)	
	
@login_required
def classDetail(request,classSection):
	neatSection = classSection[1:-1] + " " + classSection[-1]
	strippedSection = classSection[1:]
	context = {'classSection':classSection,'neatSection':neatSection,'strippedSection':strippedSection}
	return render(request,'notice/notice.html',context)