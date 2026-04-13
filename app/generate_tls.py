from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import datetime
import os

# Generate private key
key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

# Certificate details
subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"CSHybrid"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, u"Dev"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"DevCompany"),
    x509.NameAttribute(NameOID.COMMON_NAME, u"localhost"),
])

# Build certificate
cert = (
    x509.CertificateBuilder()
    .subject_name(subject)
    .issuer_name(issuer)
    .public_key(key.public_key())
    .serial_number(x509.random_serial_number())
    .not_valid_before(datetime.datetime.utcnow())
    .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365))
    .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)
    .sign(key, hashes.SHA256())
)

# Create certs directory if it doesn't exist
os.makedirs("certs", exist_ok=True)

# Write key and cert to files
with open("certs/key.pem", "wb") as f:
    f.write(key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    ))

with open("certs/cert.pem", "wb") as f:
    f.write(cert.public_bytes(serialization.Encoding.PEM))

print(" Self-signed TLS certificate and private key created in certs/")

