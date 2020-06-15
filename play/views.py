from django.shortcuts import render,reverse,get_object_or_404
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from play.models import QuesAndAns,Signup
import requests
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.core.mail import EmailMessage
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
    if req.method=='POST':
        name=req.POST['username']
        pas=req.POST['pwd']
        user=authenticate(username=name,password=pas)
        print(user)
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
        usr=User.objects.create_user(username=usr,email=em,password=pw)
        Signup.objects.create(user=usr)
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
    prev=0 
    for j in r.json()['results']:
        rn=random.randint(0,3)
        if prev==rn:
            if rn==3:
                rn=random.randint(0,2)
            if rn==0:
                rn=random.randint(1,3)
            if rn==1:
                rn=random.randint(2,3)
            else:
                rn=random.randint(0,1)
        prev=rn
        incorrects=j["incorrect_answers"]+[0]
        print(incorrects)
        if len(correct_ans)<10:
            correct_ans.append(rn)
        cont.append(
            {'question':j['question'],
              'answer':incorrects[:rn]+[j['correct_answer']]+j['incorrect_answers'][rn:4]
              })
        print(incorrects[:rn]+[j['correct_answer']]+j['incorrect_answers'][rn:4])
    return render(req,'progress.html',{'c':json.dumps(cont)})

def check(req):
    print(correct_ans)
    count=req.GET['count']
    return JsonResponse({'ans':correct_ans[int(count)]})

@login_required
def dashboard(req):
    qan=QuesAndAns.objects.filter(user=req.user)
    usr=Signup.objects.get(user=req.user)
    passed=usr.pas
    failed=usr.failed
    print(passed)
    print(failed)
    total=passed+failed
   
    return render(req,'dashboard.html',{'passed':passed,'failed':failed,'total':total,'qan':qan})

@login_required
def add_qans(req):
    question=req.GET["qns"]
    answer=req.GET["ans"]
    QuesAndAns.objects.create(user=req.user,ques=question,ans=answer)
    return JsonResponse({'added':'saved'})
    
@login_required
def pass_fail(req):
    usr=Signup.objects.get(user=req.user)
    if req.GET['result']=='Pass':
        usr.pas+=1
    if req.GET['result']=='Fail':
        usr.failed+=1
    usr.save()
    return JsonResponse({'status':'ok'})

def check_user(req):
    if req.method=="GET":
        un = req.GET["usern"]
        check = User.objects.filter(username=un)
        if len(check) == 1:
            return HttpResponse("Exists")
        else:
            return HttpResponse("Not Exists")

def resetpass(req):
    print(req.POST)
    if req.method=='POST':
        us = User.objects.get(username=req.POST['username'])
        us.set_password(req.POST["npass"])
        us.save()
        login(req,us)
        return HttpResponseRedirect(reverse('qlist'))
    if req.method=='GET':
        try:
            un = req.GET["username"]
            user = get_object_or_404(User,username=un)
            otp = random.randint(1000,9999)
            msz = "Dear {} \n {} is your one time password (OTP) dont not share with others \n Thanks & Regards \n QuizManiac".format(user.username,otp)
            try:
                email = EmailMessage("Account Verification",msz,to=[user.email])
                email.send()
                return JsonResponse({"status": "sent","email":user.email,"rotp":otp})
            except:
                return JsonResponse({"status": "error","email":user.email})

        except:
            return JsonResponse({"status":"failed"})


def forget_pass(req):
    return render(req,'forgetpass.html')

def password_change(req):
    if req.GET:
        user=get_object_or_404(User,id=req.user.id)
        pas=req.GET["pas"]
        user.set_password(pas)
        user.save()
        login(req,user)
        return JsonResponse({'msg':'Successfully password is changed!!!'})
@login_required
def change_pass(req):
    return render(req,'changepass.html')

        