from django.shortcuts import render

# Create your views here.
def show_main(request):
    context = {
        'nama aplikasi' : 'Strike Shop',
        'name': 'Angga Tri Setiawan',
        'class': 'PBP F'
    }

    return render(request, "main.html", context)
