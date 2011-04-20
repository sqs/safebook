from django.contrib.auth.models import User
from django.http import HttpResponseNotFound
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

def index(request):
    users = User.objects.all()
    return render_to_response('profiles/index.html', {'allusers': users},
                              context_instance=RequestContext(request))

def detail(request, username):
    thisuser = get_object_or_404(User, username=username)
    return render_to_response('profiles/detail.html', {'thisuser': thisuser},
                              context_instance=RequestContext(request))

