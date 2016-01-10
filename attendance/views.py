from django.shortcuts import render
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


# Create your views here.

def getStudentList(classSection):
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
	return result['results'][0]['Student_Name']

def getUsernames(classSection):
	connection = httplib.HTTPSConnection('api.parse.com', 443)
	params = urllib.urlencode({"where":json.dumps({"Class_Name": classSection,}),"limit":999})
	connection.connect()
	connection.request('GET', '/1/classes/_User?%s' % params, '', {
			"X-Parse-Application-Id": "Sqj2XR5GDdMcXuMsffDQ9yEdzhYJqBZYvDSMLqFC",
		   "X-Parse-REST-API-Key": "Ox5FKRyiEM33GzS7Ka6oTJCXRIjiPghotbD9dWPx"
			})
	userNames = json.loads(connection.getresponse().read())
	return userNames['results']

def postAttendanceData(classSection,json_data):
	connection = httplib.HTTPSConnection('api.parse.com', 443)
	connection.connect()
	connection.request('POST', '/1/classes/' + classSection , json_data, {
		   "X-Parse-Application-Id": "Sqj2XR5GDdMcXuMsffDQ9yEdzhYJqBZYvDSMLqFC",
		   "X-Parse-REST-API-Key": "Ox5FKRyiEM33GzS7Ka6oTJCXRIjiPghotbD9dWPx",
		   "Content-Type": "application/json"
		 })
	results = json.loads(connection.getresponse().read())
	print results


@login_required
def index(request):
	context = {'item1':"My first string"}
	return render(request,'attendance/list.html',context)	

@login_required
def viewAttendance(request,classSection):
	neatSection = classSection[1:-1] + " " + classSection[-1]
	strippedSection = classSection[1:]
	context = {'classSection':classSection,'neatSection':neatSection,'strippedSection':strippedSection}
	return render(request,'attendance/viewAttendance.html',context)

@login_required
def enterAttendance(request,classSection):
	studentList = getStudentList(classSection)
	if request.method == 'POST':
		userNames = getUsernames(classSection)
		absentStudents = request.POST
		data = {}
		# For loop to iterate over list of students and assign 'A' or 'P'.
		# Also sends emails to absent students' parents
		for student in studentList:
			studentMod = student.replace (" ", "_")
			studentMod = "R" + studentMod
			if(student in absentStudents):
				data[studentMod] = "A"
				userdata = (user for user in userNames if user["username"] == classSection+student).next()
				if 'email' in userdata:
					print 'email the person!'
					email = EmailMessage('Hello there', 'well well, your son was absent today', to=[userdata['email']])
					print userdata['email']
					email.send()
				else:
					print 'ask them to enter their e-mail!'

			else:
				data[studentMod] = "P"
		data['cDate'] = request.POST['date']
		dateOfAttendance = data['cDate']
		start = dateOfAttendance.find('/')
		end = dateOfAttendance.rfind('/')
		data['mdate'] = int(dateOfAttendance[start+1:end])
		json_data = json.dumps(data)
		postAttendanceData(classSection,json_data)					
		return HttpResponseRedirect(reverse('attendance:index'))
	else:	
		neatSection = classSection[1:-1] + " " + classSection[-1]
		strippedSection = classSection[1:]

		context = {'classSection':classSection,'neatSection':neatSection,'strippedSection':strippedSection,'studentList':studentList}
		return render(request,'attendance/enterAttendance.html',context)

class UploadFileForm(forms.Form):
	file = forms.FileField()

@login_required
def uploadAttendance(request,classSection):
	if request.method == "POST":
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			filehandle = request.FILES['file']
			attendanceExcel = request.FILES['file'].get_array()
			for i in range(1,len(attendanceExcel)):
				print attendanceExcel[i]
	else:
		form = UploadFileForm()
	return render_to_response(
		'attendance/upload_form.html',
		{
			'form': form,
			'title': 'Excel file upload and download example',
			'header': 'Please choose any excel file from your cloned repository:'
		},
		context_instance=RequestContext(request))
