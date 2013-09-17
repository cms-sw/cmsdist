### RPM external expat 2.0.1
## INITENV +PATH LD_LIBRARY_PATH %{i}/lib64
%define mic %(case %cmsplatf in (*_mic_*) echo true;; (*) echo false;; esac)
%if "%mic" == "true"
Requires: icc
%endif
Source: http://downloads.sourceforge.net/project/expat/%n/%realversion/expat-%realversion.tar.gz
Provides: libc.so.6()(64bit)
Provides: libc.so.6(GLIBC_2.2.5)(64bit)  

%prep
%setup -n %n-%{realversion}

%build
case %{cmsplatf} in
   *_mic_* )
     CXX="icpc -fPIC -mmic"  CC="icc -fPIC -mmic" ./configure --prefix=%{i} --host=x86_64-k1om-linux
     ;;
   * )
     ./configure --prefix=%{i}
     ;;
esac
make 
make install

%install

%post
find $RPM_INSTALL_PREFIX/%{pkgrel}/lib* -name "*.la" -exec perl -p -i -e "s|%{instroot}|$CMS_INSTALL_PREFIX|g" {} \;
