### RPM external tbb 44_20151115oss
Source: https://www.threadingbuildingblocks.org/sites/default/files/software_releases/source/%{n}%{realversion}_src.tgz

Patch0: tbb-cpp11-rvalue-ref-present

%prep
%setup -n tbb%{realversion}
%patch0 -p1

%build

make %makeprocesses

%install
install -d %i/lib
cp -r include %i/include
case %cmsplatf in 
  osx*) SONAME=dylib ;;
  *) SONAME=so ;;
esac
find build -name "*.$SONAME*" -exec cp {} %i/lib \; 
