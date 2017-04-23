#!/usr/binpython
#-*- coding:utf-8 -*-
from django.shortcuts import render , render_to_response
from django.http import HttpResponse , HttpResponseRedirect
from django import forms
from TodoApp.models import User , TodoList

# Create your views here.

class UserForm(forms.Form):
	username = forms.CharField(label='用户名' , max_length=50)
	email = forms.CharField(label='邮箱')
	password = forms.CharField(label='密码' , widget=forms.PasswordInput())
	repassword = forms.CharField(label='重复密码' , widget=forms.PasswordInput())

class LoginForm(forms.Form):
	username = forms.CharField(label="用户名" , max_length = 50)
	password = forms.CharField(label="密码" , widget = forms.PasswordInput())

class Todo(forms.Form):
	title = forms.CharField(label="标题" , max_length = 50)
	todo = forms.CharField(label="内容" , max_length = 200)


#设置默认首页
def index(request):
	return render(request , 'register.html')


#实现注册功能
def regist(request):
	if request.method == 'POST':
		userform = UserForm(request.POST)
		if userform.is_valid():
			username = userform.cleaned_data['username']
			email = userform.cleaned_data['email']
			password = userform.cleaned_data['password']
			repassword = userform.cleaned_data['repassword']

			NameFilter = User.objects.filter(username = username )
			EmailFilter = User.objects.filter(email = email )


			if password != repassword:
				return render(request , "register.html" , { 'errorcode':1 })
			elif len(NameFilter) != 0:
				return render(request , "register.html" , { 'errorcode':2 })
			elif len(EmailFilter) != 0:
				return render(request , "register.html" , { 'errorcode':3 })
			else:
				User.objects.create(username = username , password = password , email = email)
				return HttpResponseRedirect("/login/")

			
	else:
		userform = UserForm()
	return render(request , 'register.html' , {'userform':userform})


#实现登录功能
def login(request):
	if request.method == 'POST':
		loginform = LoginForm(request.POST)
		if loginform.is_valid():
			username = loginform.cleaned_data['username']
			password = loginform.cleaned_data['password']

			UserFilter = User.objects.filter(username = username , password = password)

			if len(UserFilter) == 1:
				request.session['username'] = username
				return HttpResponseRedirect("/todo/")
			else:
				return render(request , 'login.html' , { 'errorcode':1 })
	else:
		loginform = LoginForm()
		return render(request , 'login.html' , { 'loginform':loginform})


def todoList(request):
	username = request.session.get('username')
	List = TodoList.objects.filter(user = username).order_by('create_time')
	return render(request , 'todoList.html' , {'username':username , 'List':List})



def addlist(request):
	if request.method == "POST":
		todoform = Todo(request.POST)
		if todoform.is_valid():
			title = todoform.cleaned_data['title']
			todo = todoform.cleaned_data['todo']

			username = request.session.get("username")

			TodoList.objects.create(user = username , title = title , todo = todo)

			return HttpResponseRedirect("/todo/")
	else:
		todoform = Todo()
		username = request.session.get('username')
		return render(request , "todoList.html" , { 'todoform':todoform,'username':username})


def deletelist(request):
	list_id = request.GET['list_id']
	TodoList.objects.get(id = list_id).delete()
	return HttpResponseRedirect("/todo/")



def logout(request):
	del request.session['username']
	return HttpResponseRedirect("/login/")


def editlist(request):
	if request.method == 'POST':
		list_id = request.POST['list_id']
		return HttpResponse(list_id)
		


			






