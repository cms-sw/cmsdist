### RPM external clhep 2.3.4.2

%define tag 03bdb22fe139303b43ca834a641f451f8e79bbcf
%define branch cms/v%{realversion}
%define github_user cms-externals
Source: git+https://github.com/%github_user/%{n}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

BuildRequires: cmake ninja

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx g++
%endif

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -std=c++0x
%endif

%prep
%setup -n %{n}-%{realversion}

%build
rm -rf ../build
mkdir ../build
cd ../build

cmake ../%{n}-%{realversion} \
  -G Ninja \
  -DCMAKE_CXX_COMPILER="%cms_cxx" \
  -DCMAKE_CXX_FLAGS="%{cms_cxxflags}" \
  -DCMAKE_INSTALL_PREFIX:PATH="%i" \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo

ninja -v %{makeprocesses} -l $(getconf _NPROCESSORS_ONLN)

%install
cd ../build
ninja install

case $(uname) in Darwin ) so=dylib ;; * ) so=so ;; esac
rm -f %i/lib/libCLHEP-[A-Z]*-%realversion.$so

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
