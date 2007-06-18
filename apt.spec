### RPM external apt 0.5.15lorg3.2
Source:  http://apt-rpm.org/releases/%n-%v.tar.bz2
Patch0: apt-rpm449
Requires: libxml2 beecrypt rpm zlib bz2lib
%if "%(echo %{cmsos} | cut -d_ -f 2 | sed -e 's|.*64.*|64|')" == "64"
%define libdir lib64
%else
%define libdir lib
%endif

%prep
%setup -n %n-%{realversion}
%patch0 -p0
%build
export CPPFLAGS="-I$BEECRYPT_ROOT/include -I$RPM_ROOT/include -I$RPM_ROOT/include/rpm"
export LDFLAGS="-L$BEECRYPT_ROOT/%{libdir} -L$RPM_ROOT/%{libdir}"
export LIBDIR="$LIBS"
export LIBXML2_CFLAGS="-I$LIBXML2_ROOT/include/libxml2 -I$BEECRYPT_ROOT/include -I$RPM_ROOT/include"
export LIBXML2_LIBS="-lxml2 -L$LIBXML2_ROOT/lib -L$BEECRYPT_ROOT/%{libdir} -L$RPM_ROOT/%{libdir}"

./configure --prefix=%{i} --exec-prefix=%{i} \
                            --disable-nls \
                            --disable-dependency-tracking \
                            --without-libintl-prefix \
                            --disable-rpath
make %makeprocesses
%install
make install
mkdir -p %{i}/etc/profile.d
(echo "#!/bin/sh"; \
 echo "source $RPM_ROOT/etc/profile.d/init.sh"; \
 echo "source $LIBXML2_ROOT/etc/profile.d/init.sh" ) > %{i}/etc/profile.d/dependencies-setup.sh
(echo "#!/bin/tcsh"; \
 echo "source $RPM_ROOT/etc/profile.d/init.csh"; \
 echo "source $LIBXML2_ROOT/etc/profile.d/init.csh" ) > %{i}/etc/profile.d/dependencies-setup.csh
%post
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh
