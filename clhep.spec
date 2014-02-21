### RPM external clhep 2.1.3.1
%define mic %(case %cmsplatf in (*_mic_*) echo true;; (*) echo false;; esac)
%if "%mic" == "true"
Requires: icc
%endif
Source: http://proj-clhep.web.cern.ch/proj-clhep/DISTRIBUTION/distributions/%n-%realversion.tgz
Patch0: clhep-2.1.1.0-no-virtual-inline
Patch1: clhep-2.1.3.1-diagnostic-ignore-unused-variable

%if "%mic" != "true"
BuildRequires: cmake ninja
%endif

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx g++
%endif

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -std=c++0x
%endif

%prep
%setup -n %{realversion}/CLHEP
case %cmsplatf in
  osx*|*gcc4[789]*)
%patch0 -p3
  ;;
esac
%patch1 -p2

%build
rm -rf ../build
mkdir ../build
cd ../build

%if "%mic" == "true"
CXXFLAGS="-fPIC -mmic" cmake ../CLHEP \
  -DCMAKE_CXX_COMPILER="icpc" \
  -DCMAKE_CXX_FLAGS="-fPIC -mmic" \
  -DCMAKE_INSTALL_PREFIX:PATH="%i" \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo
make VERBOSE=1
%else
cmake ../CLHEP \
  -G Ninja \
  -DCMAKE_CXX_COMPILER="%cms_cxx" \
  -DCMAKE_CXX_FLAGS="%{cms_cxxflags}" \
  -DCMAKE_INSTALL_PREFIX:PATH="%i" \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo
ninja -v %{makeprocesses} -l $(getconf _NPROCESSORS_ONLN)
%endif

%install
cd ../build
%if "%mic" == "true"
make install
%else
ninja install
%endif

case $(uname) in Darwin ) so=dylib ;; * ) so=so ;; esac
rm %i/lib/libCLHEP-[A-Z]*-%realversion.$so

%post
%{relocateConfig}bin/Evaluator-config
%{relocateConfig}bin/Cast-config
%{relocateConfig}bin/GenericFunctions-config
%{relocateConfig}bin/Exceptions-config
%{relocateConfig}bin/RandomObjects-config
%{relocateConfig}bin/Geometry-config
%{relocateConfig}bin/Matrix-config
%{relocateConfig}bin/Random-config
%{relocateConfig}bin/RefCount-config
%{relocateConfig}bin/Units-config
%{relocateConfig}bin/Utility-config
%{relocateConfig}bin/Vector-config
%{relocateConfig}bin/clhep-config
