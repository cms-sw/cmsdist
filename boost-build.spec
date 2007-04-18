### RPM external boost-build 2.0-m10
Requires: gcc-wrapper
Source: http://dl.sourceforge.net/sourceforge/boost/boost-build-%v.tar.bz2 
%prep
%setup -n boost-build

%build
## IMPORT gcc-wrapper
cd jam_src
case $(uname) in
  Darwin ) sh build.sh darwin ;;
  * )      sh build.sh gcc ;;
esac

%install
mkdir -p %i
cp -r jam_src/bin.* %i/bin
