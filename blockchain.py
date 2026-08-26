import hashlib
from datetime import datetime

from certificate_hash import (
    load_certificates,
    generate_certificate_hash
)


# -----------------------------
# Block
# -----------------------------

class Block:

    def __init__(
        self,
        index,
        certificate_id,
        certificate_hash,
        previous_hash
    ):

        self.index = index
        self.certificate_id = certificate_id
        self.certificate_hash = certificate_hash
        self.previous_hash = previous_hash
        self.timestamp = str(datetime.now())

    def calculate_block_hash(self):

        block_data = (
            str(self.index) +
            self.certificate_id +
            self.certificate_hash +
            self.previous_hash +
            self.timestamp
        )

        return hashlib.sha256(
            block_data.encode()
        ).hexdigest()


# -----------------------------
# Blockchain
# -----------------------------

class Blockchain:

    def __init__(self):

        self.chain = []

        self.create_genesis_block()

    def create_genesis_block(self):

        genesis_block = Block(
            0,
            "GENESIS",
            "GENESIS_HASH",
            "0000000000000000"
        )

        self.chain.append(genesis_block)

    def add_certificate(
        self,
        certificate_id,
        certificate_hash
    ):

        previous_block = self.chain[-1]

        new_block = Block(
            len(self.chain),
            certificate_id,
            certificate_hash,
            previous_block.calculate_block_hash()
        )

        self.chain.append(new_block)


# -----------------------------
# Create blockchain from CSV
# -----------------------------

def create_certificate_blockchain():

    df = load_certificates()

    blockchain = Blockchain()

    for _, certificate in df.iterrows():

        certificate_hash = generate_certificate_hash(
            certificate
        )

        blockchain.add_certificate(
            certificate["Certificate_ID"],
            certificate_hash
        )

    return blockchain


# -----------------------------
# Test
# -----------------------------

if __name__ == "__main__":

    blockchain = create_certificate_blockchain()

    print("===================================")
    print("SIMULATED CERTIFICATE BLOCKCHAIN")
    print("===================================")

    print(
        "Total Blocks:",
        len(blockchain.chain)
    )

    print()

    for block in blockchain.chain[:5]:

        print("-----------------------------------")
        print("Block:", block.index)
        print(
            "Certificate ID:",
            block.certificate_id
        )
        print(
            "Certificate Hash:",
            block.certificate_hash
        )
        print(
            "Previous Hash:",
            block.previous_hash
        )