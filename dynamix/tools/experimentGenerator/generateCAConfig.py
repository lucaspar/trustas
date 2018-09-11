#!/usr/bin/python
import sys

print "#############################################################################"
# Server's listening port (default: 7054)
print "port: 7054"

# Enables debug logging (default: false)
print "debug: false"

# Size limit of an acceptable CRL in bytes (default: 512000)
print "crlsizelimit: 512000"

print "#############################################################################"
print "tls:"
  # Enable TLS (default: false)
print "  enabled: false"
  # TLS for the server's listening port
print "  certfile: ca-cert.pem"
print "  keyfile: ca-key.pem"
print "  clientauth:"
print "    type: noclientcert"
print "    certfiles:"

print "#############################################################################"
print "ca:"
  # Name of this CA
print "  name:"
  # Key file (default: ca-key.pem)
print "  keyfile: ca-key.pem"
  # Certificate file (default: ca-cert.pem)
print "  certfile: ca-cert.pem"
  # Chain file (default: chain-cert.pem)
print "  chainfile: ca-chain.pem"

print "#############################################################################"
print "registry:"
  # Maximum number of times a password/secret can be reused for enrollment
  # (default: -1, which means there is no limit)
print "  maxenrollments: -1"
  # Contains identity information which is used when LDAP is disabled
print "  identities:"
print "    - name: admin"
print "      pass: adminpw"
print "      type: client"
print "      affiliation: \"\""
print "      attrs:"
print "        hf.Registrar.Roles: \"client,user,peer,validator,auditor\""
print "        hf.Registrar.DelegateRoles: \"client,user,validator,auditor\""
print "        hf.Revoker: true"
print "        hf.IntermediateCA: true"

print "#############################################################################"
print "db:"
print "  type: sqlite3"
print "  datasource: fabric-ca-server.db"
print "  tls:"
print "    enabled: false"
print "    certfiles:"
print "      - db-server-cert.pem"
print "    client:"
print "      certfile: db-client-cert.pem"
print "      keyfile: db-client-key.pem"

print "#############################################################################"
print "ldap:"
   # Enables or disables the LDAP client (default: false)
   # If this is set to true, the "registry" section is ignored.
print "  enabled: false"
   # The URL of the LDAP server
print "  url: ldap://<adminDN>:<adminPassword>@<host>:<port>/<base>"
print "  tls:"
print "    certfiles:"
print "      - ldap-server-cert.pem"
print "    client:"
print "      certfile: ldap-client-cert.pem"
print "      keyfile: ldap-client-key.pem"

print "#############################################################################"
print "affiliations:"
for i in range(1, int(sys.argv[1])+1):
    print "  org"+str(i)+":"
    print "    - department1"

print "#############################################################################"
print "signing:"
print "  default:"
print "    usage:"
print "      - digital signature"
print "    expiry: 8760h"
print "  profiles:"
print "    ca:"
print "      usage:"
print "        - cert sign"
print "      expiry: 43800h"
print "      caconstraint:"
print "        isca: true"
print "        maxpathlen: 0"

print "#############################################################################"
print "csr:"
print "  cn: fabric-ca-server"
print "  names:"
print "    - C: US"
print "      ST: \"North Carolina\""
print "      L:"
print "      O: Hyperledger"
print "      OU: Fabric"
print "  hosts:"
print "    - ca2bab1d1c73"
print "    - localhost"
print "  ca:"
print "    expiry: 131400h"
print "    pathlength: 1"

print "#############################################################################"
print "bccsp:"
print "  default: SW"
print "  sw:"
print "    hash: SHA2"
print "    security: 256"
print "    filekeystore:"
            # The directory used for the software file-based keystore
print "      keystore: msp/keystore"

print "#############################################################################"

print "cacount:"
print "cafiles:"

print "#############################################################################"
print "intermediate:"
print "  parentserver:"
print "    url:"
print "    caname:"

print "  enrollment:"
print "    hosts:"
print "    profile:"
print "    label:"

print "  tls:"
print "    certfiles:"
print "    client:"
print "      certfile:"
print "      keyfile:"
