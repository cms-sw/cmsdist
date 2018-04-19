### RPM external zlib_qat 1.2.8
Source: http://zlib.net/%{n}-%{realversion}.tar.gz

Patch0: zlib-1.2.8-qat
Patch1: zlib-clean

Provides: libicp_qa_al_s.so()(64bit)

%prep
%setup -n %{n}-%{realversion}
%patch0 -p0
%patch1 -p1

%build
export ICP_ROOT=/QAT/QAT1.6

# One could use the following macros for debugging:
#   -DQAT_TESTS_LOG -DQAT_DEBUG

case %{cmsplatf} in
   *_amd64_*|*_mic_*)
     CFLAGS="-fPIC -O3 -DUSE_MMAP -DUNALIGNED_OK -D_LARGEFILE64_SOURCE=1 -msse3" \
     ./configure --prefix=%{i}
     ;;
   *_armv7hl_*|*_aarch64_*|*_ppc64le_*)
     CFLAGS="-fPIC -O3 -DUSE_MMAP -DUNALIGNED_OK -D_LARGEFILE64_SOURCE=1" \
     ./configure --prefix=%{i}
     ;;
   *)
     %{cfgopts} ./configure --prefix=%{i}
     ;;
esac

make %{makeprocesses}

%install
export ICP_ROOT=/QAT/QAT1.6

make install

# Strip libraries, we are not going to debug them.
%define strip_files %{i}/lib
# Look up documentation online.
%define drop_files %{i}/share
