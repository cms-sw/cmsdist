### RPM external libxml2 2.6.23-CMS3
Source: ftp://xmlsoft.org/%n/%n-%realversion.tar.gz

%if "%{?online_release:set}" != "set"
Requires: zlib
%endif

%prep
%setup -n %n-%realversion
%build
%if "%{?online_release:set}" != "set"
./configure --prefix=%i --with-zlib=$ZLIB_ROOT --without-python
%else
./configure --prefix=%i --with-zlib=/usr --without-python
%endif
make %makeprocesses
