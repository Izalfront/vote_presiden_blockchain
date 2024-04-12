import json
import random
from uuid import uuid4

# Fungsi untuk menghasilkan suara acak
def generate_random_votes(num_votes):
    valid_candidates = ['A', 'B', 'C']
    votes = []
    for _ in range(num_votes):
        candidate = random.choice(valid_candidates)
        voter_id = str(uuid4())
        vote = {'voter_id': voter_id, 'candidate': candidate}
        votes.append(vote)
    return votes

# Fungsi untuk menyimpan suara ke file JSON
def save_votes_to_json(votes, filename):
    with open(filename, 'w') as f:
        json.dump(votes, f)

# Contoh penggunaan: generate 10 suara acak dan simpan ke file 'votes.json'
if __name__ == '__main__':
    num_votes = 10  # Ganti jumlah suara yang ingin di-generate
    random_votes = generate_random_votes(num_votes)
    save_votes_to_json(random_votes, 'blockchain.json')
    print(f'Suara acak berhasil disimpan ke file "blockchain.json"')
