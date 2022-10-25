from django.shortcuts import render
from contracts.models import (
    LN_Node,
    Contract,
    Entity,
    Good,
    Service,
    MonetaryObligation,
    SaleOfGood,
    SaleOfService,
    ContractText
)

def index(request):
    return render(request, 'contracts/index.html')

def contracts(request):
    context=Contract.contracts_context()
    return render(request, 'contracts/contracts.html', context)

def contract(request):
    return render(request, 'contracts/contract.html')

def connect(request):
    print("LN Node Connected!")
    return render(request, 'contracts/index.html')