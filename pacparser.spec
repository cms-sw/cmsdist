### RPM external pacparser 1.3.1
Source: http://%{n}.googlecode.com/files/%{n}-%{realversion}.tar.gz

%prep
%setup -n %{n}-%{realversion}

%build
make -C src PREFIX=%{i}

%install
make -C src install PREFIX=%{i}

%define strip_files %{i}/{lib,bin}
%define drop_files %{i}/{share,man}
