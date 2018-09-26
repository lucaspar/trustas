# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: hfc/protos/peer/proposal.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from hfc.protos.peer import chaincode_pb2 as hfc_dot_protos_dot_peer_dot_chaincode__pb2
from hfc.protos.peer import proposal_response_pb2 as hfc_dot_protos_dot_peer_dot_proposal__response__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='hfc/protos/peer/proposal.proto',
  package='protos',
  syntax='proto3',
  serialized_pb=_b('\n\x1ehfc/protos/peer/proposal.proto\x12\x06protos\x1a\x1fhfc/protos/peer/chaincode.proto\x1a\'hfc/protos/peer/proposal_response.proto\";\n\x0eSignedProposal\x12\x16\n\x0eproposal_bytes\x18\x01 \x01(\x0c\x12\x11\n\tsignature\x18\x02 \x01(\x0c\">\n\x08Proposal\x12\x0e\n\x06header\x18\x01 \x01(\x0c\x12\x0f\n\x07payload\x18\x02 \x01(\x0c\x12\x11\n\textension\x18\x03 \x01(\x0c\"a\n\x18\x43haincodeHeaderExtension\x12\x1a\n\x12payload_visibility\x18\x01 \x01(\x0c\x12)\n\x0c\x63haincode_id\x18\x02 \x01(\x0b\x32\x13.protos.ChaincodeID\"\xa8\x01\n\x18\x43haincodeProposalPayload\x12\r\n\x05input\x18\x01 \x01(\x0c\x12H\n\x0cTransientMap\x18\x02 \x03(\x0b\x32\x32.protos.ChaincodeProposalPayload.TransientMapEntry\x1a\x33\n\x11TransientMapEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x0c:\x02\x38\x01\"\x81\x01\n\x0f\x43haincodeAction\x12\x0f\n\x07results\x18\x01 \x01(\x0c\x12\x0e\n\x06\x65vents\x18\x02 \x01(\x0c\x12\"\n\x08response\x18\x03 \x01(\x0b\x32\x10.protos.Response\x12)\n\x0c\x63haincode_id\x18\x04 \x01(\x0b\x32\x13.protos.ChaincodeIDB`\n\"org.hyperledger.fabric.protos.peerB\x0fProposalPackageZ)github.com/hyperledger/fabric/protos/peerb\x06proto3')
  ,
  dependencies=[hfc_dot_protos_dot_peer_dot_chaincode__pb2.DESCRIPTOR,hfc_dot_protos_dot_peer_dot_proposal__response__pb2.DESCRIPTOR,])




_SIGNEDPROPOSAL = _descriptor.Descriptor(
  name='SignedProposal',
  full_name='protos.SignedProposal',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='proposal_bytes', full_name='protos.SignedProposal.proposal_bytes', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='signature', full_name='protos.SignedProposal.signature', index=1,
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
  serialized_start=116,
  serialized_end=175,
)


_PROPOSAL = _descriptor.Descriptor(
  name='Proposal',
  full_name='protos.Proposal',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='header', full_name='protos.Proposal.header', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='payload', full_name='protos.Proposal.payload', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='extension', full_name='protos.Proposal.extension', index=2,
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
  serialized_start=177,
  serialized_end=239,
)


_CHAINCODEHEADEREXTENSION = _descriptor.Descriptor(
  name='ChaincodeHeaderExtension',
  full_name='protos.ChaincodeHeaderExtension',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='payload_visibility', full_name='protos.ChaincodeHeaderExtension.payload_visibility', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='chaincode_id', full_name='protos.ChaincodeHeaderExtension.chaincode_id', index=1,
      number=2, type=11, cpp_type=10, label=1,
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
  serialized_start=241,
  serialized_end=338,
)


_CHAINCODEPROPOSALPAYLOAD_TRANSIENTMAPENTRY = _descriptor.Descriptor(
  name='TransientMapEntry',
  full_name='protos.ChaincodeProposalPayload.TransientMapEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='protos.ChaincodeProposalPayload.TransientMapEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='protos.ChaincodeProposalPayload.TransientMapEntry.value', index=1,
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
  options=_descriptor._ParseOptions(descriptor_pb2.MessageOptions(), _b('8\001')),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=458,
  serialized_end=509,
)

_CHAINCODEPROPOSALPAYLOAD = _descriptor.Descriptor(
  name='ChaincodeProposalPayload',
  full_name='protos.ChaincodeProposalPayload',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='input', full_name='protos.ChaincodeProposalPayload.input', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='TransientMap', full_name='protos.ChaincodeProposalPayload.TransientMap', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_CHAINCODEPROPOSALPAYLOAD_TRANSIENTMAPENTRY, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=341,
  serialized_end=509,
)


