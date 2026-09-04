### RPM external xgboost 1.7.5

BuildRequires: cmake
Source: git+https://github.com/dmlc/xgboost.git?obj=master/v%{realversion}&export=%{n}-%{realversion}&submodules=1&output=/%{n}-%{realversion}.tgz
Patch0: xgboost-arm-and-ppc

%prep
%setup -q -n %{n}-%{realversion}
%ifnarch x86_64
%patch0 -p1
%endif

%build
rm -rf ../build; mkdir ../build; cd ../build
cmake ../%{n}-%{realversion} \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_BUILD_TYPE=Release \
  -DUSE_CUDA=OFF

%install
cd ../build
make %{makeprocesses}
make install

%post
%{relocateConfig}lib64/pkgconfig/xgboost.pc
