import pdb
from django.shortcuts import render, redirect
from django.http import HttpResponse

from lists.models import Item

# Create your views here.

#home_page = None
def home_page(request):
    #pdb.set_trace()
    #return HttpResponse(request.POST['item_text'])
    if request.method == 'POST':
        print('POST Request included: {}'.format(request.POST['item_text']))
        Item.objects.create(text=request.POST['item_text'])
        #item_orm = Item()
        #item_orm.text = request_post.get('item_text', '')
        #item_orm.save()
        return redirect('/')
    return render(request, 'home.html', {'items':Item.objects.all()})
    #return HttpResponse('<html><title>To-Do lists</title></html>')
