from django.shortcuts import redirect

def home(request):
    for g in request.user.groups.all():
        print(g)
        if g.name == "mediadex":
            return redirect(to="/mediadex")
    return redirect(to="/admin")