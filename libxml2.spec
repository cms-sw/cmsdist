### RPM external libxml2 2.6.23_CMS19
%define downloadv %(echo %realversion | cut -d"_" -f1)
Source: ftp://xmlsoft.org/%n/%n-%downloadv.tar.gz
%define closingbrace )
%define online %(case %cmsplatf in *onl_*_*%closingbrace echo true;; *%closingbrace echo false;; esac)

%if "%online" != "true"
Requires: zlib
%endif

%prep
%setup -n %n-%downloadv
%build
%if "%online" != "true"
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
