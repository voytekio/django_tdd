import pdb
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

#home_page = None
def home_page(request):
    #pdb.set_trace()
    #if request.method == 'POST':
    #    return render(request, 'home.html', {'new_item_text':request.POST['item_text']})
        #return HttpResponse(request.POST['item_text'])
    return render(request, 'home.html', {'new_item_text':request.POST.get('item_text', '')})
    #return render(request, 'home.html')
    #return HttpResponse('<html><title>To-Do lists</title></html>')
