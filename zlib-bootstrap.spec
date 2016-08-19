### RPM external zlib-bootstrap 1.2.8
Source: http://zlib.net/zlib-%{realversion}.tar.gz

%prep
%setup -n zlib-%{realversion}

%build

case %{cmsplatf} in
   *_amd64_gcc4[56789]*|*_mic_* )
     CFLAGS="-fPIC -O3 -DUSE_MMAP -DUNALIGNED_OK -D_LARGEFILE64_SOURCE=1 -msse3" \
     ./configure --prefix=%{i}
     ;;
   *_armv7hl_gcc4[56789]* )
     CFLAGS="-fPIC -O3 -DUSE_MMAP -DUNALIGNED_OK -D_LARGEFILE64_SOURCE=1" \
     ./configure --prefix=%{i}
     ;;
   * )
     ./configure --prefix=%{i}
     ;;
esac

make %{makeprocesses}

# Strip libraries, we are not going to debug them.
%define strip_files %{i}/lib
# Look up documentation online.
%define drop_files %{i}/share
