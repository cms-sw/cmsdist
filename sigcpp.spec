### RPM external sigcpp 3.2.0
Source: https://github.com/libsigcplusplus/libsigcplusplus/archive/refs/tags/%{realversion}.tar.gz

BuildRequires: cmake gmake

%prep
%setup -q -n libsigcplusplus-%{realversion}

%build
rm -rf ../build ; mkdir ../build ; cd ../build
cmake ../libsigcplusplus-%{realversion} \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_PREFIX="%{i}"
make %{makeprocesses}

%install
cd ../build
make install
# We remove pkg-config files for two reasons:
# * it's actually not required (macosx does not even have it).
# * rpm 4.8 adds a dependency on the system /usr/bin/pkg-config
#   on linux.
# In the case at some point we build a package that can be build
# only via pkg-config we have to think on how to ship our own
# version.
rm -rf %{i}/lib/pkgconfig
# Read documentation online.
%define drop_files %{i}/share
cp %{i}/lib/sigc++-3.0/include/sigc++config.h %{i}/include/sigc++-3.0/

%post
%{relocateConfig}lib/cmake/sigc++-3/*.cmake
