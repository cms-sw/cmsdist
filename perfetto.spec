### RPM external perfetto 56.1
## INCLUDE cpp-standard

# The Perfetto C++ tracing SDK is published per release as a self-contained
# amalgamation (perfetto.h + perfetto.cc), with no dependencies beyond the C++
# standard library and pthread.
Source0: https://github.com/google/perfetto/releases/download/v%{realversion}/perfetto-cpp-sdk-src.zip

%prep
# The zip has no top-level directory; create one and unpack into it.
%setup -q -c -n %{n}-%{realversion}

%build
mkdir -p %{i}/lib %{i}/include
# Compile the amalgamation into a shared library (a single translation unit).
g++ -std=c++%{cms_cxx_standard} -O2 -fPIC -pthread -DNDEBUG -Wno-redundant-move \
    -shared -Wl,-soname,libperfetto.so \
    -o %{i}/lib/libperfetto.so perfetto.cc -lpthread

%install
cp -p perfetto.h %{i}/include/perfetto.h
