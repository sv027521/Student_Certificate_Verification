import pandas as pd
import hashlib


def generate_certificate_hash(certificate):

    certificate_data = (
        str(certificate["Certificate_ID"]) +
        str(certificate["Student_ID"]) +
        str(certificate["Course"]) +
        str(certificate["Institution"]) +
        str(certificate["Year"]) +
        str(certificate["Certificate_Type"]) +
        str(certificate["Issue_Date"]) +
        str(certificate["Verification_Code"])
    )

    certificate_hash = hashlib.sha256(
        certificate_data.encode()
    ).hexdigest()

    return certificate_hash


def load_certificates():

    df = pd.read_csv("certificates.csv")

    return df