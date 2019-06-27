### RPM cms CSCTrackFinderEmulation 1.2
%define tag 8c0287fde4739d96fd3fd4a03e5ce5e6b986052e
%define branch cms/CMSSW_8_1_X
%define github_user cms-externals
Source: git+https://github.com/%github_user/%{n}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
 
%prep
%setup -q -n %{n}-%{realversion}

%build
make %{makeprocesses}

%install
make install
cp -r %{_builddir}/%{n}-%{realversion}/installDir/* %{i}
# bla bla
