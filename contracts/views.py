from django.shortcuts import render


def index(request):
    return render(request, 'contracts/index.html')

def contracts(request):
    return render(request, 'contracts/contracts.html')

def contract(request):
    return render(request, 'contracts/contract.html')

def connect(request):
    print("LN Node Connected!")
    return render(request, 'contracts/index.html')