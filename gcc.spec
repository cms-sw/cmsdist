### RPM external gcc 3.4.5-CMS1
## INITENV +PATH LD_LIBRARY_PATH %i/lib/32
## BUILDIF case $(uname):$(uname -p) in Linux:i*86 ) true ;; Linux:x86_64 ) true ;;  Linux:ppc64 ) false ;; Darwin:* ) false ;; * ) true ;; esac
%define realVersion %(echo %v | cut -d- -f1)
Source: ftp://ftp.fu-berlin.de/unix/gnu/%n/%n-%realVersion/%n-%realVersion.tar.bz2
%define cpu %(echo %cmsplatf | cut -d_ -f2)

%prep
%setup -q -n %{n}-%{realVersion}

%build
# FIXME: --enable-__cxa_atexit can't be used with gcc 3.2.3 on RH 7.3,
# enabling it causes qt's uic to die with segmentation violation half
# way down the build of qt (projecsettings.ui or something like that;
# not the first or only call to uic).  Disabling the flag removes the
# issue, so clearly the option does not work correctly on this
# platform combination.
mkdir -p obj
cd obj

if [ "`echo %v | cut -d. -f 1`" == "3" ]
then
../configure --prefix=%i --enable-languages=c,c++,f77 \
    --enable-shared # --enable-__cxa_atexit
else
../configure --prefix=%i --enable-languages=c,c++ \
    --enable-shared # --enable-__cxa_atexit
fi
make %makeprocesses bootstrap

%install
cd obj && make install

ln -s gcc %i/bin/cc

%post

mkdir $RPM_INSTALL_PREFIX/%{pkgrel}/bin.orig

for exe in `ls $RPM_INSTALL_PREFIX/%{pkgrel}/bin`; do
mv $RPM_INSTALL_PREFIX/%{pkgrel}/bin/${exe} $RPM_INSTALL_PREFIX/%{pkgrel}/bin.orig/${exe}
cat << \EOF  | sed -e "s|\@EXEC\@|$RPM_INSTALL_PREFIX/%{pkgrel}/bin.orig/${exe}|g" > $RPM_INSTALL_PREFIX/%{pkgrel}/bin/$exe
#!/bin/sh
@EXEC@ "$@" -m32 -Wa,--32
EOF
chmod +x $RPM_INSTALL_PREFIX/%{pkgrel}/bin/$exe
done


%{relocateConfig}lib/libg2c.la
%{relocateConfig}lib/libstdc++.la
%{relocateConfig}lib/libsupc++.la
%if "%cpu" == "amd64"
%{relocateConfig}lib64/libg2c.la
%{relocateConfig}lib64/libstdc++.la
%{relocateConfig}lib64/libsupc++.la
%{relocateConfig}lib/32/libg2c.la
%{relocateConfig}lib/32/libstdc++.la
%{relocateConfig}lib/32/libsupc++.la
%endif
