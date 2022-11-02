from flask import Flask, request
from flask_socketio import SocketIO, emit,send
from flask import jsonify
from flask_cors import CORS, cross_origin
from algosdk.v2client.indexer import IndexerClient
import json
import math

algod_address = "https://mainnet-api.algonode.cloud"
indexer_address = "https://mainnet-idx.algonode.cloud"




def paginate( array, page=0, page_size=5):
    l=page*page_size
    return array[l:l+page_size]


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

CORS(app)
@app.route('/')
def hello():
    return 'Hello, World!'    

algod_token = ""
subscribed = []




@socketio.on('subscribe')
def subscribe(wallet_address):
    # subscribed.push({'wallet_address':wallet_address})
    # send({'wallet_address':wallet_address})
    print(wallet_address)

@socketio.on('/unsubscribe')
def     unsubscribe(wallet_address):
    subscribed = list(filter(lambda x: x['wallet_address'] == wallet_address, subscribed))
    send('UnSubscribed',namespace='/unsubscription')
    

@socketio.on('connect')
def test_connect():
    print('someone connected to websocket')
    emit('responseMessage', {'data': 'Connected! ayy'})
    # need visibility of the global thread object
    

@socketio.on('get-notification')
@app.route('/notif/<wallet_address>')
def endpoint_socket(wallet_address):
    print("---------------------------------------");
    print(wallet_address, "WALLET ADDRESS");
    print("---------------------------------------");

    indexer_client = IndexerClient(
        algod_token, indexer_address, headers={"User-Agent": "algosdk"}
    )

    response = indexer_client.search_transactions_by_address(
        address=wallet_address)

    socketio.emit("get-notification",{"data": response["transactions"]}) 
    return jsonify({'count': len(response["transactions"]),'data':response["transactions"]})




if __name__ == '__main__':
    socketio.run(app, host="127.0.0.1", port=8000, debug=True)
