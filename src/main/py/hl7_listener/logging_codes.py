""" Common place to document project logging codes. HL7L = HL7 Listener service."""

# ERROR
HL7_MLLP_CONNECT_ERROR = "HL7LERR001: Error connecting to the HL7 MLLP listener port %s"
NATS_CONNECT_ERROR = "HL7LERR002: Error connecting to the NATS server %s"
NATS_NOT_INITIALIZED = "HL7LERR003: NATS not initialized."
HL7_MLLP_INCOMPLETE_READ = (
    "HL7LERR004: HL7 MLLP Unexpected incomplete message read error. peername=%s"
)
HL7_MLLP_RECEIVER_ERR = "HL7LERR005: HL7 MLLP Receiver encounterred exception."
HL7_MLLP_MSG_PARSE_ERR = "HL7LERR006: Received HL7 message is not a valid. peername=%s"
HL7_MLLP_UNKNOWN_ERR = (
    "HL7LERR007: Unknown error during HL7 receive message processing. peername=%s"
)


# INFO
STARTUP_ENV_VARS = (
    "HL7LLOG001: HL7 Listener started with the follow values from the env:\n"
    + 'HL7 MLLP listening host:port="%s:%s"\n'
    + 'NATS Jetstream Connection="%s" and Subject="%s"\n'
    + 'NATS Allow Reconnect:%s Reconnect attempts:%d\n'
    + 'NATS nkey file:"%s"\n'
    + 'CA certs file:"%s"'
)
HL7_MLLP_CONNECTED = "HL7LLOG002: HL7 Listener connection established. peername=%s"
HL7_MLLP_MSG_RECEIVED = "HL7LLOG003: HL7 Listener received a message."
HL7_MLLP_DISCONNECTED = "HL7LLOG004: HL7 Listener connection closed. peername=%s"
HL7_MLLP_RECEIVER_CANCELLED = (
    "HL7LLOG005: HL7 Listener was cancelled. This is not considered an error."
)
NATS_CONNECTED = "HL7LLOG006: Connected to the NATS server URL %s."
SENDING_MSG_TO_NATS = "HL7LLOG007: Sending message to the NATS JetStream server."
NATS_REQUEST_SEND_MSG_RESPONSE = (
    "HL7LLOG008: Response from NATS request for sending an HL7 message: %s"
)
HL7_MLLP_CONNECTION_CLOSING = (
    "HL7LLOG008: HL7 Listener connection from a sender peer is closing. peername=%s"
)
