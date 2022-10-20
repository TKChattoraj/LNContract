from django.shortcuts import render


def contract(request):
    return render(request, 'contracts/index.html')
