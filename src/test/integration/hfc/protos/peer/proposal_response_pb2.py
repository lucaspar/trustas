# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: hfc/protos/peer/proposal_response.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='hfc/protos/peer/proposal_response.proto',
  package='protos',
  syntax='proto3',
  serialized_pb=_b('\n\'hfc/protos/peer/proposal_response.proto\x12\x06protos\x1a\x1fgoogle/protobuf/timestamp.proto\"\xb1\x01\n\x10ProposalResponse\x12\x0f\n\x07version\x18\x01 \x01(\x05\x12-\n\ttimestamp\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\"\n\x08response\x18\x04 \x01(\x0b\x32\x10.protos.Response\x12\x0f\n\x07payload\x18\x05 \x01(\x0c\x12(\n\x0b\x65ndorsement\x18\x06 \x01(\x0b\x32\x13.protos.Endorsement\"<\n\x08Response\x12\x0e\n\x06status\x18\x01 \x01(\x05\x12\x0f\n\x07message\x18\x02 \x01(\t\x12\x0f\n\x07payload\x18\x03 \x01(\x0c\"C\n\x17ProposalResponsePayload\x12\x15\n\rproposal_hash\x18\x01 \x01(\x0c\x12\x11\n\textension\x18\x02 \x01(\x0c\"2\n\x0b\x45ndorsement\x12\x10\n\x08\x65ndorser\x18\x01 \x01(\x0c\x12\x11\n\tsignature\x18\x02 \x01(\x0c\x42h\n\"org.hyperledger.fabric.protos.peerB\x17ProposalResponsePackageZ)github.com/hyperledger/fabric/protos/peerb\x06proto3')
  ,
  dependencies=[google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,])




_PROPOSALRESPONSE = _descriptor.Descriptor(
  name='ProposalResponse',
  full_name='protos.ProposalResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='version', full_name='protos.ProposalResponse.version', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='protos.ProposalResponse.timestamp', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='response', full_name='protos.ProposalResponse.response', index=2,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='payload', full_name='protos.ProposalResponse.payload', index=3,
      number=5, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='endorsement', full_name='protos.ProposalResponse.endorsement', index=4,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=85,
  serialized_end=262,
)


_RESPONSE = _descriptor.Descriptor(
  name='Response',
  full_name='protos.Response',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='status', full_name='protos.Response.status', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='message', full_name='protos.Response.message', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='payload', full_name='protos.Response.payload', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=264,
  serialized_end=324,
)


_PROPOSALRESPONSEPAYLOAD = _descriptor.Descriptor(
  name='ProposalResponsePayload',
  full_name='protos.ProposalResponsePayload',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='proposal_hash', full_name='protos.ProposalResponsePayload.proposal_hash', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='extension', full_name='protos.ProposalResponsePayload.extension', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=326,
  serialized_end=393,
)


_ENDORSEMENT = _descriptor.Descriptor(
  name='Endorsement',
  full_name='protos.Endorsement',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='endorser', full_name='protos.Endorsement.endorser', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='signature', full_name='protos.Endorsement.signature', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=395,
  serialized_end=445,
)

_PROPOSALRESPONSE.fields_by_name['timestamp'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_PROPOSALRESPONSE.fields_by_name['response'].message_type = _RESPONSE
_PROPOSALRESPONSE.fields_by_name['endorsement'].message_type = _ENDORSEMENT
DESCRIPTOR.message_types_by_name['ProposalResponse'] = _PROPOSALRESPONSE
DESCRIPTOR.message_types_by_name['Response'] = _RESPONSE
DESCRIPTOR.message_types_by_name['ProposalResponsePayload'] = _PROPOSALRESPONSEPAYLOAD
DESCRIPTOR.message_types_by_name['Endorsement'] = _ENDORSEMENT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ProposalResponse = _reflection.GeneratedProtocolMessageType('ProposalResponse', (_message.Message,), dict(
  DESCRIPTOR = _PROPOSALRESPONSE,
  __module__ = 'hfc.protos.peer.proposal_response_pb2'
  # @@protoc_insertion_point(class_scope:protos.ProposalResponse)
  ))
_sym_db.RegisterMessage(ProposalResponse)

Response = _reflection.GeneratedProtocolMessageType('Response', (_message.Message,), dict(
  DESCRIPTOR = _RESPONSE,
  __module__ = 'hfc.protos.peer.proposal_response_pb2'
  # @@protoc_insertion_point(class_scope:protos.Response)
  ))
_sym_db.RegisterMessage(Response)

ProposalResponsePayload = _reflection.GeneratedProtocolMessageType('ProposalResponsePayload', (_message.Message,), dict(
  DESCRIPTOR = _PROPOSALRESPONSEPAYLOAD,
  __module__ = 'hfc.protos.peer.proposal_response_pb2'
  # @@protoc_insertion_point(class_scope:protos.ProposalResponsePayload)
  ))
_sym_db.RegisterMessage(ProposalResponsePayload)

Endorsement = _reflection.GeneratedProtocolMessageType('Endorsement', (_message.Message,), dict(
  DESCRIPTOR = _ENDORSEMENT,
  __module__ = 'hfc.protos.peer.proposal_response_pb2'
  # @@protoc_insertion_point(class_scope:protos.Endorsement)
  ))
_sym_db.RegisterMessage(Endorsement)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n\"org.hyperledger.fabric.protos.peerB\027ProposalResponsePackageZ)github.com/hyperledger/fabric/protos/peer'))
# @@protoc_insertion_point(module_scope)
