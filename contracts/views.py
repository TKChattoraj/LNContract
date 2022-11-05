import sys

from django.shortcuts import render
from django.template import Context
from django.core import serializers
from contracts.andytest import b

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

from contracts.nodes.connect_ln_node import connect_ln_node, LNConnection, connect_cp_ln_node, channel_open, lnc




def index(request):
    print("&&&&&&&&&&&&&&&&&&&&&&7")
    print(b.a)
    b.change(2)
    request.session['context']={}
    return render(request, 'contracts/index.html')

def contracts(request):
    print("******************")
    print(b.a)
    contracts=Contract.contracts_context_data()  # list of tuples (contract, entity, entity)  
    context={'contracts': contracts} 
    return render(request, 'contracts/contracts.html', context)

def contract(request, pk):
    contract_data=Contract.contract_context_data(pk) # tuple of (contract, party, counterparty, obligations_sorted)
    request.session['contract']=contract_data[0].pk
    request.session['party']=contract_data[1].pk
    request.session['counterparty']=contract_data[2].pk
    context={'contract': contract_data}
    return render(request, 'contracts/contract_initial.html', context)

def connect(request, pk):
    print(f'Connection to Party {pk} LN Node.')
    contract=Contract.contract_context_data(pk)
    connect=connect_ln_node(pk) # tuple: (balance, info)
    context={'contract':contract, 'connect':connect}
    return render(request, 'contracts/ln_node_connect.html', context)

def connect_cp(request, pk):
    print(f'Connecting to Counterparty {pk} LN Node')
    contract=Contract.contract_context_data(request.session['contract'])  
    connect=connect_ln_node(request.session['party']) # tuple: (balance, info)
    connect_cp=connect_cp_ln_node(pk, lnc) #directing the Party ln node to connect with the counterparty ln node
    context={'contract':contract, 'connect':connect,'connect_cp':connect_cp}
    print("Connected to counterparty")
    print(context['connect_cp'])
    return render(request, 'contracts/ln_node_connect_cp.html', context)

def open_channel(request, pk):
    channel=channel_open(lnc, pk)
    context={'channel': channel}
    return render(request, 'contracts/open_channel.html', context)

def serialize_list(l):
    print("in serialize")
    ll=[]
    for t in l:  #iterate over a list of tuples
        #tuple to hold the serialzied dicts
        print("in list iteration")
        print(t)
        new_tuple_list=[]
        list_from_tuple=list(t)
        for i, item in enumerate(list_from_tuple):

            print("in tuple iteration")
            
            li_s=serializers.serialize('json', [item]) #list holding one dict which is serialized item 
            print(li_s)
            print(type(li_s))
            print(li_s[0])
            new_tuple_list.append(li_s[0])
            print("new tuple list")
            print(new_tuple_list)
        s_tuple=tuple(new_tuple_list)
        ll.append(s_tuple)
    print(ll)
    return ll
