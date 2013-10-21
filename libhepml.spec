### RPM external libhepml 0.2.1
%define mic %(case %cmsplatf in (*_mic_*) echo true;; (*) echo false;; esac)
%if "%mic" == "true"
Requires: icc
%endif
Source: http://mcdb.cern.ch/distribution/api/%{n}-%{realversion}.tar.gz
Patch0: libhepml-0.2.1-gcc43
Patch1: libhepml-0.2.1-leopard

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx g++
%endif

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -O2 -std=c++0x
%endif

%prep
%setup -q -n %{n}-%{realversion}
%patch0 -p2
case %cmsplatf in
  osx*)
%patch1 -p1
  ;;
esac

%build
cd src

%if "%mic" == "true"
sed -ibak "s/\(^CC *= \)\(.*\)/\1icc/g;s/\(^CXX *= \)\(.*\)/\1icpc/g;s/\(^CXXFLAGS *= \)\(.*\)/\1\2 %cms_cxxflags -mmic/g;s/\(^CFLAGS *= \)\(.*\)/\1\2 -mmic/g" Makefile
sed -ibak "s/\(^LINK *= \)\(.*\)/\1icpc/g;s/\(^LFLAGS *= \)\(.*\)/\1\2 -mmic/g" Makefile
%else
sed -ibak "s/\(^CXX *= \)\(.*\)/\1%cms_cxx/g;s/\(^CXXFLAGS *= \)\(.*\)/\1\2 %cms_cxxflags/g" Makefile
%endif

make
mv *.so ../lib/.

%install
tar -c lib interface | tar -x -C %i
