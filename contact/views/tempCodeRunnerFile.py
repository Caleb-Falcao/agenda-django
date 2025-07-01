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
                'first_name':contact.first_name
            })
        print('funciona')
        return JsonResponse({'results': data})