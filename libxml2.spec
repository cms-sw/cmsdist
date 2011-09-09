### RPM external libxml2 2.7.7
%define downloadv %(echo %realversion | cut -d"_" -f1)
Source: ftp://xmlsoft.org/%n/%n-%downloadv.tar.gz
%define online %(case %cmsplatf in (*onl_*_*) echo true;; (*) echo false;; esac)

%if "%online" != "true"
Requires: zlib
%endif

%prep
%setup -n %n-%downloadv
%build
%if "%online" != "true"
./configure --prefix=%i --with-zlib=$ZLIB_ROOT --without-python
#./configure --prefix=%i --with-zlib=$ZLIB_ROOT
%else
./configure --prefix=%i --with-zlib=/usr --without-python
#./configure --prefix=%i --with-zlib=/usr
%endif
make %makeprocesses
%install
make install
rm -rf %{i}/lib/pkgconfig
rm -rf %{i}/share/{man,doc,gtk-doc}
%post
%{relocateConfig}bin/xml2-config
%{relocateConfig}lib/libxml2.la
%{relocateConfig}lib/xml2Conf.sh
