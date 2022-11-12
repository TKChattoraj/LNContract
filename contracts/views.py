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

from django.http import StreamingHttpResponse
from django.template import Context, Template

from google.protobuf.json_format import MessageToDict

from contracts.nodes.connect_ln_node import connect_ln_node, LNConnection, connect_cp_ln_node, channel_open, ln_node_info, lnc




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
    node_data=ln_node_info(lnc) # tuple:  (balance, info, (connected, pub_key, address))
    context={'contract': contract_data, 'node': node_data}
    # if party's LN Node is connected to counterparty's node:
    #  then display view included the counterparty node info
    # else:  display view that includes button to connect to counterparty node
    if node_data[2][0]:
        return render(request, 'contracts/contract_connected.html', context)
    else:
        return render(request, 'contracts/contract_not_connected.html', context) 


# def connect(request, pk):
#     print(f'Connection to Party {pk} LN Node.')
#     contract=Contract.contract_context_data(request.session['contract']) 
#     connect=connect_ln_node(pk) #pk is the party primary, key tuple: (balance, info) 
#     context={'contract':contract, 'connect':connect}
#     return render(request, 'contracts/ln_node_connect.html', context)

# def webpack(request):
#     return render(request, 'contracts/hello_webpack.html' )

def connect_cp(request, pk):
    contract_data=Contract.contract_context_data(request.session['contract'])  

    connect_cp=connect_cp_ln_node(pk, lnc) #directing the Party ln node to connect with the counterparty ln node.  returns a None if connected
    print(f"connect_cp: {connect_cp}")
    if  not connect_cp:
        node_data=ln_node_info(lnc) # tuple:  (balance, info, (connected, address))
    else:
        pass
    
    context={'contract': contract_data, 'node': node_data}

    return render(request, 'contracts/contract_connected.html', context)

def open_channel(request, pk):
    contract_data=Contract.contract_context_data(request.session['contract']) 
    node_data=ln_node_info(lnc)
    #channel_response=channel_open(lnc, pk)  #this gets the generator function
    print("*****************printing generator function result")
    
    response_stream=StreamingHttpResponse(generate_t(request, contract_data, node_data, pk))
    return response_stream

    #################
    # for response in channel_response:  # in this line you seem to actually be running the generator function producing a "stream" of responses determined by each yeild encountered in the generator function--which in this case are a dictionary of the openstatus response--it seems like it is "running until a yield is encountered then return that yeild to the 'response' variable."
    #     print("in the generator call for")
    #     print(type(response))  #response is what is returned by the yeild
    #     print(response)
    #     context={'contract': contract_data, 'node': node_data, 'channel': response}
        
    #     if 'chanPending' in response.keys():
    #         print("we are pending!")
    #         print(context['channel']['chanPending']['txid'])
    #     if 'chanOpen' in response.keys():
    #         print("we are open")
    #         break
            
    #         # return render(request, 'contracts/channel_open.html', context)
    #################


def generate_t(request, contract_data, node_data, pk):
    channel_response=channel_open(lnc, pk)  #this gets the generator function
    print("*****************in generate_t")
    print(channel_response)
    
    for response in channel_response:  # in this line you seem to actually be running the generator function producing a "stream" of responses determined by each yeild encountered in the generator function--which in this case are a dictionary of the openstatus response--it seems like it is "running until a yield is encountered then return that yeild to the 'response' variable."
        print("in the generator call for")
        print(type(response))  #response is what is returned by the yeild
        print(response)

        if 'chanOpen' in response.keys():
            print("we are open")
            context={'contract': contract_data, 'node': node_data, 'channel': response}
            print(context['channel']['chanOpen']['channelPoint']['fundingTxidBytes'])
            t=Template('contracs/channel_open.html')
            yield (t.render(context))

        
        if 'chanPending' in response.keys():
            print("we are pending!")
            context={'contract': contract_data, 'node': node_data, 'channel': response}
            print(context['channel']['chanPending']['txid'])
            t=Template('contracts/channel_pending.html')
            yield (t.render(context))
            
        
            
            # return render(request, 'con



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
