# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse

def index(request):
    return render_to_response('base.html',locals(),context_instance=RequestContext(request))