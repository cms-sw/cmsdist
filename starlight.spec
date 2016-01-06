Release:	1%{?dist}
Requires: clhep gfortran

%define branch cms/%{realversion}
%define github_user cms-externals
Source0:	git+http://github.com/%github_user/%{n}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

BuildRequires:	cmake

%define keep_archives true

%description


%prep
%setup -q -n %{n}/%{realversion}

%patch0 -p1

%build
%configure
make %{?_smp_mflags}


%install
cmake <path-to-starlight-source> -DENABLE_DPMJET=on
make


%files



%changelog

