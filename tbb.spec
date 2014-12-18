### RPM external tbb 43_20141023oss
Source: https://www.threadingbuildingblocks.org/sites/default/files/software_releases/source/%{n}%{realversion}_src.tgz

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx g++
%endif

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -std=c++0x
%endif

%prep
%setup -n tbb%{realversion}

%build

CXX="%cms_cxx" CXXFLAGS="%cms_cxxflags" make %makeprocesses

%install
install -d %i/lib
cp -r include %i/include
case %cmsplatf in 
  slc*) SONAME=so ;;
  osx*) SONAME=dylib ;;
esac
find build -name "*.$SONAME*" -exec cp {} %i/lib \; 
