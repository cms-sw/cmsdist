### RPM external conifer 1.3
## NOCOMPILER

Source: https://github.com/thesps/%{n}/archive/v%{realversion}.tar.gz
Requires: json

%prep
%setup -n %{n}-%{realversion}

%build

%install
mkdir -p %{i}/include/
cp conifer/backends/cpp/include/conifer.h     %{i}/include/

%post

