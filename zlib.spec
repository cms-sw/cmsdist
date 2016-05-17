### RPM external zlib 1.2.8
Source: http://zlib.net/%{n}-%{realversion}.tar.gz

%prep
%setup -n %{n}-%{realversion}

%build
%if "%{cmscompiler}" == "icc"
%define cfgopts CC="icc -fPIC"
%else
%define cfgopts %{nil}
%endif

case %{cmsplatf} in
   *_amd64_*|*_mic_*)
     CFLAGS="-fPIC -O3 -DUSE_MMAP -DUNALIGNED_OK -D_LARGEFILE64_SOURCE=1 -msse3" \
     ./configure --prefix=%{i}
     ;;
   *_armv7hl_*|*_aarch64_*|*_ppc64le_*|*_ppc64_*)
     CFLAGS="-fPIC -O3 -DUSE_MMAP -DUNALIGNED_OK -D_LARGEFILE64_SOURCE=1" \
     ./configure --prefix=%{i}
     ;;
   *)
     %{cfgopts} ./configure --prefix=%{i}
     ;;
esac

make %{makeprocesses}

# Strip libraries, we are not going to debug them.
%define strip_files %{i}/lib
# Look up documentation online.
%define drop_files %{i}/share
