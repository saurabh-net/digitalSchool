from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
import json,httplib,urllib
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
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
	return render(request,'marks/list.html',context)	

@login_required
def viewMarks(request,classSection):
	firstInstance = ListOfClasses.objects.filter(schoolUser=request.user).first()
	restKey = firstInstance.restKey
	javaKey = firstInstance.javaKey
	appKey 	= firstInstance.appKey
	neatSection = classSection[1:-1] + " " + classSection[-1]
	strippedSection = classSection[1:]
	context = {'classSection':classSection,'neatSection':neatSection,'strippedSection':strippedSection,'appKey':appKey,'javaKey':javaKey}
	return render(request,'marks/viewMarks.html',context)
	
@login_required
def enterMarks(request,classSection):
	firstInstance = ListOfClasses.objects.filter(schoolUser=request.user).first()
	restKey = firstInstance.restKey
	javaKey = firstInstance.javaKey
	appKey 	= firstInstance.appKey

	connection = httplib.HTTPSConnection('api.parse.com', 443)
	params = urllib.urlencode({"where":json.dumps({
	       "Class_Name": '%s' % classSection
	     })})
	connection.connect()
	connection.request('GET', '/1/classes/Class?%s' % params, '', {
	       # "X-Parse-Application-Id": "Sqj2XR5GDdMcXuMsffDQ9yEdzhYJqBZYvDSMLqFC",
	       # "X-Parse-REST-API-Key": "Ox5FKRyiEM33GzS7Ka6oTJCXRIjiPghotbD9dWPx"
	       "X-Parse-Application-Id": appKey,
	       "X-Parse-REST-API-Key": restKey
	     })
	result = json.loads(connection.getresponse().read())
	studentList = result['results'][0]['Student_Name']

	if request.method == 'POST':
		latest_class_list = ListOfClasses.objects.filter(schoolUser=request.user);
		classLinks = [p.someClass for p in latest_class_list]
		classNames = [p[1:-1] + " " + p[-1] for p in classLinks]
		zipped_data = zip(classLinks, classNames)

		submittedData = request.POST
		data = {}
		for student in studentList:
			studentMod = student.replace (" ", "_")
			studentMod = "R" + studentMod
			if submittedData[student] == "":
				data[studentMod] = -1
			else:
				data[studentMod] = int(submittedData[student])

		data['cDate'] = submittedData['date']
		data['Category'] = submittedData['category']
		data['MaxMarks'] = int(submittedData['total'])
		data['Subject'] = submittedData['subject']
		data['UMI'] = submittedData['date'] + classSection + submittedData['subject'] + submittedData['category']
		json_data = json.dumps(data)

		connection = httplib.HTTPSConnection('api.parse.com', 443)
		connection.connect()
		connection.request('POST', '/1/classes/Marks' + classSection, json_data, {
		       # "X-Parse-Application-Id": "Sqj2XR5GDdMcXuMsffDQ9yEdzhYJqBZYvDSMLqFC",
		       # "X-Parse-REST-API-Key": "Ox5FKRyiEM33GzS7Ka6oTJCXRIjiPghotbD9dWPx",
		       "X-Parse-Application-Id": appKey,
		       "X-Parse-REST-API-Key": restKey,
		       "Content-Type": "application/json"
		     })
		results = json.loads(connection.getresponse().read())
		# print results					
		# return HttpResponseRedirect(reverse('marks:index'))
		# return render(request,'marks/list.html',{'alert':'alert',"classSection":classSection,'classLinks':classLinks,'classNames':classNames,'zipped_data':zipped_data})
		# return HttpResponse(json_data)
		return render(request,'marks/list.html',{'alert':'alert',"classSection":classSection,'classLinks':classLinks,'classNames':classNames,'zipped_data':zipped_data})
		# return render(request,'attendance/list.html',{'alert':'alert',"classSection":classSection,'classLinks':classLinks,'classNames':classNames,'zipped_data':zipped_data})

	else:	
		neatSection = classSection[1:-1] + " " + classSection[-1]
		strippedSection = classSection[1:]

		context = {'classSection':classSection,'neatSection':neatSection,'strippedSection':strippedSection,'studentList':studentList}
		return render(request,'marks/enterMarks.html',context)

