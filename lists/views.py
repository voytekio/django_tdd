import pdb
from django.shortcuts import render, redirect
from django.http import HttpResponse

from lists.models import Item, List

# Create your views here.

#home_page = None
def home_page(request):
    return render(request, 'home.html')

def view_list(request):
    return render(request, 'list.html', {'items':Item.objects.all()})

def new_list(request):
    print('POST Request included: {}'.format(request.POST['item_text']))
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/the-only-list-in-the-world/')
