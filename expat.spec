### RPM external expat 2.4.6
## INITENV +PATH LD_LIBRARY_PATH %{i}/lib64
%define uversion %(echo %realversion | sed -e 's/\\./_/g')
Source: https://github.com/libexpat/libexpat/releases/download/R_%{uversion}/%{n}-%{realversion}.tar.gz

BuildRequires: autotools
Requires: libbsd

%define drop_files %{i}/share

%prep
%setup -n %{n}-%{realversion}

%build
# Update to detect aarch64 and ppc64le
rm -f ./conftools/config.{sub,guess}
%get_config_sub ./conftools/config.sub
%get_config_guess ./conftools/config.guess
chmod +x ./conftools/config.{sub,guess}

./configure --prefix=%{i} --with-libbsd LDFLAGS="-L${LIBBSD_ROOT}/lib -L${LIBMD_ROOT}/lib" CFLAGS="-I${LIBBSD_ROOT}/include -I${LIBMD_ROOT}/include"
make %{makeprocesses} LDFLAGS="-L${LIBBSD_ROOT}/lib -L${LIBMD_ROOT}/lib" CFLAGS="-I${LIBBSD_ROOT}/include -I${LIBMD_ROOT}/include"

%install
make install
