import streamlit as st
import pandas as pd

from certificate_hash import load_certificates
from blockchain import create_certificate_blockchain
from hash_utils import verify_certificate

st.set_page_config(
    page_title="Student Certificate Verification",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Student Certificate Verification System")
st.write("Verify student certificates using SHA-256 hashing and a simulated blockchain.")

@st.cache_data
def get_data():
    return load_certificates()

df = get_data()

st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    ["🏠 Home", "🔍 Verify Certificate", "📊 Dashboard",
     "⛓ Blockchain Explorer", "ℹ️ About Project"]
)

if page == "🏠 Home":
    st.header("Welcome")
    st.write(
        "This system verifies the authenticity of student certificates. "
        "Certificate information is converted into a SHA-256 digital fingerprint "
        "and stored in a simulated blockchain."
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Certificates", len(df))
    c2.metric("Unique Students", df["Student_ID"].nunique())
    c3.metric("Certificate Types", df["Certificate_Type"].nunique())

    st.subheader("How it works")
    st.markdown("""
    1. Certificate data is read from the CSV file.
    2. Important certificate information is converted into a SHA-256 hash.
    3. The hash is stored in a simulated blockchain block.
    4. During verification, the hash is generated again.
    5. Matching hashes mean the certificate is authentic.
    """)

elif page == "🔍 Verify Certificate":
    st.header("🔍 Verify Certificate")

    certificate_id = st.text_input(
        "Enter Certificate ID",
        placeholder="Example: CERT001"
    )

    if st.button("🔎 Verify Certificate", type="primary"):
        if not certificate_id.strip():
            st.warning("Please enter a Certificate ID.")
        else:
            result = verify_certificate(certificate_id.strip())

            if result["status"] == "Authentic":
                st.success("✅ CERTIFICATE AUTHENTIC")
                st.write("The certificate hash matches the blockchain record.")

                certificate = result["certificate"]

                st.subheader("Certificate Details")

                c1, c2 = st.columns(2)

                with c1:
                    st.write("**Certificate ID:**", certificate.get("Certificate_ID"))
                    st.write("**Student ID:**", certificate.get("Student_ID"))
                    st.write("**Course:**", certificate.get("Course"))
                    st.write("**Institution:**", certificate.get("Institution"))

                with c2:
                    st.write("**Year:**", certificate.get("Year"))
                    st.write("**Certificate Type:**", certificate.get("Certificate_Type"))
                    st.write("**Issue Date:**", certificate.get("Issue_Date"))
                    st.write("**Verification Code:**", certificate.get("Verification_Code"))

                st.subheader("SHA-256 Hash")
                st.code(result["hash"])

            else:
                st.error("❌ CERTIFICATE NOT VERIFIED")
                st.error(result["message"])

elif page == "📊 Dashboard":
    st.header("📊 Certificate Dashboard")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Certificates", len(df))
    c2.metric("Students", df["Student_ID"].nunique())
    c3.metric("Institutions", df["Institution"].nunique())
    c4.metric("Courses", df["Course"].nunique())

    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Certificates by Course")
        st.bar_chart(df["Course"].value_counts())

    with c2:
        st.subheader("Certificates by Year")
        st.bar_chart(df["Year"].value_counts().sort_index())

    c3, c4 = st.columns(2)

    with c3:
        st.subheader("Certificate Types")
        st.bar_chart(df["Certificate_Type"].value_counts())

    with c4:
        st.subheader("Certificate Status")
        st.bar_chart(df["Status"].value_counts())

    st.subheader("Certificate Data")
    st.dataframe(df, use_container_width=True, hide_index=True)

elif page == "⛓ Blockchain Explorer":
    st.header("⛓ Simulated Blockchain Explorer")

    blockchain = create_certificate_blockchain()

    st.metric("Total Blockchain Blocks", len(blockchain.chain))

    for block in blockchain.chain:
        with st.expander(f"Block {block.index} — {block.certificate_id}"):
            st.write("**Certificate ID:**", block.certificate_id)
            st.write("**Timestamp:**", block.timestamp)
            st.write("**Certificate Hash:**")
            st.code(block.certificate_hash)
            st.write("**Previous Block Hash:**")
            st.code(block.previous_hash)
            st.write("**Block Hash:**")
            st.code(block.calculate_block_hash())

elif page == "ℹ️ About Project":
    st.header("ℹ️ About Project")

    st.subheader("Objective")
    st.write(
        "The Student Certificate Verification System verifies certificate "
        "authenticity using SHA-256 hashing and a simulated blockchain."
    )

    st.subheader("Technologies")
    st.markdown("""
    - Python
    - Streamlit
    - Pandas
    - SHA-256 hashing
    - Simulated blockchain
    """)

    st.subheader("Verification Flow")
    st.code(
        "Certificate Data → SHA-256 Hash → Blockchain → "
        "Recalculate Hash → Compare → Authentic / Not Verified"
    )

    st.info(
        "This is a simulated blockchain created for academic demonstration; "
        "it is not a real decentralized blockchain network."
    )
