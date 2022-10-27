import sys

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

from contracts.nodes.connect_ln_node import connect_ln_node, LNConnection

def index(request):
    return render(request, 'contracts/index.html')

def contracts(request):
    context=Contract.contracts_context()
    return render(request, 'contracts/contracts.html', context)

def contract(request, pk):
    context=Contract.contract_context(pk)
    return render(request, 'contracts/contract.html', {'contract': context})

def connect(request, pk):
    print(f'LN Node Connected! Party: {pk}')
    ln_connection=LNConnection()
    response=connect_ln_node(pk)
    return render(request, 'contracts/ln_node_connect.html', {'connect': response})