### RPM external cpu_features 0.7.0

Source: https://github.com/google/cpu_features/archive/refs/tags/v%{realversion}.tar.gz
BuildRequires: gmake cmake

%prep
%setup -n %{n}-%{realversion}

%build
cmake -S. -Bbuild \
    -DBUILD_TESTING=OFF \
    -DBUILD_SHARED_LIBS=ON \
    -DCMAKE_INSTALL_PREFIX:STRING=%{i}

%install
cd build
make install
