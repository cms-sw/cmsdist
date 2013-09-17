### RPM external cppunit 1.12.1
%define mic %(case %cmsplatf in (*_mic_*) echo true;; (*) echo false;; esac)
%if "%mic" == "true"
Requires: icc
%endif
Source0: http://switch.dl.sourceforge.net/sourceforge/%n/%n-%realversion.tar.gz
Source1: CppUnit_testdriver_cpp

%prep
%setup -n %n-%realversion

%build
case %cmsplatf in
    osx* ) perl -p -i -e 's|rm(.*)conftest|rm -fr $1 conftest|g' configure \
                                                                 aclocal.m4 \
						                 libtool \
						               	 config/ltmain.sh
    ;;
    slc*|fc* )
       # Ugly hack to force -ldl to be linked, which for some reason is
       # not currently happening via configure
       perl -p -i -e 's|LIBS.*LIBS.*lm|LIBS="$LIBS -lm -ldl|' configure
    ;;
esac
%if "%mic" == "true"
CXX="icpc -fPIC -mmic"  CC="icc -fPIC -mmic" ./configure --prefix=%i --disable-static --host=x86_64-k1om-linux
%else
./configure --prefix=%i --disable-static
%endif
make %makeprocesses
%install
make install
cp %_sourcedir/CppUnit_testdriver_cpp %i/include/CppUnit_testdriver.cpp
# We remove pkg-config files for two reasons:
# * it's actually not required (macosx does not even have it).
# * rpm 4.8 adds a dependency on the system /usr/bin/pkg-config 
#   on linux.
# In the case at some point we build a package that can be build
# only via pkg-config we have to think on how to ship our own
# version.
rm -rf %i/lib/pkgconfig
# Remove unneded files
rm -rf %i/lib/*.{l,}a
# Read documentation online
%define drop_files %i/share

%post
%{relocateConfig}/bin/cppunit-config
