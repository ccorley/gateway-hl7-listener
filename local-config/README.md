# gateway-hl7-listener NATS configuration
The HL7 listener NATS configuration for LinuxForHealth connect requires a CA certs file (lfh-root-ca.pem) and a NATS nkey file(nats-server.nk).

These files must match the files used by the deployed instance of LinuxForHealth connect.  If the LinuxForHealth connect root CA file or NATS nkey file is regenerated, it must be copied to this directory to replace the existing file.
