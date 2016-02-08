from django.shortcuts import render
# Create your views here.
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
from django.contrib.auth.models import User
from attendance.models import ListOfClasses


def getStudentList(classSection,restKey,appKey):
	connection = httplib.HTTPSConnection('api.parse.com', 443)
	params = urllib.urlencode({"where":json.dumps({
		   "Class_Name": '%s' % classSection
		 })})
	connection.connect()
	connection.request('GET', '/1/classes/Class?%s' % params, '', {
		   # "X-Parse-Application-Id": "Sqj2XR5GDdMcXuMsffDQ9yEdzhYJqBZYvDSMLqFC",
		   # "X-Parse-REST-API-Key": "Ox5FKRyiEM33GzS7Ka6oTJCXRIjiPghotbD9dWPx",
		   "X-Parse-Application-Id": appKey,
		   "X-Parse-REST-API-Key": restKey
		 })
	result = json.loads(connection.getresponse().read())
	# print result
	return result['results'][0]['Student_Name']


def postClassTable(json_data,theclass,theuser,restKey,appKey,javaKey,masterKey):
	connection = httplib.HTTPSConnection('api.parse.com', 443)
	connection.connect()
	connection.request('POST', '/1/classes/Class', json_data, {
		   "X-Parse-Application-Id": appKey,
		   "X-Parse-REST-API-Key": restKey,
		   "Content-Type": "application/json"
		 })
	results = json.loads(connection.getresponse().read())
	q=ListOfClasses(schoolUser=theuser,someClass=theclass,appKey=appKey,restKey=restKey, javaKey=javaKey, masterKey=masterKey)
	q.save()

	#print results

def postListClassTable(classNumber,classSection,restKey,appKey,masterKey):
	# Change Schema
	print masterKey
	fullname = 'c' + classNumber + classSection
	partname = classNumber + classSection 
	data = {}
	data['className'] = "List_Class"
	data['fields'] = {}
	data['fields'][fullname] = {}
	data['fields'][fullname]['type'] = "Array"
	json_data = json.dumps(data)
	print json_data 
	connection = httplib.HTTPSConnection('api.parse.com', 443)
	connection.connect()
	connection.request('PUT', '/1/schemas/List_Class', json_data, {
	       "X-Parse-Application-Id": appKey,
	       "X-Parse-Master-Key": masterKey,
	       "Content-Type": "application/json"
	     })
	print "Changing the schema"
	result = json.loads(connection.getresponse().read())
	print result

	# Update
	data = {}
	data["Class_List"] = {}
	data["Class_List"]["__op"] = "AddUnique"
	data["Class_List"]["objects"] = [partname]
	data[fullname] = {}
	data[fullname]["__op"] = "AddUnique"
	data[fullname]["objects"] = ["English", "Hindi"]
	json_data = json.dumps(data)
	connection = httplib.HTTPSConnection('api.parse.com', 443)
	connection.connect() 
	connection.request('PUT', '/1/classes/List_Class/1hKtVUxgOI', json_data, {
	   "X-Parse-Application-Id": appKey,
	   "X-Parse-REST-API-Key": restKey,
	   "Content-Type": "application/json"
	 })
	result = json.loads(connection.getresponse().read())
	print result

	
@login_required
def index(request):
	latest_class_list = ListOfClasses.objects.filter(schoolUser=request.user)	
	classLinks = [p.someClass for p in latest_class_list]
	classNames = [p[1:-1] + " " + p[-1] for p in classLinks]
	zipped_data = zip(classLinks, classNames)
	firstInstance = ListOfClasses.objects.filter(schoolUser=request.user).first()
	restKey = firstInstance.restKey
	javaKey = firstInstance.javaKey
	appKey 	= firstInstance.appKey
	masterKey = firstInstance.masterKey
	context = {'item1':"My first string",'classLinks':classLinks,'classNames':classNames,'zipped_data':zipped_data}
	if request.method == 'POST':
		classNumber = request.POST['classNumber']
		classSection = request.POST['classSection']
		data = {}
		data['Class_Name'] = 'c' + request.POST['classNumber'] + request.POST['classSection']
		data['Student_Name'] = []
		json_data = json.dumps(data)
		postClassTable(json_data,data['Class_Name'],request.user,restKey,appKey,javaKey,masterKey)		
		postListClassTable(classNumber,classSection,restKey,appKey,masterKey)
		context['alert'] = 'alert'
		return render(request,'records/list.html',context)
	else:
		return render(request,'records/list.html',context)	

