from django.shortcuts import render


def contract(request):
    return render(request, 'contracts/index.html')

def connect(request):
    print("LN Node Connected!")
    return render(request, 'contracts/index.html')