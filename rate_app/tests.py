from django.test import TestCase
from django.contrib.auth.models import User
from .models import *


# Create your tests here.
class  ProfileTest(TestCase):
  def setUp(self):
    user = User.objects.create(username='morris',password = '5431')
    self.test = Profile(Bio='awesome projects',user=user)
    
  def test_instance(self):
    self.assertTrue(isinstance(self.test,Profile))
    
    
class ProjectTest(TestCase):
    def setUp(self):
      user =User.objects.create(username='morris',password='5431')
      profile = Profile.objects.create(user=user,Bio='awesome projects',email='morrison.githinji@student.moringaschoool.com',phone_number=1234567)   
      self.test = Project(user =user,title='test',description='lets test',project_link='www.test.com',profile=profile)
      
    def test_instance(self):
      self.assertTrue(isinstance(self.test,Project))   
      
    def test_save(self):
      self.test.save_project()
      saved = Project.objects.all()
      self.assertTrue(len(saved)>0)
      
    def test_delete(self):
      self.test.save_project()
      self.test.delete_project()
      deleted = Project.objects.all()
      self.assertTrue(len(deleted)== 0) 
      
    def tearDown(self):
      Project.objects.all().delete()
      
      
class ReviewTest(TestCase):
  
  def setUp(self):
   user =User.objects.create(username='morris',password='5431')
   profile = Profile.objects.create(user=user,Bio='awesome project',email='morrison.githinji@student.moringaschoool.com',phone_number=1234567) 
   project = Project.objects.create(user=user,title='lets test',description='we can',project_link='www.iwill.com',profile=profile)  
    
   self.test = Review (user=user,project=project,review='you actually did it',design=5,usability=6,content=4)
   
  def test_instance(self):
    self.assertTrue(isinstance(self.test,Review)) 
    
    

        