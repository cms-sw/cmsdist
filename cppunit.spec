### RPM external cppunit 1.12.1
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

# Update to detect aarch64 and ppc64le
rm -f ./config/config.{sub,guess}
curl -L -k -s -o ./config/config.sub 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD'
curl -L -k -s -o ./config/config.guess 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD'
chmod +x ./config/config.{sub,guess}

./configure --prefix=%i --disable-static
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
