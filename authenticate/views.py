from django.shortcuts import render,redirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponse
from django.contrib.auth import authenticate, login

# def home(request):
# 	if request.user and not request.user.is_anonymous():
# 		print "#$@#%$#$%^$&^"
# 		request.session['userid'] = str(request.user)
# 		return redirect('/')
# 	else:
# 		context = RequestContext(request,{'request': request,'user': None})
# 		return render_to_response('authenticate/login.html',context_instance=context)

def home(request):
    state = "Please log in below..."
    username = password = ''
    context = RequestContext(request,{'state':state, 'username': username})
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                state = "You're successfully logged in!"
                return redirect('/attendance')
            else:
                state = "Your account is not active, please contact the site admin."
        else:
            state = "Your username and/or password were incorrect."
            context = RequestContext(request,{'state':state, 'username': username})

    return render_to_response('authenticate/auth.html',context_instance=context)