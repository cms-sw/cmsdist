### RPM external classlib 3.1.3
%define tag b2569c29126780017b48b96d324fe73a05573bc5
%define branch cms/%{realversion}
%define github_user cms-externals
Source: git+https://github.com/%{github_user}/%{n}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

Requires: pcre

%prep
%setup -n %{n}-%realversion

%build
# Update to get aarch64 and ppc64le
rm -f ./cfg/config.{sub,guess}
%get_config_guess ./cfg/config.guess
%get_config_sub ./cfg/config.sub
chmod +x ./cfg/config.{sub,guess}

./configure --prefix=%i           \
  --without-zlib --without-bz2lib \
  --without-lzma --without-lzo \
  --with-pcre-includes=$PCRE_ROOT/include \
  --with-pcre-libraries=$PCRE_ROOT/lib

perl -p -i -e 's|-lz | |;s|-lbz2| |;s|-lcrypto| |;s|-llzma||' Makefile
perl -p -i -e '
  s{-llzo2}{}g;
  !/^\S+: / && s{\S+LZO((C|Dec)ompressor|Constants|Error)\S+}{}g' \
 Makefile

make %makeprocesses CXXFLAGS="-Wno-error=extra -ansi -pedantic -W -Wall -Wno-long-long -Werror -Wno-cast-function-type"

%install
make %makeprocesses install
