import hashlib
import json
from time import time
from urllib.parse import urlparse
from blockchain_module import Blockchain  # Import the blockchain code we wrote previously

class LinguaChainCryptocurrency:
    def __init__(self, blockchain):
        self.blockchain = blockchain
        self.nodes = set()  # This will manage the network nodes, similar to the Blockchain class

    def register_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def verify_transaction(self, transaction):
        """ Verify that the transaction is valid """
        sender_balance = self.get_balance(transaction['sender'])
        return sender_balance >= transaction['amount']

    def submit_transaction(self, sender, receiver, amount):
        """ Create a new transaction and add it to the blockchain """
        transaction = {
            'sender': sender,
            'receiver': receiver,
            'amount': amount,
            'timestamp': time()
        }
        if self.verify_transaction(transaction):
            self.blockchain.add_transaction(sender, receiver, amount)
            return True
        else:
            return False

    def get_balance(self, node_address):
        """ Calculate the balance for a node """
        balance = 0
        for block in self.blockchain.chain:
            for trans in block.transactions:
                if trans['sender'] == node_address:
                    balance -= trans['amount']
                if trans['receiver'] == node_address:
                    balance += trans['amount']
        return balance

    def distribute_rewards(self):
        """ Distribute rewards to nodes based on their contributions """
        # For simplicity, let's assume each block mined by a node earns them a reward
        for block in self.blockchain.chain:
            if block.block_type == 'version':
                miner_reward = 10  # Set a fixed reward for mining a version block
                self.submit_transaction('network', block.model_state['node_id'], miner_reward)


