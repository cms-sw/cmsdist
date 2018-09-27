### RPM external libjpeg-turbo 1.5.3                                                                                                                                                                                                                          
## INITENV SETV LIBJPEG_TURBO_SOURCE %{source0}                                                                                                                                                                                                               
## INITENV SETV LIBJPEG_TURBO_STRIP_PREFIX %{source_prefix}                                                                                                                                                                                                   

%define source0 https://github.com/libjpeg-turbo/libjpeg-turbo/archive/%{realversion}.tar.gz
%define source_prefix %{n}-%{realversion}
Source: %{source0}

BuildRequires: nasm autotools gmake

%prep
%setup -n %{source_prefix}

%build
# Update to get AArch64                                                                                                                                                                                                                                       
rm -f ./config.{sub,guess}
curl -L -k -s -o ./config.sub 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD'
curl -L -k -s -o ./config.guess 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD'
chmod +x ./config.{sub,guess}

autoreconf -fiv

./configure \
  --prefix="%{i}" \
  --enable-shared \
  --disable-static \
  --with-jpeg8 \
  --disable-dependency-tracking

make %{makeprocesses}
%install
make install

%define strip_files %{i}/lib
%define drop_files %{i}/{share,man}
