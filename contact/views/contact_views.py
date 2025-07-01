from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q
from contact.models import Contact
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='contact:login')
def index(request):
    contacts = Contact.objects \
        .filter(show=True) \
        .order_by('-id')
    
    paginator = Paginator(contacts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'site_title': 'Contatos - ',
    }

    return render(
        request,
        'contact/index.html',
        context
    )

def search(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = []
        search_value = request.GET.get('q', '').strip()
        contacts = Contact.objects \
        .filter(show=True)\
        .filter(
            Q(first_name__icontains=search_value) |
            Q(last_name__icontains=search_value)|
            Q(phone__icontains=search_value)|
            Q(email__icontains=search_value)
            )\
        .order_by('-id')
        
        paginator = Paginator(contacts, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        
        for contact in page_obj:
            data.append({
                'first_name':contact.first_name,
                'last_name':contact.last_name,
                'phone':contact.phone,
                'email':contact.email 
            })
        return JsonResponse({'results': data})
    else:
        search_value = request.GET.get('q', '').strip()

        if search_value == '':
            return redirect('contact:index')

        contacts = Contact.objects \
            .filter(show=True) \
            .filter(
                Q(first_name__icontains=search_value) |
                Q(last_name__icontains=search_value) |
                Q(phone__icontains=search_value) |
                Q(email__icontains=search_value)
            ) \
            .order_by('-id')

        paginator = Paginator(contacts, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context = {
            'page_obj': page_obj,
            'site_title': 'Search - ',
        }

        return render(request, 'contact/index.html', context)
def contact(request, contact_id):
    #single_contact = Contact.objects.filter(pk=contact_id).first()
    single_contact = get_object_or_404(
        Contact,
        pk=contact_id,
        show=True
        )
    site_title = f'{single_contact.first_name} {single_contact.last_name} - '
    context = {
        'contact': single_contact,
        'site_title': site_title,
    }
    return render(
        request,
        'contact/contact.html',
        context
    )