### RPM external libxml2 2.6.23-CMS19
Source: ftp://xmlsoft.org/%n/%n-%realversion.tar.gz

Requires: zlib

%prep
%setup -n %n-%realversion
%build
%if "%cmsplatf" != "slc4onl_ia32_gcc346"
./configure --prefix=%i --with-zlib=$ZLIB_ROOT --without-python
%else
./configure --prefix=%i --with-zlib=/usr --without-python
%endif
make %makeprocesses
%post
%{relocateConfig}bin/xml2-config
%{relocateConfig}lib/libxml2.la
%{relocateConfig}lib/pkgconfig/libxml-2.0.pc
%{relocateConfig}lib/xml2Conf.sh
