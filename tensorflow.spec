### RPM external tensorflow 2.4.1
%define source_package tensorflow-sources
%if "%{?vectorized_package:set}" != "set"
BuildRequires: %{source_package}
%define tf_root %(echo %{source_package}_ROOT | tr '[a-z-]' '[A-Z_]')
%define tf_version %(echo %{source_package}_VERSION | tr '[a-z-]' '[A-Z_]')
%else
BuildRequires: %{source_package}_%{vectorized_package}
%define tf_root %(echo %{source_package}_%{vectorized_package}_ROOT | tr '[a-z-]' '[A-Z_]')
%endif
Provides: libtensorflow_cc.so(tensorflow)(64bit)
Source: none

%prep
case ${%{tf_version}} in
  %{realversion}|%{realversion}-*) ;;
  * ) echo "ERROR: Mismatch %{n} (%{realversion}) and %{source_package} (${%{tf_version}}) versions."
      echo "Please update %{n}.spec to use ${%{tf_version}} verison."
      exit 1
      ;;
esac

%build

%install

tar xfz ${%{tf_root}}/libtensorflow_cc.tar.gz -C %{i}
