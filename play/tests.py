from django.test import TestCase
from django.contrib.auth.models import User
from .models import  QuesAndAns,Signup


# Create your tests here.

class ModelTestCase(TestCase):
    def setUp(self):
        u1=User.objects.create(username="liahs",email="liahschhetri2@gmail.com",password="hellodear")
        s1=Signup.objects.create(user=u1,pas=6,failed=4)

        u2=User.objects.create(username="shail",email="liahschhetri2@gmail.com",password="helloworld")
        s2=Signup.objects.create(user=u2,pas=0,failed=3)

        q1=QuesAndAns.objects.create(user=u1,ques='What is the name of Iron man ?',ans='Tony Stark')
        q2=QuesAndAns.objects.create(user=u1,ques='What is the name of Black panther>?',ans='TRovy')
        q3=QuesAndAns.objects.create(user=u2,ques='Who is wanda maxioff?',ans='Crimson witch')

    def test_users_passed(self):
        u=User.objects.get(username='liahs')
        a=Signup.objects.get(user=u)
        self.assertEqual(a.pas,6)

    def test_users_failed(self):
        u=User.objects.get(username='shail')
        a=Signup.objects.get(user=u)
        self.assertEqual(a.failed,3)
    
    def test_ques_answer_count(self):
        user=User.objects.get(username='liahs')
        self.assertEqual(user.qns_ans.count(),2)
        user=User.objects.get(username='shail')
        self.assertEqual(user.qns_ans.count(),1)
    
