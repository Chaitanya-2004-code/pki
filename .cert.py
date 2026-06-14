import subprocess

# Take inputs
root = input("Enter root name: ")
subca = input("Enter subca name: ")
private = input("Enter private name: ")

# Root CA
print(f'openssl genrsa -out {root}.key 2048')
subprocess.run(f'openssl genrsa -out {root}.key 2048', shell=True)

print(f'openssl req -x509 -new -nodes -key {root}.key -sha256 -days 3650 -out {root}.crt')
subprocess.run(f'openssl req -x509 -new -nodes -key {root}.key -sha256 -days 3650 -out {root}.crt', shell=True)

# SubCA
print('echo "===============SubCA=================="')

print(f'openssl genrsa -out {subca}.key 2048')
subprocess.run(f'openssl genrsa -out {subca}.key 2048', shell=True)

print(f'openssl req -new -key {subca}.key -out {subca}.csr')
subprocess.run(f'openssl req -new -key {subca}.key -out {subca}.csr', shell=True)

# Create subca_ext.cnf
subca_ext = """basicConstraints=critical,CA:TRUE,pathlen:0
keyUsage=critical,keyCertSign,cRLSign
subjectKeyIdentifier=hash
authorityKeyIdentifier=keyid,issuer
"""
with open(f"{subca}_ext.cnf", "w") as f:
    f.write(subca_ext)

print(f'openssl x509 -req -in {subca}.csr -CA {root}.crt -CAkey {root}.key -CAcreateserial -out {subca}.crt -days 1825 -sha256 -extfile {subca}_ext.cnf')
subprocess.run(f'openssl x509 -req -in {subca}.csr -CA {root}.crt -CAkey {root}.key -CAcreateserial -out {subca}.crt -days 1825 -sha256 -extfile {subca}_ext.cnf', shell=True)

# Private cert
print('echo "===============private=================="')

print(f'openssl genrsa -out {private}.key 2048')
subprocess.run(f'openssl genrsa -out {private}.key 2048', shell=True)

print(f'openssl req -new -key {private}.key -out {private}.csr')
subprocess.run(f'openssl req -new -key {private}.key -out {private}.csr', shell=True)

# Create private_ext.cnf
private_ext = f"""basicConstraints=critical,CA:FALSE
keyUsage=critical,digitalSignature,nonRepudiation,keyEncipherment,keyAgreement
extendedKeyUsage=serverAuth,clientAuth,emailProtection
subjectAltName=@alt_names
[alt_names]
DNS.1= www.{private}.com
"""
with open(f"{private}_ext.cnf", "w") as f:
    f.write(private_ext)

print(f'openssl x509 -req -in {private}.csr -CA {subca}.crt -CAkey {subca}.key -CAcreateserial -out {private}.crt -days 365 -sha256 -extfile {private}_ext.cnf')
subprocess.run(f'openssl x509 -req -in {private}.csr -CA {subca}.crt -CAkey {subca}.key -CAcreateserial -out {private}.crt -days 365 -sha256 -extfile {private}_ext.cnf', shell=True)

# Full chain
print(f'cat {private}.crt {subca}.crt {root}.crt > fullchain.crt')
subprocess.run(f'cat {private}.crt {subca}.crt {root}.crt > fullchain.crt', shell=True)
