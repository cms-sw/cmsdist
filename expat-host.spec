### RPM external expat-host 2.0.1
## INITENV +PATH LD_LIBRARY_PATH %{i}/lib64
Source: http://downloads.sourceforge.net/project/expat/expat/%realversion/expat-%realversion.tar.gz
Provides: libc.so.6()(64bit)
Provides: libc.so.6(GLIBC_2.2.5)(64bit)  

%prep
%setup -n expat-%{realversion}

%build
./configure --prefix=%{i}
make 
make install

%install

%post
find $RPM_INSTALL_PREFIX/%{pkgrel}/lib* -name "*.la" -exec perl -p -i -e "s|%{instroot}|$CMS_INSTALL_PREFIX|g" {} \;
