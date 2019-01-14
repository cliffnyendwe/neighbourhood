from django.db import models
from django.contrib.auth.models import User 
from django.dispatch import receiver
from django.db.models.signals import post_save

class Neighborhood (models.Model):
    '''
    We want to narrow down to Neighborhoods so Users can recieve relevant information
    '''
    name = models.CharField(max_length=30)
    city = models.CharField(max_length = 50 , blank=True )
    admin = models.ForeignKey(User , on_delete=models.CASCADE, related_name='hood_admin' , null=True , blank= True)
    occupants = models.ManyToManyField(User , related_name='hood_occupants', blank=True)


    def __str__(self):
        return self.name

    def new_hood ( self ):
        '''
        Saving a new Hood 
        '''
        self.add()

    def is_neighbor(self, neighbor):
        return neighbor in self.occupants.all()

    def get_number_of_neighbors(self):
        if self.occupants.count():
            return self.occupants.count()
        else:
            return 0

    @classmethod 
    def get_all_occupants (cls):
        '''
        Returns
        '''
        return cls.objects.all()
    
    @classmethod  
    def find_neighborhood (cls , hood_name):
        '''
        method for returning a specific neighborhood 
        '''
        return cls.objects.get( name = hood_name )

    @classmethod 
    def search_hood (cls , search_term):
        '''
        Search for a hood from database
        '''
        return cls.objects.filter(name__icontains=search_term)

    @classmethod 
    def update_hood_name ( cls ,id , new_name ):
        return cls.objects.get(id).update( name = new_name )

    @classmethod 
    def get_hood_by_name(cls , name) :
        return cls.objects.get(name=name)

class Profile(models.Model):
    '''
    Profile of an individul . More Information .
    '''
    user = models.OneToOneField(User,  on_delete=models.CASCADE)
    neighborhood = models.ForeignKey(Neighborhood , null=True , blank=True ,related_name='population')
    profile_picture = models.ImageField(upload_to='static/profile', default="pic.png" , blank=True)
    about = models.TextField(max_length=150, blank=True)

    def __str__(self):
        return self.user.username

    @classmethod
    def get_user_profile(cls, user):
        return cls.objects.get(user=user)

    @classmethod
    def get_all_profiles(cls):
        return cls.objects.all()

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

class Business (models.Model):
    '''
    Bunisesses in a particular neighborhood
    '''
    name = models.CharField(max_length = 30)
    neighborhood = models.ForeignKey(Neighborhood, on_delete=models.CASCADE)
    email = models.EmailField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Businesses'

    def create_business ( self ):
        self.save()

    def remove_business ( self ):
        self.delete()

    @classmethod 
    def get_hood_business ( cls , hood ):
        return cls.objects.filter(neighborhood__name = hood)

    @classmethod 
    def get_bussiness ( cls , hood ):
        business = Business.objects.filter(name__username__icontains=hood)
        return business    
    
    @classmethod
    def update_business ( id , new_name):
        return cls.objects.get(id).update(name = new_name)


class Update ( models.Model ):
    '''
    Could be Images , Videos or Plain words 
    '''
    user = models.ForeignKey(User , on_delete=models.CASCADE )
    hood = models.ForeignKey(Neighborhood ,null=True , blank=True )
    post = models.TextField(max_length=280 )
    picture = models.ImageField( upload_to = 'static/posts/' , null=True )
    post_date = models.DateField(auto_now=True)

    def __str__(self):
        return f"{ self.user.username }'s post"

    @classmethod 
    def get_hood_updates(cls , hood):
        return cls.objects.filter(hood = hood)


class Comment ( models.Model ):
    comment = models.CharField(max_length = 280)

    update = models.ForeignKey(Update , on_delete=models.CASCADE)
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    comment_date = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.user.username }'s comment on update by {self.update.user.username}"

    @classmethod 
    def get_hood_comments(cls , hood):
        return cls.objects.filter(update__hood=hood)