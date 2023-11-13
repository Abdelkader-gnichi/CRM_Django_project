from django.db.models.signals import post_save,post_delete
from django.contrib.auth.models import User,Group
from .models import Customer


def user_2_customer_creation(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='customer')
        instance.groups.add(group)
        Customer.objects.create(user=instance)

post_save.connect(user_2_customer_creation, sender= User)

def customer_delete_user(sender, instance, **kwargs):
    
        User.objects.filter(username=instance.user.username).delete()

post_delete.connect(customer_delete_user,sender=Customer)




