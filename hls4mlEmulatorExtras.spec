### RPM external hls4mlEmulatorExtras 1.0
%define tag a599ccb0ef3afa2852f32dfa91b4faf8a3d606e1
%define branch main
%define github_user smuzaffar

Source: git+https://github.com/%{github_user}/root.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz

BuildRequires: gmake

%prep
%setup -n %{n}-%{realversion}

%build
make %{makeprocesses} 

%install
make PREFIX=%{i} install

