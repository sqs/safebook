from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from safebook.tlssrp.forms import SRPUserCreationForm

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
