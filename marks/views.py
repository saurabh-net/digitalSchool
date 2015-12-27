from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
import json,httplib,urllib
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

# Create your views here.

def index(request):
	context = {'item1':"My first string"}
	return render(request,'marks/list.html',context)	

def viewMarks(request,classSection):
	neatSection = classSection[1:-1] + " " + classSection[-1]
	strippedSection = classSection[1:]
	context = {'classSection':classSection,'neatSection':neatSection,'strippedSection':strippedSection}
	return render(request,'marks/viewMarks.html',context)

def enterMarks(request,classSection):
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
		data['UMI'] = submittedData['date'] + 'cNurseryA' + submittedData['subject'] + submittedData['category']
		json_data = json.dumps(data)

		connection = httplib.HTTPSConnection('api.parse.com', 443)
		connection.connect()
		connection.request('POST', '/1/classes/MarkscNurseryA', json_data, {
		       "X-Parse-Application-Id": "Sqj2XR5GDdMcXuMsffDQ9yEdzhYJqBZYvDSMLqFC",
		       "X-Parse-REST-API-Key": "Ox5FKRyiEM33GzS7Ka6oTJCXRIjiPghotbD9dWPx",
		       "Content-Type": "application/json"
		     })
		results = json.loads(connection.getresponse().read())
		print results					
		# return HttpResponseRedirect(reverse('marks:index'))
		return HttpResponse(json_data)
	else:	
		neatSection = classSection[1:-1] + " " + classSection[-1]
		strippedSection = classSection[1:]

		context = {'classSection':classSection,'neatSection':neatSection,'strippedSection':strippedSection,'studentList':studentList}
		return render(request,'marks/enterMarks.html',context)

