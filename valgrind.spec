### RPM external valgrind 3.17.0
## INITENV SET VALGRIND_LIB %{i}/lib/valgrind
Source: https://sourceware.org/pub/valgrind/%{n}-%{realversion}.tar.bz2

BuildRequires: autotools gmake

%prep
%setup -n %{n}-%{realversion}

%build
CONF_OPTS="--enable-only64bit"
%ifos darwin
  CFLAGS="-D__private_extern__=extern"
%endif

./autogen.sh
./configure --prefix=%{i} --without-mpicc --disable-static ${CONF_OPTS}
make %{makeprocesses}

%install
make install
%define strip_files %{i}/libexec %{i}/bin/{cg_merge,no_op*,valgrind*}
%define drop_files %{i}/libexec/valgrind/*.a %{i}/share

perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' $(grep -r -e "^#!.*perl.*" %{i} | cut -d: -f 1)
# I don't see how to make perl options work nicely with env, so drop the -w
# in these two scripts
perl -p -i -e 's|perl -w|perl|' %{i}/bin/callgrind_annotate
perl -p -i -e 's|perl -w|perl|' %{i}/bin/callgrind_control
