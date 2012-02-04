### RPM external xerces-c 2.8.0
%define xercesv %(echo %realversion | tr . _)
Source: http://archive.apache.org/dist/xml/xerces-c/sources/xerces-c-src_%xercesv.tar.gz 
Patch0: xerces-c-2.8.0-osx106

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
case %cmsos in
 slc*)
   ./runConfigure -P%i -plinux -cgcc -xg++ ;;
 osx*_amd64)
   ./runConfigure -P%i -b 64 -pmacosx -nnative -rnone -cgcc -xg++ ;;
 osx*_amd32)
   ./runConfigure -P%i -b 32 -pmacosx -nnative -rnone -cgcc -xg++ ;;
 *)
   exit 1
esac
make

%install
export XERCESCROOT=$PWD
cd src/xercesc
make install
