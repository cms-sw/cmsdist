### RPM external tbb 44_20160526oss
Source: https://www.threadingbuildingblocks.org/sites/default/files/software_releases/source/tbb%{realversion}_src_0.tgz

Patch0: tbb-cpp11-rvalue-ref-present

%prep
%setup -n tbb%{realversion}
%patch0 -p1

%build

make %{makeprocesses} stdver=c++14 CXXFLAGS='-flifetime-dse=1'

%install
install -d %i/lib
cp -r include %i/include
case %cmsplatf in 
  osx*) SONAME=dylib ;;
  *) SONAME=so ;;
esac
find build -name "*.$SONAME*" -exec cp {} %i/lib \; 
