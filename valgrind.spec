### RPM external valgrind 3.12.99
## INITENV SET VALGRIND_LIB %{i}/lib/valgrind

# Exported from SVN at 16435 revision (4th June, 2017)
%define valgrindRevision 16435
%define valgrindBranch trunk
Source: svn://svn.valgrind.org/valgrind/%{valgrindBranch}?module=%{n}-%{valgrindRevision}&revision=%{valgrindRevision}&output=/%{n}-%{valgrindRevision}.tar.gz

BuildRequires: autotools

%prep
%setup -n %{n}-%{valgrindRevision}

%build
case %{cmsplatf} in
  osx*)
    CFLAGS="-D__private_extern__=extern"
    ;;
  *_amd64_*|*_aarch64_*|*_ppc64le_*|*_ppc64_*)
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
