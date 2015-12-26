from django.shortcuts import render
from django.http import HttpResponse
import json,httplib,urllib
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

# Create your views here.

def index(request):
	context = {'item1':"My first string"}
	return render(request,'attendance/list.html',context)	

def viewAttendance(request,classSection):
	neatSection = classSection[1:-1] + " " + classSection[-1]
	strippedSection = classSection[1:]
	context = {'classSection':classSection,'neatSection':neatSection,'strippedSection':strippedSection}
	return render(request,'attendance/viewAttendance.html',context)

def markAttendance(request,classSection):
	connection = httplib.HTTPSConnection('api.parse.com', 443)
	params = urllib.urlencode({"where":json.dumps({
	       "Class_Name": '%s' % classSection
	     })})
	connection.connect()
	connection.request('GET', '/1/classes/Class?%s' % params, '', {
	       "X-Parse-Application-Id": "Sqj2XR5GDdMcXuMsffDQ9yEdzhYJqBZYvDSMLqFC",
	       "X-Parse-REST-API-Key": "Ox5FKRyiEM33GzS7Ka6oTJCXRIjiPghotbD9dWPx"
	     })
	result = json.loads(connection.getresponse().read())
	studentList = result['results'][0]['Student_Name']

	if request.method == 'POST':
		absentStudents = request.POST
		data = {}
		for student in studentList:
			studentMod = student.replace (" ", "_")
			studentMod = "R" + studentMod
			if(student in absentStudents):
				data[studentMod] = "A"
			else:
				data[studentMod] = "P"
		data['cDate'] = request.POST['date']
		data['mdate'] = 12
		json_data = json.dumps(data)

		connection = httplib.HTTPSConnection('api.parse.com', 443)
		connection.connect()
		connection.request('POST', '/1/classes/cNurseryA', json_data, {
		       "X-Parse-Application-Id": "Sqj2XR5GDdMcXuMsffDQ9yEdzhYJqBZYvDSMLqFC",
		       "X-Parse-REST-API-Key": "Ox5FKRyiEM33GzS7Ka6oTJCXRIjiPghotbD9dWPx",
		       "Content-Type": "application/json"
		     })
		results = json.loads(connection.getresponse().read())
		print results
					
		return HttpResponseRedirect(reverse('attendance:index'))
	else:	
		neatSection = classSection[1:-1] + " " + classSection[-1]
		strippedSection = classSection[1:]

		context = {'classSection':classSection,'neatSection':neatSection,'strippedSection':strippedSection,'studentList':studentList}
		return render(request,'attendance/markAttendance.html',context)

