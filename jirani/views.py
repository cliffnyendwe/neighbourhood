from django.shortcuts import render , redirect , get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Neighborhood , Profile , Business , Update , Comment
from .forms import UpdateForm , UserUpdateForm , ProfileUpdateForm , CommentForm , BusinessForm ,NewBusinessForm, HoodForm

@login_required( login_url= '/accounts/login')
def index(request):
    '''
    The first view user is redirected to upon signing in 
    '''
    update_form = UpdateForm()
    comment_form = CommentForm()

    try:
        updates = Update.get_hood_updates(request.user.profile.neighborhood)[::-1]
        comments = Comment.get_hood_comments(request.user.profile.neighborhood)
        profile = Profile.get_user_profile(request.user)
        print(updates)
        print(comments)
    except:
        updates = None
        comments = None
        profile = None

    context = {
        'profile':profile ,
        'update_form' : update_form ,
        'updates' : updates ,
        'comments' : comments ,
        'comment_form' : comment_form
        }
    return render(request , 'index.html' , context )


def profile (request, user_username = None ):
    '''
    Function view to a user profile 
    '''
    profile = get_object_or_404(Profile, user__username=user_username)
    neighbors = Profile.objects.filter(neighborhood = profile.neighborhood)
    print(profile.profile_picture)
    print(neighbors)

    data = {
        'profile': profile,
        'neighbors' : neighbors
    }
    return render(request, 'profile.html', data)

def editprofile(request ,username=None ):
    '''
    View function to editing user profile !
    '''
    if request.method == 'POST' and request.user.is_active:
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_info = user_form.save(commit=False)
            profile_info = profile_form.save(commit=False)
            user_info.save()
            profile_info.save()
            message = f"{request.user.username}'s profile updated successfully !"

            return redirect('userprofile',request.user)

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        message = ''

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'message': message
    }

    return render(request, 'editprofile.html', context)

def post_update(request):
    '''
    A function view to save new posts to neighborhood 
    '''
    if request.method == 'POST':
        hood_update_form = UpdateForm(request.POST, request.FILES)
        if hood_update_form.is_valid():
            new_update = hood_update_form.save(commit=False)
            new_update.user = request.user
           
            print(new_update)

            new_update.save()
            return redirect(index)

def comment(request, update_id):
    '''
    Commenting to an update !
    '''
    update = get_object_or_404(Update, pk=update_id)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.update = update
            comment.save()
            return redirect('index')

def search(request):
    '''
    controller function to searching hoods in our app !
    '''

    if 'hood_search' in request.GET and request.GET['hood_search']:
        searched = request.GET['hood_search']
        # hoods = Neighborhood.search_hood(searched)
        hoods = Neighborhood.objects.filter(name__icontains=searched)
        print(hoods)
        message = f'{ searched }'
    else:
        message = 'Objects not found'
        hoods= Neighborhood.objects.all() 

    context = {
        'hoods': hoods,
        'message': message,
    }

    return render(request, "search.html", context)

def hood_details(request , hood_name = None):
    '''
    We want to be able to view more details once we search a hood !
    '''
    hood = Neighborhood.find_neighborhood(hood_name)
    neighbors = Profile.objects.filter(neighborhood=hood)
    business = Business.get_hood_business(hood)
    business_form = BusinessForm()
    context = {
        'hood' : hood ,
        'business_form': business_form ,
        'neighbors' : neighbors ,
        'business' : business ,
    }
    return render (request,'neighbour.html',context)

def business ( request):
    if request.method == 'POST':
        form = BusinessForm(request.POST)
        if form.is_valid():
            business = form.save(commit=False)
            business.user = current_user
            business.neighborhood = neighborhood
            business.save()
            return redirect('businesses')
    else:
        form = BusinessForm()

    try:
        businesses = Business.objects.filter(neighborhood = neighborhood)
    except:
        businesses = None

    return render(request,'businesses.html',{"businesses":businesses,"form":form})

@login_required(login_url='/accounts/login/')
def newbusiness(request):
 neighbour = request.user.id
 profile = Profile.objects.get(user=neighbour)

 if request.method == 'POST':
   form = NewBusinessForm(request.POST)
   if form.is_valid():
     business = form.save(commit=False)
     business.neighborhood = profile.neighborhood
     business.save()
   return redirect('business')

 else:
   form = NewBusinessForm()

 return render(request, 'newbusiness.html',{'form':form,'profile':profile})

def create_hood(request):
    '''
    Handling creation of a new hood !
    '''
    if request.method == 'POST':
        hood_form = HoodForm(request.POST)
        if hood_form.is_valid():
            new_hood = hood_form.save(commit=False)
            new_hood.admin = request.user
            # new_hood.join_hood(request.user)
            new_hood.save()
            return redirect('hood_details',new_hood.name)
    else:
        hood_form = HoodForm()

    context = {
        'hood_form' : hood_form
    }
    return render(request , 'create_hood.html',context)
