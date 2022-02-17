from django.shortcuts import render,redirect,get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .forms import *
from .serializer import *
from rest_framework import status
from django.contrib.auth.decorators import login_required
from django.urls import  reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.db.models import  Avg

# Create your views here.
def index(request):
  return render(request, 'index.html')

@login_required
def profile(request,username):
  user = get_object_or_404(User,username=username)
  profile = Profile.objects.get(user=user)
  
  return render(request,'profile.html',{'user':user, 'profile':profile})

@login_required
def project(request):
  project = Project.objects.all()
  
  
  return render (request,'project.html',{'project':project})

@login_required
def project_detail(request,project_id):
  user = request.user
  project = get_object_or_404(Project, id=project_id)
  reviews = Review.objects.filter(project=project)
  if request.method == 'POST':
      form = ReviewForm(request.POST)
      if form.is_valid():
        reviews = form.save(commit=False)
        reviews.user= user
        reviews.project=project
        reviews.save()
        
        return HttpResponseRedirect(reverse('project_detail', args=[project_id]))
  else:
    form = ReviewForm()
  
  average_design = reviews.aggregate(Avg('design'))["design__avg"]
  average_usability = reviews.aggregate(Avg('usability'))["usability__avg"]
  average_content = reviews.aggregate(Avg('content'))["content__avg"]
  # average_design = round(average_design, 2)
  # average_usability = round(average_usability,2)
  # average_content = round(average_content,2)

  
  return render (request, 'project_detail.html',{'project':project, 'user':user, 'reviews':reviews,'form':ReviewForm,'average_design':average_design,'average_usability':average_usability,'average_content':average_content})


      
      
    
    
      

@login_required
def new_project(request):
  user = request.user
  profile = Profile.objects.get(user=request.user)
  
  if  request.method == 'POST':
    form = ProjectForm(request.POST, request.FILES)
    if form.is_valid():
      project =form.save(commit=False)
      project.profile = profile
      project.user = request.user
      project.save()
    return redirect('project')  
  else:
    form = ProjectForm()
  return render (request, 'newproject.html',{'form':form})  
  
@login_required
def update_profile(request, username):
  user = get_object_or_404(User,username=username)  
  new_user = request.user
  if request.method == 'POST':
    
    form = ProfileForm(request.POST, request.FILES)
    if form.is_valid():
      profile = form.save(commit=False)
      profile.user = new_user
      profile.save()
      
      return HttpResponseRedirect(reverse('profile', args=[username]))
    else:
      form = ProfileForm()
    
  return render(request, 'new_profile.html',{'user':user,'form':ProfileForm})   

@login_required
def search_project(request):
  if 'project' in request.GET and request.GET["project"]:
    search_term = request.GET.get('project')
    searched_projects = Project.search_title(search_term)
    message = f"{search_term}"
    
    return render (request, 'search.html',{"message":message, "projects":searched_projects})
  else:
    message = "Have you searched for any term?"
    return render (request,'search.html',{"message":message})  

class ProfileList(APIView):
  def get(self, request, format=None):
    profiles = Profile.objects.all()
    serializers = ProfileSerializer(profiles, many=True)
    return Response(serializers.data)

  def post(self, request,format=None):
    serializers = ProfileSerializer(data=request.data)
    if serializers.is_valid():
      serializers.save()
      return Response(serializers.data,status=status.HTTP_201_CREATED)
    return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
  
  
class ProjectList(APIView):
  def get(self,request,format=None):
    projects = Project.objects.all()
    serializers = ProjectSerializer(projects,many=True)
    return Response(serializers.data)
  
  def post(self,request,format=None):
    serializers=ProjectSerializer(data=request.data)
    if serializers.is_valid():
      serializers.save()
      return Response(serializers.data,status=status.HTTP_201_CREATED)
    return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)  