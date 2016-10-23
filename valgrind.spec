### RPM external valgrind 3.12.0
## INITENV SET VALGRIND_LIB %{i}/lib/valgrind
%define tag 19bc5aa976d728189c0eda5ca4bb2a50c63e1bf9
%define branch v3.12.0
%define github_user cms-externals
Source: git+https://github.com/%{github_user}/%{n}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

BuildRequires: autotools

%prep
%setup -n %{n}-%{realversion}

%build
case %{cmsplatf} in
  osx*)
    CFLAGS="-D__private_extern__=extern"
    ;;
  *_amd64_*|*_aarch64_*|*_ppc64le_*)
    CONF_OPTS="--enable-only64bit"
    ;;
esac

./autogen.sh
./configure --prefix=%{i} --without-mpicc --disable-static \
            ${CONF_OPTS} ${CFLAGS+CFLAGS=${CFLAGS}}
make %{makeprocesses}

%install
make install
%define strip_files %{i}/lib %{i}/bin/{cg_merge,no_op*,valgrind*}
%define drop_files %{i}/lib/valgrind/*.a %{i}/share

perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' $(grep -r -e "^#!.*perl.*" %{i} | cut -d: -f 1)
# I don't see how to make perl options work nicely with env, so drop the -w
# in these two scripts
perl -p -i -e 's|perl -w|perl|' %{i}/bin/callgrind_annotate
perl -p -i -e 's|perl -w|perl|' %{i}/bin/callgrind_control
