### RPM external tbb 44_20160316oss
Source: https://www.threadingbuildingblocks.org/sites/default/files/software_releases/source/%{n}%{realversion}_src.tgz

Patch0: tbb-cpp11-rvalue-ref-present


%prep
%setup -n tbb%{realversion}
%patch0 -p1

%build

%ifos darwin
CXX=g++ CXXFLAGS=-std=c++14 make %makeprocesses
%else
make %makeprocesses
%endif

%install
install -d %i/lib
cp -r include %i/include
case %cmsplatf in 
  osx*) SONAME=dylib ;;
  *) SONAME=so ;;
esac
find build -name "*.$SONAME*" -exec cp {} %i/lib \; 
