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
curl -L -k -s -o ./cfg/config.sub 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD'
curl -L -k -s -o ./cfg/config.guess 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD'
chmod +x ./cfg/config.{sub,guess}

./configure --prefix=%i                         \
  --with-pcre-includes=$PCRE_ROOT/include       \
  --with-pcre-libraries=$PCRE_ROOT/lib

perl -p -i -e '
  s{-llzo2}{}g;
  !/^\S+: / && s{\S+LZO((C|Dec)ompressor|Constants|Error)\S+}{}g' \
 Makefile

make %makeprocesses CXXFLAGS="-Wno-error=extra -ansi -pedantic -W -Wall -Wno-long-long -Werror"

%install
make %makeprocesses install
