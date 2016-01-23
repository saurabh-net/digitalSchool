from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.http import HttpResponse
import json,httplib,urllib
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, JsonResponse
from django import forms
from django.template import RequestContext
import django_excel as excel
import pyexcel.ext.xls
import pyexcel.ext.xlsx
import pyexcel
import urllib
from attendance.models import ListOfClasses
from datetime import datetime

# Create your views here.

def postNoticeData(classSection,json_data,restKey,appKey):
	connection = httplib.HTTPSConnection('api.parse.com', 443)
	connection.connect()
	connection.request('POST', '/1/classes/Notice', json_data, {
		   "X-Parse-Application-Id": appKey,
		   "X-Parse-REST-API-Key": restKey,
		   "Content-Type": "application/json"
		 })
	results = json.loads(connection.getresponse().read())
	print results

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
	latest_class_list = ListOfClasses.objects.filter(schoolUser=request.user);
	classLinks = [p.someClass for p in latest_class_list]
	classNames = [p[1:-1] + " " + p[-1] for p in classLinks]
	zipped_data = zip(classLinks, classNames)
	firstInstance = ListOfClasses.objects.filter(schoolUser=request.user).first()
	restKey = firstInstance.restKey
	javaKey = firstInstance.javaKey
	appKey 	= firstInstance.appKey
	neatSection = classSection[1:-1] + " " + classSection[-1]
	print neatSection
	strippedSection = classSection[1:]
	if request.method == 'POST':
		print "I am here!"
		data = {}
		data['Category']=request.POST['selectedcategory']
		listClasses = []
		listClasses.append(request.POST['classes'])
		data['Classes'] = listClasses
		data['message'] = request.POST['message']
		json_data = json.dumps(data)
		print json_data
		postNoticeData(classSection,json_data,restKey,appKey)
		return render(request,'notice/list.html',{'alert':'alert','item1':"My first string",'classLinks':classLinks,'classNames':classNames,'zipped_data':zipped_data,'neatSection':neatSection})
	else:
		context = {'classSection':classSection,'neatSection':neatSection,'strippedSection':strippedSection,'javaKey':javaKey,'appKey':appKey}
		return render(request,'notice/notice.html',context)