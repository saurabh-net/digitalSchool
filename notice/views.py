from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from attendance.models import ListOfClasses

# Create your views here.

@login_required
def index(request):
	latest_class_list = ListOfClasses.objects.filter(schoolUser=request.user);
	classLinks = [p.someClass for p in latest_class_list]
	classNames = [p[1:-1] + " " + p[-1] for p in classLinks]
	zipped_data = zip(classLinks, classNames)
	context = {'item1':"My first string",'classLinks':classLinks,'classNames':classNames,'zipped_data':zipped_data}
	return render(request,'notice/list.html',context)	
	
@login_required
def classDetail(request,classSection):
	firstInstance = ListOfClasses.objects.filter(schoolUser=request.user).first()
	restKey = firstInstance.restKey
	javaKey = firstInstance.javaKey
	appKey 	= firstInstance.appKey
	neatSection = classSection[1:-1] + " " + classSection[-1]
	strippedSection = classSection[1:]
	context = {'classSection':classSection,'neatSection':neatSection,'strippedSection':strippedSection,'javaKey':javaKey,'appKey':appKey}
	return render(request,'notice/notice.html',context)