import hashlib
import json
from time import time
from uuid import uuid4
from flask import Flask, jsonify, request 


class Blockchain:
    def __init__(self):
        # Inisialisasi blockchain
        self.chain = []
        self.current_votes = []
        self.nodes = set()

        # Coba memuat blockchain dari file JSON saat inisialisasi
        self.load_blockchain()

    def save_blockchain(self):
        # Simpan blockchain ke file JSON
        with open('blockchain.json', 'w') as f:
            json.dump(self.chain, f)

    def load_blockchain(self):
        try:
            # Coba memuat blockchain dari file JSON jika ada
            with open('blockchain.json', 'r') as f:
                self.chain = json.load(f)
        except FileNotFoundError:
            # Jika file tidak ditemukan, buat blockchain baru
            self.chain = []
        except json.JSONDecodeError:
            # Tangani kesalahan jika JSON tidak dapat diuraikan dengan benar
            print("Error: Failed to decode JSON file. Creating new blockchain.")
            self.chain = []

    def new_block(self, proof, previous_hash=None):
        # Fungsi untuk menambahkan blok baru ke blockchain
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'votes': self.current_votes,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.current_votes = []
        self.chain.append(block)
        self.save_blockchain()  # Simpan blockchain setelah menambahkan blok baru
        return block

    def new_vote(self, candidate):
        valid_candidates = ['A', 'B', 'C']
        if candidate not in valid_candidates:
            return False  # Jika kandidat tidak valid, vote tidak dicatat
        
        self.current_votes.append({
            'voter_id': str(uuid4()),
            'candidate': candidate
        })
        self.save_blockchain()
        return True

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"  # Contoh kesulitan sederhana untuk validasi

# Inisialisasi node Flask
app = Flask(__name__)

# Buat instance blockchain
blockchain = Blockchain()

# Buat endpoint untuk menambahkan suara pemilihan
@app.route('/vote', methods=['POST'])
def new_vote():
    values = request.get_json()

    if not values or 'candidate' not in values:
        return jsonify({'error': 'Invalid request. Missing candidate field.'}), 400

    candidate = values['candidate']
    if blockchain.new_vote(candidate):
        index = len(blockchain.chain)  # Menggunakan panjang rantai sebagai indeks block
        response = {'message': f'Vote untuk kandidat {candidate} akan dicatat pada block {index}'}
        return jsonify(response), 201
    else:
        return jsonify({'error': 'Invalid candidate. Candidate must be A, B, or C.'}), 400

# Buat endpoint untuk menampilkan blockchain lengkap
@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
