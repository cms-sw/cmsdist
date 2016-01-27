### RPM external gengetopt 2.22.6
Source: ftp://ftp.gnu.org/gnu/gengetopt/gengetopt-%{realversion}.tar.gz
Patch0: gengetopt-parallelbuild

BuildRequires: autotools

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx c++
%endif

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -O2 -std=c++14
%endif

%prep
%setup -q -n gengetopt-%{realversion}

%patch0 -p1 

# Regenerate build scripts
autoreconf -fiv

%build
CXX="$(which %{cms_cxx}) -fPIC"
CC="$(which gcc) -fPIC"
PLATF_CONF_OPTS="--enable-shared --disable-static"

# Only keep bin folder 
./configure $PLATF_CONF_OPTS \
            --disable-silent-rules \
	    --prefix=/tmp \
            --datarootdir=/tmp \
            --bindir=%{i} \
            CXX="$CXX" CC="$CC" CXXFLAGS="%{cms_cxxflags}" 

make %{makeprocesses}

%install
make install

