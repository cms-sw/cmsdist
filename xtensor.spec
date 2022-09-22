### RPM external xtensor 0.24.1
Source: https://github.com/QuantStack/xtensor/archive/%{realversion}.tar.gz
BuildRequires: cmake
Requires: xtl

%prep
%setup -n %{n}-%{realversion}

%build

rm -rf ../build; mkdir ../build; cd ../build
cmake -DCMAKE_INSTALL_PREFIX=%{i} -DCMAKE_PREFIX_PATH=${XTL_ROOT} ../%{n}-%{realversion}
make %{makeprocesses}

%install
cd ../build
make install

%post
%{relocateConfig}lib64/pkgconfig/xtensor.pc
