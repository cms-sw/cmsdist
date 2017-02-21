### RPM external libjpeg-turbo 1.3.1
Source: http://heanet.dl.sourceforge.net/project/%{n}/%{realversion}/%{n}-%{realversion}.tar.gz

BuildRequires: nasm

%prep
%setup -n %{n}-%{realversion}

%build
# Update to get AArch64
rm -f ./config.{sub,guess}
curl -L -k -s -o ./config.sub 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD'
curl -L -k -s -o ./config.guess 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD'
chmod +x ./config.{sub,guess}

./configure \
  --prefix=%{i} \
  --enable-shared \
  --disable-static \
  --with-jpeg8 \
  --disable-dependency-tracking

make %{makeprocesses}
%install
make install

%define strip_files %{i}/lib
%define drop_files %{i}/{share,man}
