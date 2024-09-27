### RPM external tensorflow 2.17.0
%if "%{?vectorized_package:set}" != "set"
%define source_package tensorflow-sources
%else
%define source_package tensorflow-sources_%{vectorized_package}
%endif
## INCLUDE tensorflow-requires
BuildRequires: %{source_package} py3-wheel
%define tf_major %(echo %realversion | cut -d. -f1)
%define tf_root %(echo %{source_package}_ROOT | tr '[a-z-]' '[A-Z_]')
Source: none

%prep

%build

%install
mkdir %{i}/lib %{i}/xla-aot-runtime
rm -rf tensorflow-%{realversion}
wheel unpack ${%{tf_root}}/tensorflow-%{realversion}*-cp%{cms_python3_major_minor}-cp%{cms_python3_major_minor}-linux_%{_arch}.whl
mv tensorflow-%{realversion}/tensorflow/include %{i}/include
for l in libtensorflow_cc.so  libtensorflow_framework.so ; do
  mv tensorflow-%{realversion}/tensorflow/${l}.%{tf_major} %{i}/lib
  ln -s ${l}.%{tf_major} %{i}/lib/${l}
done
mv tensorflow-%{realversion}/tensorflow/xla_aot_runtime_src %{i}/xla-aot-runtime/src
cp -r ${%{tf_root}}/lib-xla-runtime %{i}/xla-aot-runtime/lib

%if %{enable_gpu}
mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/tf_cuda_support.xml
  <tool name="tf_cuda_support" version="1.0">
  </tool>
EOF_TOOLFILE
%endif
