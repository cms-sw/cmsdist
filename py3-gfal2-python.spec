### RPM external py3-gfal2-python 1.11.0.post3
## IMPORT build-with-pip3
BuildRequires: cmake boost175py3
Provides: libgfal2.so.2()(64bit)
Provides: libgfal_transfer.so.2()(64bit)
Provides: libglib-2.0.so.0()(64bit)
Provides: libboost_python38.so.1.75.0()(64bit)

Patch0: py3-gfal2
%define PipPreBuild export Boost_LIBRARYDIR=${BOOST175PY3_ROOT}/lib ; export CXXFLAGS="-I${BOOST175PY3_ROOT}/include"
#define PipBuildOptionsPy3 --global-option="--without=docs" --global-option="--without=python2"
