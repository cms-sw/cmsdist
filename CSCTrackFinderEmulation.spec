### RPM cms CSCTrackFinderEmulation 1.0
   
%define tag 2165a0914634bd792386cae47ef07183aaa975f4
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
