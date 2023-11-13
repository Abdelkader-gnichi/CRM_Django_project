from django.shortcuts import redirect


def is_logged(func):

    def wrapper(request,*args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return func(request, *args, **kwargs)
        
    return wrapper

def allowed_users(user_group=[]):

    def decorator(func):
        def wrapper(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
   
            print(group)
            if group in user_group or request.user.is_staff :
                    return func(request, *args, **kwargs)
            elif group == 'customer':
                   return redirect('user_profile')
            
                
        return wrapper
    return decorator

def for_admins(func):
    def wrapper(request, *args, **kwargs):

        group = None
        if request.user.groups.exists():
             group = request.user.groups.all()[0].name
        
        if group is not None or request.user.is_staff:
            
            if group == 'admin' or request.user.is_staff:
                return func(request, *args, **kwargs)
            if group == 'customer':
                return redirect('user_profile')
    return wrapper