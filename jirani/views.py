from django.shortcuts import render , redirect , get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Neighborhood , Profile , Business , PolicePost , Hospital , Update , Comment
from .forms import UpdateForm , UserUpdateForm , ProfileUpdateForm , CommentForm , PoliceAddForm , BusinessForm , HospitalForm , HoodForm

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
            new_update.neighbour = request.user.neighbour
            print(new_update)

            new_update.save()
            return redirect(index)
            

def delete_update(request , update_id):
    '''
    Author of the update can delete an update
    '''
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

    hospital = Hospital.fetch_hood_hospitals(hood)
    business = Business.get_hood_business(hood)
    police = PolicePost.get_hood_police(hood)

    police_form = PoliceAddForm()
    business_form = BusinessForm()
    hospital_form = HospitalForm()

    context = {
        'hood' : hood ,
        'police_form': police_form ,
        'business_form': business_form ,
        'hospital_form': hospital_form ,
        'neighbors' : neighbors ,
        'hospital' : hospital ,
        'business' : business ,
        'police' : police

    }
    return render (request,'neighbour.html',context)

  

def add_business ( request):
    '''
    view function to which a new business shall be created
    '''
    if request.method == 'POST':
        business_form = BusinessForm(request.POST)
        if business_form.is_valid():
            business = business_form.save(commit=False)
            business.neighborhood = request.user.profile.neighborhood
            business.save()
            return redirect('hood_details', business.neighborhood)



def delete_business(request):
    '''
    view function to which an existing business shall be deleted
    '''
    return redirect('index')



def add_police_post(request):
    '''
    view function to which a new police post shall be created
    '''
    if request.method == 'POST':
        police_form = PoliceAddForm(request.POST)
        if police_form.is_valid():
            station = police_form.save(commit=False)
            station.hood = request.user.profile.neighborhood
            station.save()
            return redirect('hood_details',station.hood)


def delete_police_post(request , pk ):
    '''
    view function to which an existing police post shall be deleted
    '''
    police_post = PolicePost.get_police_post(pk)
    police_post.remove_post()

    return redirect('hood_details')


def add_hood_hospital(request):
    '''
    view function to which a new police post shall be created
    '''
    if request.method == 'POST':
        hospital_form = HospitalForm(request.POST)
        if hospital_form.is_valid():
            hospital = hospital_form.save(commit=False)
            hospital.neighborhood = request.user.profile.neighborhood
            hospital.save()
            return redirect('hood_details',hospital.neighborhood)


def delete_hood_hospital(request, pk):
    '''
    view function to which an existing police post shall be deleted
    '''
    police_post = PolicePost.get_police_post(pk)
    police_post.remove_post()

    return redirect('index')

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




def delete_hood(request , hood_id):
    '''
    The view function for the admin to delete a hood !
    '''
    hood = get_object_or_404(Neighborhood, pk=hood_id)
    hood.remove_hood()
    return redirect('index')


def leave_hood (request , user):
    '''
    When a user wishes to chuck from any group !
    '''
    hood_name = Neighborhood.get_hood_by_name(request.user.profile.neighborhood)
    hood_name.leave_hood(request.user)
    request.user.neighborhood = None
    return redirect('hood_details', hood_name)