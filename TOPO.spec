### RPM external TOPO 0.1.0
# to be used in future Source: https://github.com/cms-hls4ml/%{n}/archive/refs/tags/v%{realversion}.tar.gz
%define tag 1e9a692ccfa92cee5a87bbc94eb902b9f560870b
Source: git+https://github.com/cms-hls4ml/%{n}.git?obj=main/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz
Requires: hls4mlEmulatorExtras hls
BuildRequires: gmake

%prep
%setup -n %{n}-%{realversion}

%build
make %{?_smp_mflags} EMULATOR_EXTRAS=${HLS4MLEMULATOREXTRAS_ROOT} HLS_ROOT=${HLS_ROOT}

%install
make PREFIX=%{i} install
