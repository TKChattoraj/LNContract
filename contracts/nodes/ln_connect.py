import lightning_pb2 as ln
import lightning_pb2_grpc as lnrpc

#import kcomm_pb2_grpc
#import kcomm_pb2

import grpc
import os
import subprocess
import codecs

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

        self.get_node_info()
    

    # Metadata callback
    def metadata_callback(self, context, callback):
        # for more info see grpc docs
        callback([('macaroon', self.macaroon)], None)

    # Get Info of node.
    def get_node_info(self):     
        request = ln.GetInfoRequest()
        response = self.stub.GetInfo(request)
        return response


    # Get Wallet info
    def get_wallet_info(self):
        request = ln.WalletBalanceRequest()
        response = self.stub.WalletBalance(request)
        return response
        

    # Open Channel to Bob
    def open_channel(self, node_pubkey, amount):
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

        


##########################################################################


# # Due to updated ECDSA generated tls.cert we need to let gprc know that
# # we need to use that cipher suite otherwise there will be a handhsake
# # error when we communicate with the lnd rpc server.
# os.environ["GRPC_SSL_CIPHER_SUITES"] = 'HIGH+ECDSA'


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


# # Retrieve and display the wallet balance.
response = stub.WalletBalance(ln.WalletBalanceRequest())
print(response.total_balance)


# # # Get Info of node.
request = ln.GetInfoRequest()
response = stub.GetInfo(request)
print(response)

# ##################

# # # # List Peers
# # # request = ln.ListPeersRequest(
# # #     latest_error=True
# # # )
# # # response = stub.ListPeers(request)
# # # print(response)



# # # # List Permissions.
# # # request = ln.ListPermissionsRequest()
# # # response = stub.ListPermissions(request)
# # # print(response)

# # # Fee Report
# # # request = ln.FeeReportRequest()
# # # response = stub.FeeReport(request)
# # # print(response)


# # # Prepare Bake Macaroon request
# # permissions = [{"entity":"info", "action":"read"}, {"entity":"offchain", "action":"read"}]
# # key = 0xffffffffffffffff
# # #key = 1
# # external_permissions = False
# # request = ln.BakeMacaroonRequest(
# #     permissions=permissions,
# #     root_key_id=key,
# #     allow_external_permissions=external_permissions
# # )
# # # The response from the request is a strng hex macaroon
# # response= stub.BakeMacaroon(request)
# # print(response)


# # # request = ln.ListMacaroonIDsRequest()
# # # response = stub.ListMacaroonIDs(request)
# # # print(response)



# # # Connect with the counterparty kcomm server
# # ############ 
# # # Assuming for now that the counterparty's server is started.
# # # We'll need to take care of error handling if server isn't on lone.
# # ############

# # def transfer_macaroon(stub, mac_hex_str):
# #     mac_request = kcomm_pb2.Inbound_Mac(MacStr=mac_hex_str)
# #     result = stub.Transfer_Macaroon(mac_request)
# #     print(result.MacResp)


# # port = input("Enter port number of counterparty:  (50051)")
# # with grpc.insecure_channel('localhost:'+port) as channel:
# #     stubk = kcomm_pb2_grpc.KCommStub(channel)
# #     transfer_macaroon(stubk, response.macaroon)

# # # Open Channel to Bob

# # # Will want Bob to send his node_pubkye to Alice
# # # Assume for now that Alice knows Bob's pubkey
# # #  "02647163e26eeedac4b9cba10d821ab06583f95d3fea1be411d2718ddf94578012"

# # node_pubkey= "02647163e26eeedac4b9cba10d821ab06583f95d3fea1be411d2718ddf94578012"
# # node_pubkey = "02fae819273fd07726778f92bbe8f7f4f89d8e5b46b4f51129f94b88ff7ebf798e"
# # node_pubkey_bytes= bytes.fromhex(node_pubkey)

# # request=ln.OpenChannelRequest(
# #     node_pubkey = node_pubkey_bytes,
# #     local_funding_amount = 20001
# # )
# # response=stub.OpenChannel(request)


# # Alice's Channels
# # List Channels Request
# request=ln.ListChannelsRequest()
# response=stub.ListChannels(request)
# print("Channels")
# channel_point = response.channels[0].channel_point
# print(channel_point)
# print("channel point type:")
# print(type(channel_point))


# # # # Close channel with Bob
# # # # Assuming Allice has only one channel, which 
# # # # is with Bob.

# # # txid=channel_point.split(":", 2)[0]
# # # index=channel_point.split(":",2)[1]
# # # print(txid)
# # # print(index)

# # # c_p = ln.ChannelPoint(
# # #     funding_txid_str=txid,
# # #     output_index=int(index)
# # # )


# # # # Close channel with Bob
# # # request=ln.CloseChannelRequest(
# # #     channel_point = c_p
# # # )
# # # response=stub.CloseChannel(request)


print("Finished.")