from django.shortcuts import render,redirect,render_to_response
from django.http import HttpResponse,Http404
from django.template.context import RequestContext

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
import json,httplib,urllib
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required


# Create your views here.

def index(request):
	context = {'item1':"My first string"}
	return render(request,'welcome.html',context)	

# @login_required
# def home(request):
# 	try:
# 		if 'userid' in request.session.keys():
# 			context = RequestContext(request,{'request': request,'user': request.user})
# 			return render_to_response('welcome.html',context_instance=context)
# 		else:
# 			print 'nope, failed'
# 			return redirect('/accounts/login')
# 	except:
# 		raise Http404

@login_required
def home(request):
	context = {'item1':"My first string"}
	return render(request,'welcome.html',context)	