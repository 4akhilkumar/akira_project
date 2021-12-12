from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group == 'Student':
                if (request.GET.get('next')):
                    return redirect(request.GET.get('next'))
                else:
                    return redirect('student_dashboard')
            elif group == 'Assistant Professor':
                if (request.GET.get('next')):
                    return redirect(request.GET.get('next'))
                else: 
                    return redirect('staff_dashboard')
            elif group == 'Associate Professor':
                if (request.GET.get('next')):
                    return redirect(request.GET.get('next'))
                else: 
                    return redirect('staff_dashboard')
            elif group == 'Professor':
                if (request.GET.get('next')):
                    return redirect(request.GET.get('next'))
                else: 
                    return redirect('staff_dashboard')
            elif group == 'Head of the Department':
                if (request.GET.get('next')):
                    return redirect(request.GET.get('next'))
                else: 
                    return redirect('hod_dashboard')
            elif group == 'Course Co-Ordinator':
                if (request.GET.get('next')):
                    return redirect(request.GET.get('next'))
                else: 
                    return redirect('cc_dashboard')
            elif group == 'Administrator':
                if (request.GET.get('next')):
                    return redirect(request.GET.get('next'))
                else:
                    return redirect('super_admin_dashboard')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                # print('Working:', allowed_roles)
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("Looks Like You Have Lost Your Way...!")
        return wrapper_func
    return decorator