from django.contrib import admin
from play.models import QuesAndAns,Signup
# Register your models here.

admin.site.site_header = "QuizManiac"

class QuesAndAnsAdmin(admin.ModelAdmin):
    list_display = ["user","ques","ans"]
    search_fields = ["user","ques"]
    list_filter = ["user"]

class SignupAdmin(admin.ModelAdmin):
    list_display = ["user","pas","failed"]
    search_fields = ["user"]

admin.site.register(QuesAndAns,QuesAndAnsAdmin)
admin.site.register(Signup,SignupAdmin)