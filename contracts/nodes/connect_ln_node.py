print("in the connect_ln_node")
import contracts.nodes.lightning_pb2 as ln
import contracts.nodes.lightning_pb2_grpc as lnrpc

#import kcomm_pb2_grpc
#import kcomm_pb2

import grpc
import os
import subprocess
import codecs

from google.protobuf.json_format import MessageToDict

#import kcomm_server as kcomm

# Nd to attriubte bulk of this code to LND site?   

class LNConnection():
    def __init__(self, tls_path, macaroon_path, ln_url_port_str):

        # Due to updated ECDSA generated tls.cert we need to let gprc know that
        # we need to use that cipher suite otherwise there will be a handhsake
        # error when we communicate with the lnd rpc server.
        os.environ["GRPC_SSL_CIPHER_SUITES"] = 'HIGH+ECDSA'

        # build the TLS credentials:# Normally Lnd cert is at ~/.lnd/tls.cert on Linux and
        # ~/Library/Application Support/Lnd/tls.cert on Mac.
        # That is if there is a local LN node.  
        # Here we are using Polar and so the TLS cert is located at
        # /home/tarun/.polar/networks/1/volumes/lnd/alice/tls.cert'
        print("TLS path: {}".format(tls_path))
        self.tls_cert=open(os.path.expanduser(tls_path), 'rb').read()
        self.cert_creds=grpc.ssl_channel_credentials(self.tls_cert)

        # Build the meta data for the macaroon credentials:
        # Normally Lnd admin macaroon is at ~/.lnd/data/chain/bitcoin/simnet/admin.macaroon on Linux and
        # ~/Library/Application Support/Lnd/data/chain/bitcoin/simnet/admin.macaroon on Mac.  
        # That is if there is a local LN node.
        # Here we are using Polar and so the macaroon will be located at: 
        # /home/tarun/.polar/networks/1/volumes/lnd/alice/data/chain/bitcoin/regtest/admin.macaroon

        with open(os.path.expanduser(macaroon_path), 'rb') as f:
            macaroon_bytes = f.read()
            self.macaroon = codecs.encode(macaroon_bytes, 'hex')

        auth_creds = grpc.metadata_call_credentials(self.metadata_callback)

        # Combine the macaroon auth credentials.
        # Every call will be encrypted and authenticated.

        combined_creds = grpc.composite_channel_credentials(self.cert_creds, auth_creds)


        channel = grpc.secure_channel(ln_url_port_str, combined_creds, options=(('grpc.enable_http_proxy', 0),('grpc.enable_https_proxy', 0)))
        
        # stub gives the location and port the ln node controlled by the party (Alice) is listening to
        # and gives the authorization credentials--the macaroon.
        # It is the basis of every communication to the LN node.  
        self.stub = lnrpc.LightningStub(channel)

        #self.get_node_info()
    

    # Metadata callback
    def metadata_callback(self, context, callback):
        # for more info see grpc docs
        callback([('macaroon', self.macaroon)], None)

    # Get Info of node.
    def get_node_info(self):     
        request = ln.GetInfoRequest()
        response = self.stub.GetInfo(request)
        return response

    # # Retrieve and display the wallet balance.
    def wallet_balance(self):  
        balance = self.stub.WalletBalance(ln.WalletBalanceRequest())
        return(balance)

    # Get Wallet info
    def get_wallet_info(self):
        request = ln.WalletBalanceRequest()
        response = self.stub.WalletBalance(request)
        return response

    def list_peers(self):
        request=ln.ListPeersRequest()
        response=self.stub.ListPeers(request)
        return response     

    def connect_peer(self, pubkey, host):
        address=ln.LightningAddress(pubkey=pubkey, host=host)
        request=ln.ConnectPeerRequest(addr=address, timeout=10)
        response=self.stub.ConnectPeer(request)

    # Open Channel to Dave
    def open_channel(self, node_pubkey, amount):  #amount is in satoshis
        # Will want Bob to send his node_pubkye to Alice
        # Assume for now that Alice knows Bob's pubkey
        # node_pubkey= "02647163e26eeedac4b9cba10d821ab06583f95d3fea1be411d2718ddf94578012"
        
        #node_pubkey = "02fae819273fd07726778f92bbe8f7f4f89d8e5b46b4f51129f94b88ff7ebf798e"
        node_pubkey_bytes= bytes.fromhex(node_pubkey)

        request=ln.OpenChannelRequest(
            node_pubkey = node_pubkey_bytes,
            local_funding_amount = amount
        )
        response=self.stub.OpenChannel(request)
        return response

