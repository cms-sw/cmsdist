### RPM external zlib 1.3.1
## INCLUDE microarch_flags
Source: https://github.com/madler/zlib/archive/refs/tags/v%{realversion}.tar.gz
BuildRequires: gmake

%prep
%setup -n zlib-%{realversion}

%build

CONF_FLAGS="-fPIC -O3 -DUSE_MMAP -DUNALIGNED_OK -D_LARGEFILE64_SOURCE=1 %{selected_microarch}"
CFLAGS="${CONF_FLAGS}" ./configure --prefix=%{i}

make %{makeprocesses}

# Strip libraries, we are not going to debug them.
%define strip_files %{i}/lib
# Look up documentation online.
%define drop_files %{i}/share
