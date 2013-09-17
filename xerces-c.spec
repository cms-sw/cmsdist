### RPM external xerces-c 2.8.0
%define xercesv %(echo %realversion | tr . _)
%define mic %(case %cmsplatf in (*_mic_*) echo true;; (*) echo false;; esac)
%if "%mic" == "true"
Requires: icc
%endif
Source: http://archive.apache.org/dist/xml/xerces-c/sources/xerces-c-src_%xercesv.tar.gz 
Patch0: xerces-c-2.8.0-osx106
Patch1: xerces-c-2.8.0-fix-narrowing-conversion
Patch2: xerces-c-2.8.0-mic

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
  *_mic_*)
%patch2 -p1
  ;;
esac

%patch1 -p1

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

case %{cmsplatf} in
  *_mic_*)
   ./runConfigure -P%{i} -plinux -c 'icc -fPIC -mmic' -x 'icpc -fPIC -mmic' -C --host=x86_64-k1om-linux ;;
  slc*)
    ./runConfigure -P%{i} -plinux -cgcc -x%{cms_cxx} ;;
  osx*)
    ./runConfigure -P%{i} -b 64 -pmacosx -nnative -rnone -cgcc -x%{cms_cxx} ;;
  *armv7*)
    ./runConfigure -P%{i} -b 32 -plinux -cgcc -x%{cms_cxx} ;;
  *)
    echo "Unsupported configuration. Please modify SPEC file accordingly."
    exit 1
esac

make

%install
export XERCESCROOT=$PWD
cd src/xercesc
make install
