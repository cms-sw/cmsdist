### RPM external libzip 1.11.4
Source: git+https://github.com/nih-at/libzip.git?obj=main/v%{realversion}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
Requires: zlib zstd
BuildRequires: cmake

%prep
%setup -n %{n}-%{realversion}

%build
rm -rf build && mkdir build
cmake -S . -B build \
  -DCMAKE_INSTALL_PREFIX=%{i}
cmake --build build %{makeprocesses}

%install
cmake --install build
