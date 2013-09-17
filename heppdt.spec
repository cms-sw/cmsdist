### RPM external heppdt 3.03.00
%define mic %(case %cmsplatf in (*_mic_*) echo true;; (*) echo false;; esac)
%if "%mic" == "true"
Requires: icc
%endif
Source: http://lcgapp.cern.ch/project/simu/HepPDT/download/HepPDT-%{realversion}.tar.gz
Patch1: heppdt-2.03.00-nobanner
Patch2: heppdt-3.03.00-silence-debug-output 
%define keep_archives yes

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx g++
%endif

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -O2 -std=c++0x
%endif

%prep
%setup -q -n HepPDT-%{realversion}
%patch1 -p1
%patch2 -p1

case %{cmsplatf} in
   *_mic_* )
    MY_SHFLAGS='-fPIC -DPIC' MY_SHLINK=-shared MY_SHNAME=-Wl,-soname, SHEXT=so AR='ar cru'  CXX="icpc -fPIC -mmic"  CC="icc -fPIC -mmic" CXXFLAGS="%cms_cxxflags" ./configure  --prefix=%{i} --host=x86_64-k1om-linux
     ;;
   * )
     CXX="%cms_cxx" CXXFLAGS="%cms_cxxflags" ./configure  --prefix=%{i}
     ;;
esac

%build
make 

%install
make install
