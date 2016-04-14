### RPM external xerces-c 2.8.0
%define xercesv %(echo %realversion | tr . _)
Source: http://archive.apache.org/dist/xml/xerces-c/sources/xerces-c-src_%xercesv.tar.gz 
Patch0: xerces-c-2.8.0-osx106
Patch1: xerces-c-2.8.0-fix-narrowing-conversion

%prep
%setup -n xerces-c-src_%xercesv

case %cmsplatf in
  osx*)
%patch0 -p1
  ;;
esac

%patch1 -p1

%build
export XERCESCROOT=$PWD
cd $PWD/src/xercesc

# Update to detect aarch64 and ppc64le
rm -f ./config.{sub,guess}
curl -L -k -s -o ./config.sub 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD'
curl -L -k -s -o ./config.guess 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD'
chmod +x ./config.{sub,guess}

export VERBOSE=1

case %cmsplatf in
  osx108_*)
    # For OS X ("Mountain Lion") do not use Objective-C in C and C++ code.
    export CXXFLAGS="${CXXFLAGS} -DOS_OBJECT_USE_OBJC=0"
    export CFLAGS="${CXXFLAGS} -DOS_OBJECT_USE_OBJC=0"
  ;;
esac

case %{cmsplatf} in
  slc*_amd64_*|fc*_amd64_*)
    ./runConfigure -P%{i} -plinux -cgcc -xg++ ;;
  *_aarch64_*|*_ppc64le_*)
    ./runConfigure -P%{i} -b 64 -plinux -cgcc -xg++ ;;
  osx*)
    ./runConfigure -P%{i} -b 64 -pmacosx -nnative -rnone -cgcc -xg++ ;;
  *)
    echo "Unsupported configuration. Please modify SPEC file accordingly."
    exit 1
esac

make

%install
export XERCESCROOT=$PWD
cd src/xercesc
make install
