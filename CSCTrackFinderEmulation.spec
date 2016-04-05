### RPM cms CSCTrackFinderEmulation 1.1
   
%define tag 10071ef27f2951e108cc13716a02590b58c3d1a9
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
