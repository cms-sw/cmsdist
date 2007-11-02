### RPM external openssl 0.9.7d-CMS18
Source: http://www.openssl.org/source/%n-%realversion.tar.gz

%prep
%setup -n %n-%{realversion}

%build
./config --prefix=%i shared
case $(uname)-$(uname -m) in
  Darwin*)
    perl -p -i -e 's|-compatibility_version.*|-compatibility_version \${SHLIB_MAJOR}.\${SHLIB_MINOR} \\|' Makefile.ssl
esac

make
%install
make install
perl -p -i -e "s|^#!.*perl|#!/usr/bin/env perl|" %{i}/ssl/misc/CA.pl %{i}/ssl/misc/der_chop %{i}/bin/c_rehash
#
# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=%n version=%v>
<lib name=ssl>
<lib name=crypto>
<client>
 <Environment name=OPENSSL_BASE default="%i"></Environment>
 <Environment name=INCLUDE default="$OPENSSL_BASE/include"></Environment>
 <Environment name=LIBDIR  default="$OPENSSL_BASE/lib"></Environment>
</client>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n
