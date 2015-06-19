### RPM external expat 2.0.1
## INITENV +PATH LD_LIBRARY_PATH %{i}/lib64
Source: http://downloads.sourceforge.net/project/expat/%n/%realversion/expat-%realversion.tar.gz
Provides: libc.so.6()(64bit)
Provides: libc.so.6(GLIBC_2.2.5)(64bit)  

%prep
%setup -n %n-%{realversion}

%build
./configure --prefix=%{i} 
make %{makeprocesses}
make install

%install
%define drop_files %i/man

%post
find $RPM_INSTALL_PREFIX/%{pkgrel}/lib* -name "*.la" -exec perl -p -i -e "s|%{instroot}|$CMS_INSTALL_PREFIX|g" {} \;