@login_required
def enterStudents(request,classSection):
	latest_class_list = ListOfClasses.objects.filter(schoolUser=request.user)	
	classLinks = [p.someClass for p in latest_class_list]
	classNames = [p[1:-1] + " " + p[-1] for p in classLinks]
	zipped_data = zip(classLinks, classNames)
	firstInstance = ListOfClasses.objects.filter(schoolUser=request.user).first()
	restKey = firstInstance.restKey
	javaKey = firstInstance.javaKey
	appKey 	= firstInstance.appKey
	studentList = getStudentList(classSection,restKey,appKey)
	studentRoll = list(p.split()[0] for p in studentList)
	counterOfPreviousStudents = len(studentRoll) + 1
	studentFirstName = list(p.split()[1] for p in studentList)
	studentLastName = []
	for p in studentList:
		try:
			x = p.split()[2:]
			x = ' '.join(x)
			studentLastName.append(x)
		except:
			studentLastName.append('')
	zipped_student = zip(studentRoll,studentFirstName,studentLastName)
	# print studentRoll
	# print studentFirstName
	# print studentLastName
	# return HttpResponse("return this string")

	if request.method == 'POST':
		userNames = getUsernames(classSection,restKey,appKey)
		absentStudents = request.POST
		data = {}
		data['cDate'] = request.POST['date']
		dateOfAttendance = data['cDate']
		myDateObject = datetime.strptime(dateOfAttendance,'%d/%m/%Y')
		myDateObject = myDateObject.strftime("%d %B %Y")
		# For loop to iterate over list of students and assign 'A' or 'P'.
		# Also sends emails to absent students' parents
		for student in studentList:
			studentMod = student.replace (" ", "_")
			studentMod = "R" + studentMod
			if(student in absentStudents):
				data[studentMod] = "A"
				userdata = (user for user in userNames if user["username"] == classSection+student).next()
				# if 'email' in userdata:
				# 	print 'email the person!'
				# 	email = EmailMessage('Hello there', 'well well, your son was absent today', to=[userdata['email']])
				# 	print userdata['email']
				# 	email.send()
				# else:
				# 	print 'ask them to enter their e-mail!'
				if 'phoneNumber' in userdata:
					# print 'Starting now'
					try:
						childName = userdata["username"].split()
						childName = childName[1] +  " " + childName[2]
					except:
						childName = "Your child"
					myMessage =  childName + ' was absent on ' + myDateObject
					myNumber = userdata['phoneNumber']
					# print 'Is this where I go wrong?'
					params = urllib.urlencode({'user': 'Saurabh', 'password': '123@123', 'mobiles': myNumber, 'sms':myMessage,'senderid':'PTMNOW','version':3})
					# print 'Or here?'
					f = urllib.urlopen("http://trans.profuseservices.com/sendsms.jsp?%s" % params)
					print f.read()
			else:
				data[studentMod] = "P"
		start = dateOfAttendance.find('/')
		end = dateOfAttendance.rfind('/')
		data['mdate'] = int(dateOfAttendance[start+1:end])
		json_data = json.dumps(data)
		postAttendanceData(classSection,json_data,restKey,appKey)					
		# return HttpResponseRedirect(reverse('attendance:index'))
		#return redirect(reverse('attendance:index'), {'alert':'alert'})
		return render(request,'attendance/list.html',{'alert':'alert',"classSection":classSection,'classLinks':classLinks,'classNames':classNames,'zipped_data':zipped_data})
	else:	
		neatSection = classSection[1:-1] + " " + classSection[-1]
		strippedSection = classSection[1:]
		# print zipped_student
		context = {'classSection':classSection,'neatSection':neatSection,'strippedSection':strippedSection,'studentList':studentList,'appKey':appKey,'javaKey':javaKey,'zipped_student':zipped_student,'my_range': range(counterOfPreviousStudents,80)}
		return render(request,'records/enterStudents.html',context)








######## Misc Commented Code ################

	# connection.connect()
	# connection.request('GET', '/1/classes/List_Class', '', {
	# 	   "X-Parse-Application-Id": appKey,
	# 	   "X-Parse-REST-API-Key": restKey,
	# 	   "Content-Type": "application/json"
	# 	 })
	# results = json.loads(connection.getresponse().read())
	# results = results['results'][0]
	# results['c' + classNumber + classSection] = ['Hindi','English']
	# results['Class_List'].append(classNumber+classSection)
	# del results['createdAt']
	# del results['updatedAt']
	# objectID = results["objectId"]
	# del results['objectId']
	# json_data = json.dumps(results)
	# # Delete old record
	# connection = httplib.HTTPSConnection('api.parse.com', 443)
	# connection.connect()
	# connection.request('DELETE', '/1/classes/List_Class/'+objectID, json_data, {
	# 	   "X-Parse-Application-Id": appKey,
	# 	   "X-Parse-REST-API-Key": restKey,
	# 	   "Content-Type": "application/json"
	# 	 })
	# results = json.loads(connection.getresponse().read())
	# print "Delete:"
	# print results


	# # Add new data
	# connection = httplib.HTTPSConnection('api.parse.com', 443)
	# connection.connect()
	# connection.request('POST', '/1/classes/List_Class', json_data, {
	# 	   "X-Parse-Application-Id": appKey,
	# 	   "X-Parse-REST-API-Key": restKey,
	# 	   "Content-Type": "application/json"
	# 	 })
	# results = json.loads(connection.getresponse().read())
	# print "Insert:"
	# print results