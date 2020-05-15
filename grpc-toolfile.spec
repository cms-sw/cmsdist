### RPM external grpc-toolfile 1.0
Requires: grpc

%prep

%build

%install
mkdir -p %i/etc/scram.d

cat << \EOF_TOOLFILE >%i/etc/scram.d/grpc.xml
<tool name="grpc" version="@TOOL_VERSION@">
  <info url="https://github.com/grpc/grpc"/>
  <client>
    <environment name="GRPC_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE" default="$GRPC_BASE/include"/>
    <environment name="LIBDIR" default="$GRPC_BASE/lib"/>
  </client>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/grpc-absl.xml
<tool name="grpc-absl" version="@TOOL_VERSION@">
  <lib name="absl_algorithm"/>
  <lib name="absl_atomic_hook"/>
  <lib name="absl_bad_optional_access"/>
  <lib name="absl_base"/>
  <lib name="absl_base_internal"/>
  <lib name="absl_bits"/>
  <lib name="absl_civil_time"/>
  <lib name="absl_compressed_tuple"/>
  <lib name="absl_config"/>
  <lib name="absl_core_headers"/>
  <lib name="absl_dynamic_annotations"/>
  <lib name="absl_endian"/>
  <lib name="absl_errno_saver"/>
  <lib name="absl_inlined_vector"/>
  <lib name="absl_inlined_vector_internal"/>
  <lib name="absl_int128"/>
  <lib name="absl_log_severity"/>
  <lib name="absl_memory"/>
  <lib name="absl_optional"/>
  <lib name="absl_raw_logging_internal"/>
  <lib name="absl_span"/>
  <lib name="absl_spinlock_wait"/>
  <lib name="absl_str_format"/>
  <lib name="absl_str_format_internal"/>
  <lib name="absl_strings"/>
  <lib name="absl_strings_internal"/>
  <lib name="absl_throw_delegate"/>
  <lib name="absl_time"/>
  <lib name="absl_time_zone"/>
  <lib name="absl_type_traits"/>
  <lib name="absl_utility"/>
  <lib name="absl_meta"/>
  <use name="grpc"/>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/grpc-lib.xml
<tool name="grpc-lib" version="@TOOL_VERSION@">
  <lib name="grpc"/>
  <lib name="grpc++"/>
  <lib name="grpc++_reflection"/>
  <lib name="cares"/>
  <lib name="address_sorting"/>
  <use name="grpc"/>
  <use name="grpc-absl"/>
  <use name="protobuf"/>
  <use name="openssl"/>
  <use name="pcre"/>
  <use name="grpc-absl"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
