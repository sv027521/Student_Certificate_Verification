from certificate_hash import load_certificates, generate_certificate_hash
from blockchain import create_certificate_blockchain


def verify_certificate(certificate_id):

    # Load certificate data
    df = load_certificates()

    # Create blockchain from all certificates
    blockchain = create_certificate_blockchain()

    # Search for certificate
    certificate = df[
        df["Certificate_ID"].astype(str) == str(certificate_id)
    ]

    # Certificate not found
    if certificate.empty:
        return {
            "status": "Invalid",
            "message": "Certificate ID not found."
        }

    # Get certificate record
    certificate = certificate.iloc[0]

    # Generate hash again
    generated_hash = generate_certificate_hash(certificate)

    # Compare with blockchain
    for block in blockchain.chain:

        if (
            str(block.certificate_id) == str(certificate_id)
            and block.certificate_hash == generated_hash
        ):

            return {
                "status": "Authentic",
                "certificate": certificate.to_dict(),
                "hash": generated_hash
            }

    # Hash does not match
    return {
        "status": "Invalid",
        "message": "Hash mismatch. Certificate may have been modified."
    }