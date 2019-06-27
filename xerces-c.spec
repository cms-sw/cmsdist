### RPM external xerces-c 3.1.3
%define xercesv %(echo %{realversion} | tr . _)
Source: http://www-us.apache.org/dist//xerces/c/3/sources/xerces-c-%{realversion}.tar.gz 

%prep
%setup -n xerces-c-%{realversion}


%build
export XERCESCROOT=$PWD
cd $PWD/

# Update to detect aarch64 and ppc64le
rm -f ./config/config.{sub,guess}
curl -L -k -s -o ./config/config.sub 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD'
curl -L -k -s -o ./config/config.guess 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD'
chmod +x ./config/config.{sub,guess}

export VERBOSE=1
case %cmsplatf in
  osx108_*)
    # For OS X ("Mountain Lion") do not use Objective-C in C and C++ code.
    export CXXFLAGS="${CXXFLAGS} -DOS_OBJECT_USE_OBJC=0"
    export CFLAGS="${CXXFLAGS} -DOS_OBJECT_USE_OBJC=0"
  ;;
esac

./configure \
  --prefix=%{i} \
  --disable-dependency-tracking \
  --disable-rpath \
  --without-icu \
  --without-curl

make %{makeprocesses}

%install
export XERCESCROOT=$PWD

make install
# bla bla
