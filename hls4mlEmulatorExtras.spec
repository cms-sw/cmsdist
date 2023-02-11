### RPM external hls4mlEmulatorExtras 1.2.0
Source: https://github.com/cms-hls4ml/%{n}/archive/refs/tags/v%{realversion}.tar.gz
BuildRequires: gmake

%prep
%setup -n %{n}-%{realversion}

%build
make %{makeprocesses} 

%install
make PREFIX=%{i} install
