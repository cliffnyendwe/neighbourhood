from django import forms
from .models import Update , Profile , Comment , Business  , Neighborhood
from django.contrib.auth.models import User



class UpdateForm ( forms.ModelForm ):
    class Meta :
        model = Update
        fields = [  'post' ,  'picture'

        ]
class CommentForm (forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'comment'
        ]
        widgets = {
            'comment': forms.TextInput(attrs={'class': 'form-control' , 'id': 'publisherInput1'}),
        }


class UserUpdateForm (forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'id': 'publisherInput1'}),
        }
class ProfileUpdateForm (forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'neighborhood', 'about']

        widgets = {
            'about': forms.Textarea(attrs={'class': 'form-control', 'id': 'publisherInput1'}),
        }
class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = [ 'name', 'email' 
           
        ]

class HoodForm( forms.ModelForm ):
    class Meta:
        model = Neighborhood
        fields = [  'name', 'city'
          
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'publisherInput1'}),
        }
