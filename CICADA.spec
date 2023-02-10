### RPM external CICADA 1.0
%define tag 7b9dde083a78e75c539bf16741f4085eee8d9412
%define branch main
%define github_user smuzaffar

Source: git+https://github.com/%{github_user}/root.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz
Requires: hls4mlEmulatorExtras
BuildRequires: gmake

%prep
%setup -n %{n}-%{realversion}

%build
make %{makeprocesses} EMULATOR_EXTRAS=${HLS4MLEMULATOREXTRAS_ROOT}

%install
make PREFIX=%{i} install EMULATOR_EXTRAS=${HLS4MLEMULATOREXTRAS_ROOT}

