### RPM external libjpeg-turbo 2.0.2
## INITENV SETV LIBJPEG_TURBO_SOURCE %{source0}
## INITENV SETV LIBJPEG_TURBO_STRIP_PREFIX %{source_prefix}

%define source0 https://github.com/libjpeg-turbo/libjpeg-turbo/archive/%{realversion}.tar.gz
%define source_prefix %{n}-%{realversion}
Source: %{source0}

BuildRequires: nasm autotools gmake cmake

%prep
%setup -n %{source_prefix}

%build
# Update to get AArch64

rm -f ./config.{sub,guess}
curl -L -k -s -o ./config.sub 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD'
curl -L -k -s -o ./config.guess 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD'
chmod +x ./config.{sub,guess}

cmake -DCMAKE_INSTALL_PREFIX=%{i} -DENABLE_SHARED=TRUE -DENABLE_STATIC=FALSE -DWITH_JPEG8=TRUE

make %{makeprocesses}
%install
make install

%define strip_files %{i}/lib
%define drop_files %{i}/{share,man}
