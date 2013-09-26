### RPM external libjpg 8b
%define mic %(case %cmsplatf in (*_mic_*) echo true;; (*) echo false;; esac)
%if "%mic" == "true"
Requires: icc
%endif
Source: http://www.ijg.org/files/jpegsrc.v%{realversion}.tar.gz

%prep
%setup -n jpeg-%realversion

%build
%if "%mic" == "true"
CXX="icpc -fPIC -mmic"  CC="icc -fPIC -mmic" ./configure --prefix=%{i} --enable-shared --disable-static  --host=x86_64-k1om-linux
%else
./configure --prefix=%{i} --enable-shared --disable-static
%endif

make %makeprocesses
%install
mkdir -p %{i}/lib
mkdir -p %{i}/bin
mkdir -p %{i}/include
mkdir -p %{i}/man/man1
make install

# Strip libraries, we are not going to debug them.
%define strip_files %i/lib
# Don't need archive libraries.
rm -f %i/lib/*.{l,}a
# Look up documentation online.
%define drop_files %i/{share,man}
