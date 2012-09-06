### RPM external xerces-c 2.8.0
%define xercesv %(echo %realversion | tr . _)
Source: http://archive.apache.org/dist/xml/xerces-c/sources/xerces-c-src_%xercesv.tar.gz 
Patch0: xerces-c-2.8.0-osx106

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx g++
%endif

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -std=c++0x
%endif

%prep
%setup -n xerces-c-src_%xercesv

case %cmsplatf in
  osx*)
%patch0 -p1
  ;;
esac

%build
export XERCESCROOT=$PWD
cd $PWD/src/xercesc

export CXXFLAGS="%cms_cxxflags"
export VERBOSE=1

case %cmsplatf in
  osx108_*)
    # For OS X ("Mountain Lion") do not use Objective-C in C and C++ code.
    export CXXFLAGS="${CXXFLAGS} -DOS_OBJECT_USE_OBJC=0"
    export CFLAGS="${CXXFLAGS} -DOS_OBJECT_USE_OBJC=0"
  ;;
esac

case %cmsos in
 slc*)
   ./runConfigure -P%i -plinux -cgcc -x%cms_cxx ;;
 osx*_amd64)
   ./runConfigure -P%i -b 64 -pmacosx -nnative -rnone -cgcc -x%cms_cxx ;;
 osx*_amd32)
   ./runConfigure -P%i -b 32 -pmacosx -nnative -rnone -cgcc -x%cms_cxx ;;
 *)
   exit 1
esac
make

%install
export XERCESCROOT=$PWD
cd src/xercesc
make install
