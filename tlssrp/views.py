from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from safebook.tlssrp.models import SRPUserInfo
from safebook.tlssrp.forms import SRPUserCreationForm, SRPUserEditForm

def register(request):
    if request.method == 'POST':
        form = SRPUserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            url = "https://safebook.trustedhttp.org/" + new_user.username
            return HttpResponseRedirect(url)
    else:
        form = SRPUserCreationForm()
    return render_to_response("tlssrp/register.html", {'form': form},
                              context_instance=RequestContext(request))

def edit(request, username):
    if request.user.username != username:
        return HttpResponseForbidden()
    user = get_object_or_404(User, username=username)
    try:
        srpinfo = SRPUserInfo.objects.get(user=user)
    except SRPUserInfo.DoesNotExist:
        srpinfo = SRPUserInfo(user=user)
    if request.method == 'POST':
        form = SRPUserEditForm(request.POST, instance=srpinfo)
        if form.is_valid():
            form.save()
    else:
        form = SRPUserEditForm(instance=srpinfo)
    return render_to_response('tlssrp/edit.html', {'form': form, 'user': user},
                              context_instance=RequestContext(request))
