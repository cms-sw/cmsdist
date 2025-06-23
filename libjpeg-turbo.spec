### RPM external libjpeg-turbo 1.3.1
Source: http://heanet.dl.sourceforge.net/project/%{n}/%{realversion}/%{n}-%{realversion}.tar.gz

BuildRequires: nasm

%prep
%setup -n %{n}-%{realversion}

%build
# Update to get AArch64
rm -f ./config.{sub,guess}
%get_config_sub ./config.sub
%get_config_guess ./config.guess
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
