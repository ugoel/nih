from django.shortcuts import render_to_response

from django.http import HttpResponse
from django.utils import simplejson
#from Test import main

#import quepy
from main import getdata

def index(request):
    return render_to_response('index.html', {'text_test': 'Hello World'})

def calltest():
    print "tesing call"

def testing(request):
    
    result = getdata(request.GET["param1"])
    
    print result
    
    return HttpResponse(simplejson.dumps(result), mimetype='application/json')
    
