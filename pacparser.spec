### RPM external pacparser 1.3.1
%define mic %(case %cmsplatf in (*_mic_*) echo true;; (*) echo false;; esac)
Source: http://%{n}.googlecode.com/files/%{n}-%{realversion}.tar.gz
%if "%mic" == "true"
Requires: icc
Source1: pacparser-1.3.1-mic1
Patch0: pacparser-1.3.1-mic
%endif

%prep
%setup -n %{n}-%{realversion}
%if "%mic" == "true"
cp %{_sourcedir}/pacparser-1.3.1-mic1 %{_builddir}
%patch0 -p1
%endif

%build
%if "%mic" == "true"
CXX="icpc -fPIC -mmic"  CC="icc -fPIC -mmic"  make -C src PREFIX=%{i}
%else
make -C src PREFIX=%{i}
%endif

%install
%if "%mic" == "true"
CXX="icpc -fPIC -mmic"  CC="icc -fPIC -mmic"  make -C src install PREFIX=%{i}
%else
make -C src install PREFIX=%{i}
%endif

%define strip_files %{i}/{lib,bin}
%define drop_files %{i}/{share,man}