def ln_stub():
    
    ##########################################################################


    # # Due to updated ECDSA generated tls.cert we need to let gprc know that
    # # we need to use that cipher suite otherwise there will be a handhsake
    # # error when we communicate with the lnd rpc server.
    os.environ["GRPC_SSL_CIPHER_SUITES"] = 'HIGH+ECDSA'


    # # Connect to Alice

    # # build the TLS credentials:# Normally Lnd cert is at ~/.lnd/tls.cert on Linux and
    # # ~/Library/Application Support/Lnd/tls.cert on Mac.
    # # That is if there is a local LN node.  
    # # Here we are using Polar and so the TLS cert is located at
    # # /home/tarun/.polar/networks/1/volumes/lnd/alice/tls.cert'

    cert = open(os.path.expanduser('/home/tarun/.polar/networks/1/volumes/lnd/alice/tls.cert'), 'rb').read()
    #cert = open(os.path.expanduser('/home/tarun/.lnd/tls.cert'), 'rb').read()

    cert_creds = grpc.ssl_channel_credentials(cert)

    # # Build the meta data for the macaroon credentials:
    # # Normally Lnd admin macaroon is at ~/.lnd/data/chain/bitcoin/simnet/admin.macaroon on Linux and
    # # ~/Library/Application Support/Lnd/data/chain/bitcoin/simnet/admin.macaroon on Mac.  
    # # That is if there is a local LN node.
    # # Here we are using Polar and so the macaroon will be located at: 
    admin_mac_path='/home/tarun/.polar/networks/1/volumes/lnd/alice/data/chain/bitcoin/regtest/admin.macaroon'
    #admin_mac_path='/home/tarun/.lnd/data/chain/bitcoin/testnet/admin.macaroon'

    with open(os.path.expanduser(admin_mac_path), 'rb') as f:
        macaroon_bytes = f.read()
        macaroon = codecs.encode(macaroon_bytes, 'hex')

    # # Metadata callback
    def metadata_callback(context, callback):
        # for more info see grpc docs
        callback([('macaroon', macaroon)], None)

    auth_creds = grpc.metadata_call_credentials(metadata_callback)


    # # Combine the macaroon auth credentials.
    # # Every call will be encrypted and authenticated.

    combined_creds = grpc.composite_channel_credentials(cert_creds, auth_creds)



    # #127.0.0.1:10004.
    grpc_location='127.0.0.1:10001'
    channel = grpc.secure_channel(grpc_location, combined_creds, options=(('grpc.enable_http_proxy', 0),('grpc.enable_https_proxy', 0)))
    # # stub gives the location and port the ln node controlled by the party (Alice) is listening to
    # # and gives the authorization credentials--the macaroon.
    # # It is the basis of every communication to the LN node.  
    stub = lnrpc.LightningStub(channel)  
    return stub

def wallet_balance(stub):
    # # Retrieve and display the wallet balance.
    balance = stub.WalletBalance(ln.WalletBalanceRequest())
    print(balance.total_balance)
    return(balance)

def wallet_info(stub):
    # # # Get Info of node.
    request = ln.GetInfoRequest()
    info = stub.GetInfo(request)
    print(info)
    return(info)

def connect_ln_node(pk): 
    pass
#     tls_cert='/home/tarun/.polar/networks/1/volumes/lnd/alice/tls.cert'
#     admin_mac_path='/home/tarun/.polar/networks/1/volumes/lnd/alice/data/chain/bitcoin/regtest/admin.macaroon'
#     grpc_location='127.0.0.1:10001'
#     ln_connection=LNConnection(tls_cert, admin_mac_path, grpc_location)
#     balance=ln_connection.wallet_balance()
#     info=ln_connection.get_node_info()
#     # stub=ln_stub()
#     # balance=wallet_balance(stub)
#     # info=wallet_info(stub)
#     print("Connected to my LN Node!")
#     return (balance, info)

def ln_node_info(lnc): #returning the node balance and info
    # tls_cert='/home/tarun/.polar/networks/1/volumes/lnd/alice/tls.cert'
    # admin_mac_path='/home/tarun/.polar/networks/1/volumes/lnd/alice/data/chain/bitcoin/regtest/admin.macaroon'
    # grpc_location='127.0.0.1:10001'
    # ln_connection=LNConnection(tls_cert, admin_mac_path, grpc_location)
    balance=lnc.wallet_balance()
    info=lnc.get_node_info()
    counterparty_pubkey='031c43195c2aa38d186cc8194f30756e88fc2b65fd9adaeed25f0dfe1b6663d383'
    cp_node_connected=connected(lnc, counterparty_pubkey)
    return (balance, info, cp_node_connected)

def connected(lnc, cp_pubkey):    # determines whether the Party's LN Node is connected to its counterpary's LN Node.
    list_response=lnc.list_peers()
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    d=MessageToDict(list_response)  # convert the gRPC response object to a dictionary
    connected=False
    address=None
    pub_key=None
    for peer in d["peers"]:
        if peer['pubKey']==cp_pubkey:
            connected=True
            address=peer['address']
            pub_key=peer['pubKey']
            continue
    print(f'address: {address}')
    print(f'connected: {connected}')
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    return(connected, pub_key, address)



def connect_cp_ln_node(pk, lnc): # pk parameter is the counterparty's entity id.
    
    connect_peer=lnc.connect_peer(pubkey='031c43195c2aa38d186cc8194f30756e88fc2b65fd9adaeed25f0dfe1b6663d383', host='172.20.0.2:9735')
    print("Connect to peer")
    print(connect_peer)
    return connect_peer
    
def channel_open(lnc, pk):#pk is the counterparty pk
    # some logic to get the counterparty node pubkey from the counterparty pk
    pubkey='031c43195c2aa38d186cc8194f30756e88fc2b65fd9adaeed25f0dfe1b6663d383'
    amount=200000  # will need to get this from the obligation amount--so the obligation will need to pass from the template to the view to here.  In Satoshis
    responses=lnc.open_channel(pubkey, amount)
    print("&&&&&&&&&&&&&&&&& Channel Open &&&&&&&&&&&&&&&&&&&&&&")
    print(responses)
    for  response in responses:
        print(response)
        # print("Received message %s at %s" %
        #       (response.message, response.location))
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    return responses



tls_cert='/home/tarun/.polar/networks/1/volumes/lnd/alice/tls.cert'
admin_mac_path='/home/tarun/.polar/networks/1/volumes/lnd/alice/data/chain/bitcoin/regtest/admin.macaroon'
grpc_location='127.0.0.1:10001'
lnc=LNConnection(tls_cert, admin_mac_path, grpc_location)