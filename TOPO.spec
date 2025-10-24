### RPM external TOPO 0.1.0
Name: TOPO
Source: https://github.com/cms-hls4ml/%{n}/archive/refs/tags/v%{realversion}.tar.gz

Requires: hls4mlEmulatorExtras hls
BuildRequires: gmake

%prep
%setup -n %{n}-%{realversion}

%build
make %{?_smp_mflags} EMULATOR_EXTRAS=${HLS4MLEMULATOREXTRAS_ROOT} HLS_ROOT=${HLS_ROOT}

%install
make PREFIX=%{i} install
