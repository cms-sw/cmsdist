### RPM external boost-build 2.0-m12-CMS18
# Override default realversion since they have a "-" in the realversion
%define realversion 2.0-m12
Source: http://superb-east.dl.sourceforge.net/sourceforge/boost/%{n}-%{realversion}.tar.bz2

%prep
%setup -n boost-build

%build
cd jam_src
case $(uname) in
  Darwin ) sh build.sh darwin ;;
  * )      sh build.sh gcc ;;
esac

%install
mkdir -p %i
cp -r jam_src/bin.* %i/bin
