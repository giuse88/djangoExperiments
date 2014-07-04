from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponse
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def index(request):
  category_list = Category.objects.order_by('-likes')
  context_dict = { 'categories' : category_list} 
  #
  for category in category_list:
    category.url = category.name.replace(' ','_')
  #
  return render(request, 'rango/index.html', context_dict) 

def about(request):
  return HttpResponse("This is the about page! <a href='/rango'>Index</a>"); 

def category(request, category_name_url):
  category_name = category_name_url.replace('_', ' ')
  context_dict = {'category_name':category_name}
  try :
    #Is this code making two queries ?
    category = Category.objects.get(name=category_name)
    pages = Page.objects.filter(category=category)
    context_dict['pages'] = pages
    context_dict['category'] = category
  except Category.DoesNotExist:
    pass
  return render(request, 'rango/category.html', context_dict)

def add_category(request):
  if request.method == 'POST':
    form = CategoryForm(request.POST)
    if form.is_valid() :
      form.save(commit=True)
      return index(request)
    else :
      print form.errors
  else :
    form = CategoryForm()
  return render(request, 'rango/add_category.html', {'form':form})

def add_page(request):
  if request.method == 'POST':
    form = PageForm(request.POST)
    if form.is_valid() :
      try:
        page = form.save(commit=False)
        selected_category = form.cleaned_data['categories']
        cat = Category.objects.get(name=selected_category)
        page.category = cat
      except Category.DoesNotExist:
        return render(request, 'rango/add_category.html', {})
      page.views=0
      page.save()
      return HttpResponseRedirect('category/' + selected_category)  
    else:
      print form.errors
  else:
    form = PageForm()
  return render(request, 'rango/add_page.html', {'form':form})

def register(request):
  registered = False
  if request.method == 'POST':
    user_form = UserForm(data=request.POST)
    profile_form = UserProfileForm(data=request.POST)
    
    if user_form.is_valid() and profile_form.is_valid():
      user = user_form.save()
      user.set_password(user.password)
      user.save()
      profile = profile_form.save(commit=False)
      profile.user = user
      if 'picture' in request.FILES:
        profile.picture = request.FILES['picture']
      profile.save()
      registered = True
    else:
      print user_form.errors, profile_form.errors 
  else:
    user_form = UserForm()
    profile_form = UserProfileForm()

  return render(request, 'rango/register.html',
      {'user_form':user_form, 'profile_form':profile_form, 'registered': registered})


def user_login(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']

    user= authenticate(username=username, password=password)
    if user: 
      if user.is_active:
        login(request, user)
        return HttpResponseRedirect('/rango')
      else:
        return HttpResponse("You rango account is disabled")
    else:
      print "Invalid login details : {0}, {1}".format(username, password)
      return HttpResponse("Invalid login details supplied.")
  else : 
    return render(request, 'rango/login.html',{})

@login_required
def restricted(request):
  return HttpResponse("Since you are logged in, you can see this")

@login_required 
def user_logout(request):
  logout(request)
  return HttpResponseRedirect('/rango')
