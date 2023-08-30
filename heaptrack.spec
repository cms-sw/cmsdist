### RPM external heaptrack 1.4.0
Source: https://github.com/KDE/heaptrack/archive/refs/tags/v%{realversion}.tar.gz
Requires: boost libunwind zstd
BuildRequires: cmake
%prep
%setup -n %{n}-%{realversion}

%build
mkdir -p %i
rm -rf ../build; mkdir ../build; cd ../build

cmake ../%{n}-%{realversion} \
   -DCMAKE_INSTALL_PREFIX=%i -DCMAKE_VERBOSE_MAKEFILE=TRUE \
   -DCMAKE_CXX_FLAGS_RELWITHDEBINFO="-g -O3" \
   -DCMAKE_PREFIX_PATH="$LIBUNWIND_ROOT;$BOOST_ROOT;$ZSTD_ROOT"
make DEBUG=1 VERBOSE=1 %makeprocesses 

%install
cd ../build
make %makeprocesses install
%define drop_files %i/share/man
