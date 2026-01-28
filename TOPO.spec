### RPM external TOPO 5.0.0
Source: https://github.com/cms-hls4ml/%{n}/archive/refs/tags/v%{realversion}.tar.gz
Requires: hls4mlEmulatorExtras hls
BuildRequires: gmake

%prep
%setup -n %{n}-%{realversion}

%build
make %{?_smp_mflags} EMULATOR_EXTRAS=${HLS4MLEMULATOREXTRAS_ROOT} HLS_ROOT=${HLS_ROOT}

%install
make PREFIX=%{i} install
