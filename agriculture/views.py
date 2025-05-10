from django.shortcuts import render

from django.contrib.auth.decorators import login_required
@login_required

def farming(request):
    return render(request, 'farming.html')
def crop(request):
    return render(request,'crop.html')