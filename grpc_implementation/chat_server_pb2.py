# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chat_server.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11\x63hat_server.proto\"\x18\n\x04User\x12\x10\n\x08username\x18\x01 \x01(\t\"9\n\x04Text\x12\x0e\n\x06sender\x18\x01 \x01(\t\x12\x10\n\x08receiver\x18\x02 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x03 \x01(\t\"\"\n\x0fText_Returnable\x12\x0f\n\x07\x63ontent\x18\x01 \x01(\t\"\x1f\n\x06Status\x12\x15\n\rstatus_result\x18\x01 \x01(\t\"!\n\x06Search\x12\x17\n\x0fusername_search\x18\x01 \x01(\t2\xf5\x01\n\x0c\x43hat_Service\x12\x18\n\x06logout\x12\x05.User\x1a\x07.Status\x12\x1e\n\x0csend_message\x12\x05.Text\x1a\x07.Status\x12\x1d\n\x0b\x63reate_user\x12\x05.User\x1a\x07.Status\x12\x1d\n\x0b\x64\x65lete_user\x12\x05.User\x1a\x07.Status\x12\x17\n\x05login\x12\x05.User\x1a\x07.Status\x12)\n\x0csearch_users\x12\x07.Search\x1a\x10.Text_Returnable\x12)\n\x0cstream_chats\x12\x05.User\x1a\x10.Text_Returnable0\x01\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'chat_server_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _USER._serialized_start=21
  _USER._serialized_end=45
  _TEXT._serialized_start=47
  _TEXT._serialized_end=104
  _TEXT_RETURNABLE._serialized_start=106
  _TEXT_RETURNABLE._serialized_end=140
  _STATUS._serialized_start=142
  _STATUS._serialized_end=173
  _SEARCH._serialized_start=175
  _SEARCH._serialized_end=208
  _CHAT_SERVICE._serialized_start=211
  _CHAT_SERVICE._serialized_end=456
# @@protoc_insertion_point(module_scope)
