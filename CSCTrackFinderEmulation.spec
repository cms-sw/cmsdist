### RPM external CSCTrackFinderEmulation 0.1

%define tag 788fae84686f1214e77510a2b22988080f4ea6c1
%define branch master
%define github_user cms-externals
Source: git+https://github.com/%github_user/%{n}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

%prep
%setup -q -n %{n}-%{realversion}

%build
make -j %{makeprocesses}

%install
make install
cp -r %{_builddir}/%{n}-%{realversion}/installDir/* %{i}
