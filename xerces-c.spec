### RPM external xerces-c 2.7.0-XXXX
%define xercesv %(echo %realversion | tr . _)
Source: http://www.apache.org/dist/xml/xerces-c/source/xerces-c-src_%xercesv.tar.gz

%prep
%setup -n xerces-c-src_%xercesv

%build
export XERCESCROOT=$PWD
cd $PWD/src/xercesc
case $(uname) in
 Linux )
   ./runConfigure -P%i -plinux -cgcc -xg++ ;;
 Darwin )
   ./runConfigure -P%i -pmacosx -cgcc -xg++ ;;
esac
make

%install
export XERCESCROOT=$PWD
cd src/xercesc
make install
