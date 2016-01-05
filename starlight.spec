Name:		
Version:	
Release:	1%{?dist}
Summary:	

Group:		
License:	
URL:		
Source0:	http://cern.ch//service-spi/external/MCGenerators/distribution/%{n}/%{n}-%{realversion}-src.tgz

BuildRequires:	cmake
BuildRequires:	gmake
Requires: gfortran
Requires: clhep
Patch0: starlight-r193-p01

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
%doc



%changelog

