### RPM external tensorflow 2.3.1
%define source_package tensorflow-sources
%if "%{?vectorized_package:set}" != "set"
BuildRequires: %{source_package}
%define tf_root %(echo %{source_package}_ROOT | tr '[a-z-]' '[A-Z_]')
%else
BuildRequires: %{source_package}_%{vectorized_package}
%define tf_root %(echo %{source_package}_%{vectorized_package}_ROOT | tr '[a-z-]' '[A-Z_]')
%endif
Provides: libtensorflow_cc.so(tensorflow)(64bit)
Source: none

%prep

%build

%install

tar xfz ${%{tf_root}}/libtensorflow_cc.tar.gz -C %{i}
