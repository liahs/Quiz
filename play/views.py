from django.shortcuts import render,reverse
from django.contrib.auth import login,authenticate,logout
import requests
from django.http import HttpResponse,HttpResponseRedirect

# Create your views here.
def index(req):
    if req.user.is_active:
        return render(req,'index.html')
    return render(req,'login.html')

def log_out(req):
    logout(req)
    return HttpResponseRedirect(reverse('home'))