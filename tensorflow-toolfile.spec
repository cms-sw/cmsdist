### RPM external tensorflow-toolfile 3.0
%define base_package %(echo %{n} | sed 's|-toolfile||')
%define base_package_uc %(echo %{base_package} | tr '[a-z-]' '[A-Z_]')
%{expand:%(for v in %{package_vectorization}; do echo Requires: %{base_package}_$v; done)}
Requires: %{base_package}

%prep

%build

%install

mkdir -p %i/etc/scram.d

cat << \EOF_TOOLFILE > %i/etc/scram.d/%{base_package}.xml
<tool name="%{base_package}" version="@TOOL_VERSION@">
  <client>
    <environment name="TENSORFLOW_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$TENSORFLOW_BASE/lib"/>
    <environment name="INCLUDE" default="$TENSORFLOW_BASE/include"/>
EOF_TOOLFILE
for v in $(echo %{package_vectorization} | tr '[a-z-]' '[A-Z_]')  ; do
  r=`eval echo \\$%{base_package_uc}_${v}_ROOT`
  echo "  <runtime name=\"${v}_LIBDIR\" value=\"${r}/lib\" type=\"path\"/>" >> %i/etc/scram.d/%{base_package}.xml
done
cat << \EOF_TOOLFILE >>%i/etc/scram.d/%{base_package}.xml
  </client>
  <runtime name="PATH" value="$TENSORFLOW_BASE/bin" type="path"/>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE > %i/etc/scram.d/tensorflow-framework.xml
<tool name="tensorflow-framework" version="@TOOL_VERSION@">
  <lib name="tensorflow_framework"/>
  <use name="tensorflow"/>
  <use name="giflib"/>
  <use name="zlib"/>
  <use name="libjpeg-turbo"/>
  <use name="protobuf"/>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE > %i/etc/scram.d/tensorflow-cc.xml
<tool name="tensorflow-cc" version="@TOOL_VERSION@">
  <lib name="tensorflow_cc"/>
  <use name="tensorflow-framework"/>
  <use name="eigen"/>
  <use name="libpng"/>
  <use name="sqlite"/>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE > %i/etc/scram.d/tensorflow-c.xml
<tool name="tensorflow-c" version="@TOOL_VERSION@">
  <lib name="tensorflow"/>
  <use name="tensorflow-framework"/>
  <use name="eigen"/>
  <use name="libpng"/>
  <use name="sqlite"/>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE > %i/etc/scram.d/tensorflow-runtime.xml
<tool name="tensorflow-runtime" version="@TOOL_VERSION@">
  <lib name="cpu_function_runtime"/>
  <use name="tensorflow"/>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE > %i/etc/scram.d/tensorflow-executable_run_options.xml
<tool name="tensorflow-executable_run_options" version="@TOOL_VERSION@">
  <lib name="executable_run_options"/>
  <use name="tensorflow"/>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE > %i/etc/scram.d/tensorflow-xla_compiled_cpu_function.xml
<tool name="tensorflow-xla_compiled_cpu_function" version="@TOOL_VERSION@">
  <lib name="xla_compiled_cpu_function"/>
  <use name="tensorflow"/>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE > %i/etc/scram.d/tensorflow-tf2xla.xml
<tool name="tensorflow-tf2xla" version="@TOOL_VERSION@">
  <lib name="tf2xla"/>
  <use name="tensorflow"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
