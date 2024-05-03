import hashlib
import json
from time import time
from urllib.parse import urlparse

class Block:
    def __init__(self, index, transactions, proof, previous_hash, block_type="transaction", model_state=None):
        self.index = index
        self.timestamp = time()
        self.transactions = transactions
        self.proof = proof
        self.previous_hash = previous_hash
        self.block_type = block_type
        self.model_state = model_state  # Only for version blocks, to store the state of the model

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.nodes = set()
        self.create_block(proof=100, previous_hash='1', block_type="genesis")  # Genesis block

    def register_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def create_block(self, proof, previous_hash, block_type="transaction", model_state=None):
        block = Block(index=len(self.chain) + 1,
                      transactions=self.current_transactions,
                      proof=proof,
                      previous_hash=previous_hash,
                      block_type=block_type,
                      model_state=model_state)
        self.current_transactions = []
        self.chain.append(block)
        return block

    def add_transaction(self, sender, receiver, amount):
        transaction = {
            'sender': sender,
            'receiver': receiver,
            'amount': amount
        }
        self.current_transactions.append(transaction)
        return self.last_block.index + 1

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_stake(self, validators):
        # This is a simplified version of PoS where we randomly select a validator based on their stake
        total_stakes = sum(validator['stake'] for validator in validators)
        winning_validator = random.choices(validators, weights=[v['stake'] for v in validators], k=1)[0]
        return winning_validator['node']

    def proof_of_work(self, last_proof):
        proof = 0
        while not self.valid_proof(last_proof, proof):
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    @staticmethod
    def hash(block):
        block_string = json.dumps(block.__dict__, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def resolve_conflicts(self):
        longest_chain = None
        max_length = len(self.chain)

        for node in self.nodes:
            response = requests.get(f'http://{node}/chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    longest_chain = chain

        if longest_chain:
            self.chain = longest_chain
            return True
        return False

    def valid_chain(self, chain):
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            if block['previous_hash'] != self.hash(last_block):
                return False
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False
            last_block = block
            current_index += 1

        return True

