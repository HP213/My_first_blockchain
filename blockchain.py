#Created on Mon Jul 23 05:51:30 2018
#modul1 - Create a blockchain

import datetime
import hashlib
import json
from flask import Flask, jsonify

#part-1 Creating a blockchain

#definig a class(Because is is much better than creating a function)
class Blockchain:
    #creating a function to initialise blockchain
    def __init__(self):
        self.chain = []
        self.create_block(proof = 1, previous_hash = '0')
        
    #creating a block
    def create_block(self, proof, previous_hash):
        #definig a dictionary to create a block everytime 
        block = {'index' : len(self.chain) + 1,
                 'timestamp' : str(datetime.datetime.now()),
                 'proof' : proof,
                 'previous_hash' : previous_hash}
        self.chain.append(block)
        return block
    
    #getting the last created block
    def get_prev_block(self):
        return self.chain[-1]
    
    #defining algorithm to solve the problem and also return proof
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof : True
            else:
                check_proof : False
                new_proof += 1
        return new_proof
    
    #Making a hash of given block
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    #validating is whole chain is valid or not
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True
    
    #Part -2 Mining our Blockchain
    
 #creating a web app
app = Flask(__name__)
 
 #creatinga blockchain 
blockchain = Blockchain()
 
 #Mining a new block
 
@app.route('/mine_block', methods = ['GET'])
def mine_block():
     previous_block = blockchain.get_prev_block()
     previous_proof = previous_block['proof']
     proof = blockchain.proof_of_work(previous_proof)
     previous_hash = blockchain.hash(previous_block)
     block = blockchain.create_block(proof, previous_hash)
     response = {'message' : 'Congratulations, You Just mined a block',
                 'index' : block['index'],
                 'timestamp' : block['timestamp'],
                 'proof' : block['proof'],
                 'previous_hash' : block['previous_hash']}
     return jsonify(response), 200
     
#Getting the full blockchain
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain' : blockchain.chain,
                'Length' : len(blockchain.chain)}
    return jsonify(response), 200

#running the app
app.run(host = '0.0.0.0', port = 5000)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    