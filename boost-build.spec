### RPM external boost-build 2.0.m12-CMS19
# Override default realversion since they have a "-" in the realversion
%define realversion 2.0-m12
Source: http://superb-east.dl.sourceforge.net/sourceforge/boost/%{n}-%{realversion}.tar.bz2
# Per http://svn.boost.org/trac/boost/ticket/977, for gcc422 problem
Patch1: boost-build-2.0-m12-gcc422-no-strict-aliasing

%prep
%setup -n boost-build
%if "%cmsplatf" == "slc4_ia32_gcc422"
%patch1 -p1
%endif

%build
cd jam_src
case $(uname) in
  Darwin ) sh build.sh darwin ;;
  * )      sh build.sh gcc ;;
esac

%install
mkdir -p %i
cp -r jam_src/bin.* %i/bin
