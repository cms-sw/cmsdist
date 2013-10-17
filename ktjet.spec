### RPM external ktjet 1.06
%define mic %(case %cmsplatf in (*_mic_*) echo true;; (*) echo false;; esac)
%if "%mic" == "true"
Requires: icc
%endif
Source: http://www.hepforge.org/archive/ktjet/KtJet-%{realversion}.tar.gz
Patch1: ktjet-1.0.6-nobanner
Patch2: ktjet-1.0.6-mic
Requires: clhep

%define keep_archives true

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx g++
%endif

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -std=c++0x
%endif

%prep
%setup -n KtJet-%{realversion}
%patch1 -p1
%if "%mic" == "true"
%patch2 -p1
%endif

%build
%if "%mic" == "true"
CPPFLAGS=" -DKTDOUBLEPRECISION -fPIC %cms_cxxflags -mmic" CXX="icpc" ./configure --with-clhep=$CLHEP_ROOT --prefix=%{i} --host=x86_64-k1om-linux
%else
CPPFLAGS=" -DKTDOUBLEPRECISION -fPIC %cms_cxxflags" CXX="%cms_cxx" ./configure --with-clhep=$CLHEP_ROOT --prefix=%{i}
%endif
make
