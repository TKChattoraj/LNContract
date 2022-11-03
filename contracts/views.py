import sys

from django.shortcuts import render
from django.template import Context

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

from contracts.nodes.connect_ln_node import connect_ln_node, LNConnection, connect_cp_ln_node

def index(request):
    request.session['context']={}
    request.session['context']['index']='data'
    # c = Context({'f':'b'})
    # request.session['c'] = serializers.serialize('json', c)
    return render(request, 'contracts/index.html')

def contracts(request):
    print("!!!!!!!!!!!!!!")
    print(request.session.items())
    contracts=Contract.contracts_context_data()  # list of tuples (contract, entity, entity)
    request.session['context']['contracts']=contracts  
    
    print("@@@@@@@@@@@@@@@@@@@@")
    print(request.session.items())
    context=request.session['context']
    
    return render(request, 'contracts/contracts.html', context)

def contract(request, pk):
    print("%%%%%%%%%%%%%%%%%%%")
    print(request.session.items())
    contract_data=Contract.contract_context_data(pk) # tuple of (contract, party, counterparty, obligations_sorted)
    request.session['context']['contract']=contract_data
    context=request.session['context']
    print("****************************")
    print(context)
    
    return render(request, 'contracts/contract_initial.html', context)

def connect(request, pk):
    print(f'Connection to Party {pk} LN Node.')
    #ln_connection=LNConnection()
    contract=Contract.contract_context(pk)
    connect=connect_ln_node(pk)
    context={'contract':contract, 'connect':connect}
    return render(request, 'contracts/ln_node_connect.html', {'context':context})

def connect_cp(request, pk):
    print(f'Connecting to Counterparty {pk} LN Node')
    connect_cp=connect_cp_ln_node(pk)
    context={'connect_cp':connect_cp}
    print("Connected to counterparty")
    print(context['connect_cp'])
    return render(request, 'contracts/ln_node_connect_cp.html', {'context':context})