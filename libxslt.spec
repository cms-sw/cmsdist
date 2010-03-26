### RPM external libxslt 1.1.26

# 64-bit version
Provides: libgcrypt.so.11()(64bit)
Provides: libgcrypt.so.11(GCRYPT_1.2)(64bit)
Provides: libgpg-error.so.0()(64bit)

Source: ftp://xmlsoft.org/%n/%n-%realversion.tar.gz

Requires: libxml2

%prep
%setup -n libxslt-%realversion
%build
./configure --prefix=%i --with-libxml-prefix=$LIBXML2_ROOT
make %makeprocesses
