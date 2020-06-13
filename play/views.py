from django.shortcuts import render,reverse
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import requests
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
import random
import json

content={
    'General':'https://opentdb.com/api.php?amount=10&category=9&type=multiple',
    'book':'https://opentdb.com/api.php?amount=10&category=10&type=multiple',
    'film':'https://opentdb.com/api.php?amount=10&category=11&type=multiple',
    'animal':'https://opentdb.com/api.php?amount=10&category=27&type=multiple',
    'science':'https://opentdb.com/api.php?amount=10&category=17&type=multiple',
    'computer':'https://opentdb.com/api.php?amount=10&category=18&type=multiple',
    'math':'https://opentdb.com/api.php?amount=10&category=19&type=multiple',
    'mythology':'https://opentdb.com/api.php?amount=10&category=20&type=multiple',
    'sports':'https://opentdb.com/api.php?amount=10&category=21&type=multiple',
    'geography':'https://opentdb.com/api.php?amount=10&category=22&type=multiple',
    'history':'https://opentdb.com/api.php?amount=10&category=23&type=multiple',
    'Plotics':'https://opentdb.com/api.php?amount=10&category=24&type=multiple',
    'celebrities':'https://opentdb.com/api.php?amount=10&category=24&type=multiple',
    'Musics':'https://opentdb.com/api.php?amount=10&category=12&type=multiple',
    'Televisions': 'https://opentdb.com/api.php?amount=10&category=14&type=multiple',
    'mix':'https://opentdb.com/api.php?amount=10',

}
# Create your views here.
def index(req):
    if req.user.is_active:
        return HttpResponseRedirect(reverse('qlist'))
    return render(req,'login.html')

def log_in(req):
    name=''
    pas=''
    message=''
    if req.method=='POST':
        name=req.POST['username']
        pas=req.POST['pwd']
    user=authenticate(username=name,password=pas)
    if user is not None:
        login(req, user)
        message=f'Successfully Logged in {name}'
    else:
        message='Sorry User is not authenticated'
        return render(req,'login.html',{'msg':message,'alt':'alert-warning'})
    return HttpResponseRedirect(reverse('qlist'))

def sign_up(req):
    if req.POST:
        usr=req.POST['usr']
        pw=req.POST['pw']
        em=req.POST['em']
        usr=User.objects.create(username=usr,email=em,password=pw)
        login(req,usr)
        return HttpResponseRedirect(reverse('qlist'))
    return render(req,'signup.html')

def log_out(req):
    logout(req)
    return HttpResponseRedirect(reverse('home'))

@login_required
def qlist(req):
    return render(req,'quizlist.html',{'content':content})


correct_ans=[]
@login_required
def progress(req):
    r=requests.get(content[req.GET['p']])   
    r.encoding='utf-8'
    cont=[] 
    print(r.json())
    for j in r.json()['results']:
        rn=random.randint(0,2)
        if len(correct_ans)<10:
            correct_ans.append(rn)
        cont.append(
            {'question':j['question'],
              'answer':j["incorrect_answers"][:rn]+[j['correct_answer']]+j['incorrect_answers'][rn:]
              })
    return render(req,'progress.html',{'c':json.dumps(cont)})

def check(req):
    print(correct_ans)
    count=req.GET['count']
    return JsonResponse({'ans':correct_ans[int(count)]})