_CHAINCODEACTION = _descriptor.Descriptor(
  name='ChaincodeAction',
  full_name='protos.ChaincodeAction',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='results', full_name='protos.ChaincodeAction.results', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='events', full_name='protos.ChaincodeAction.events', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='response', full_name='protos.ChaincodeAction.response', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='chaincode_id', full_name='protos.ChaincodeAction.chaincode_id', index=3,
      number=4, type=11, cpp_type=10, label=1,
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
  serialized_start=512,
  serialized_end=641,
)

_CHAINCODEHEADEREXTENSION.fields_by_name['chaincode_id'].message_type = hfc_dot_protos_dot_peer_dot_chaincode__pb2._CHAINCODEID
_CHAINCODEPROPOSALPAYLOAD_TRANSIENTMAPENTRY.containing_type = _CHAINCODEPROPOSALPAYLOAD
_CHAINCODEPROPOSALPAYLOAD.fields_by_name['TransientMap'].message_type = _CHAINCODEPROPOSALPAYLOAD_TRANSIENTMAPENTRY
_CHAINCODEACTION.fields_by_name['response'].message_type = hfc_dot_protos_dot_peer_dot_proposal__response__pb2._RESPONSE
_CHAINCODEACTION.fields_by_name['chaincode_id'].message_type = hfc_dot_protos_dot_peer_dot_chaincode__pb2._CHAINCODEID
DESCRIPTOR.message_types_by_name['SignedProposal'] = _SIGNEDPROPOSAL
DESCRIPTOR.message_types_by_name['Proposal'] = _PROPOSAL
DESCRIPTOR.message_types_by_name['ChaincodeHeaderExtension'] = _CHAINCODEHEADEREXTENSION
DESCRIPTOR.message_types_by_name['ChaincodeProposalPayload'] = _CHAINCODEPROPOSALPAYLOAD
DESCRIPTOR.message_types_by_name['ChaincodeAction'] = _CHAINCODEACTION
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

SignedProposal = _reflection.GeneratedProtocolMessageType('SignedProposal', (_message.Message,), dict(
  DESCRIPTOR = _SIGNEDPROPOSAL,
  __module__ = 'hfc.protos.peer.proposal_pb2'
  # @@protoc_insertion_point(class_scope:protos.SignedProposal)
  ))
_sym_db.RegisterMessage(SignedProposal)

Proposal = _reflection.GeneratedProtocolMessageType('Proposal', (_message.Message,), dict(
  DESCRIPTOR = _PROPOSAL,
  __module__ = 'hfc.protos.peer.proposal_pb2'
  # @@protoc_insertion_point(class_scope:protos.Proposal)
  ))
_sym_db.RegisterMessage(Proposal)

ChaincodeHeaderExtension = _reflection.GeneratedProtocolMessageType('ChaincodeHeaderExtension', (_message.Message,), dict(
  DESCRIPTOR = _CHAINCODEHEADEREXTENSION,
  __module__ = 'hfc.protos.peer.proposal_pb2'
  # @@protoc_insertion_point(class_scope:protos.ChaincodeHeaderExtension)
  ))
_sym_db.RegisterMessage(ChaincodeHeaderExtension)

ChaincodeProposalPayload = _reflection.GeneratedProtocolMessageType('ChaincodeProposalPayload', (_message.Message,), dict(

  TransientMapEntry = _reflection.GeneratedProtocolMessageType('TransientMapEntry', (_message.Message,), dict(
    DESCRIPTOR = _CHAINCODEPROPOSALPAYLOAD_TRANSIENTMAPENTRY,
    __module__ = 'hfc.protos.peer.proposal_pb2'
    # @@protoc_insertion_point(class_scope:protos.ChaincodeProposalPayload.TransientMapEntry)
    ))
  ,
  DESCRIPTOR = _CHAINCODEPROPOSALPAYLOAD,
  __module__ = 'hfc.protos.peer.proposal_pb2'
  # @@protoc_insertion_point(class_scope:protos.ChaincodeProposalPayload)
  ))
_sym_db.RegisterMessage(ChaincodeProposalPayload)
_sym_db.RegisterMessage(ChaincodeProposalPayload.TransientMapEntry)

ChaincodeAction = _reflection.GeneratedProtocolMessageType('ChaincodeAction', (_message.Message,), dict(
  DESCRIPTOR = _CHAINCODEACTION,
  __module__ = 'hfc.protos.peer.proposal_pb2'
  # @@protoc_insertion_point(class_scope:protos.ChaincodeAction)
  ))
_sym_db.RegisterMessage(ChaincodeAction)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n\"org.hyperledger.fabric.protos.peerB\017ProposalPackageZ)github.com/hyperledger/fabric/protos/peer'))
_CHAINCODEPROPOSALPAYLOAD_TRANSIENTMAPENTRY.has_options = True
_CHAINCODEPROPOSALPAYLOAD_TRANSIENTMAPENTRY._options = _descriptor._ParseOptions(descriptor_pb2.MessageOptions(), _b('8\001'))
# @@protoc_insertion_point(module_scope)
