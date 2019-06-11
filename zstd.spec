### RPM external zstd 1.4.0
## INITENV SETV ZSTD_SOURCE %{source0}
## INITENV SETV ZSTD_STRIP_PREFIX %{source_prefix}

%define source0 https://github.com/facebook/zstd/releases/download/v%{realversion}/zstd-%{realversion}.tar.gz
%define source_prefix %{n}-%{realversion}
Source: %{source0}

BuildRequires: gmake cmake

%prep
%setup -n %{source_prefix}

%build
# Update to get AArch64

rm -f ./config.{sub,guess}
curl -L -k -s -o ./config.sub 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD'
curl -L -k -s -o ./config.guess 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD'
chmod +x ./config.{sub,guess}

cmake build/cmake \
 -DZSTD_BUILD_CONTRIB:BOOL=OFF \
 -DZSTD_BUILD_STATIC:BOOL=OFF \
 -DZSTD_BUILD_TESTS:BOOL=OFF \
 -DCMAKE_BUILD_TYPE=Release \
 -DZSTD_BUILD_PROGRAMS:BOOL=OFF \
 -DZSTD_LEGACY_SUPPORT:BOOL=OFF \
 -DCMAKE_INSTALL_PREFIX:STRING=%{i} \
 -DCMAKE_INSTALL_LIBDIR:STRING=lib \
 -Dzstd_VERSION:STRING=%{realversion}

make %{makeprocesses}

%install

make install

