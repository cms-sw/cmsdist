### RPM external zlib 1.2.13
%define git_repo madler
%define git_branch master
%define git_commit v%{realversion}
Source0: git://github.com/%{git_repo}/zlib.git?obj=%{git_branch}/%{git_commit}&export=zlib-%{realversion}&output=/zlib-%{realversion}.tgz

%prep
%setup -n zlib-%{realversion}

%build

CONF_FLAGS="-fPIC -O3 -DUSE_MMAP -DUNALIGNED_OK -D_LARGEFILE64_SOURCE=1"
%ifarch x86_64
CONF_FLAGS="${CONF_FLAGS} -msse3"
%endif
CFLAGS="${CONF_FLAGS}" ./configure --prefix=%{i}

make %{makeprocesses}

# Strip libraries, we are not going to debug them.
%define strip_files %{i}/lib
# Look up documentation online.
%define drop_files %{i}/share
