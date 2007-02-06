### RPM external gcc 3.4.5
## INITENV +PATH LD_LIBRARY_PATH %i/lib/32
## INITENV +PATH LD_LIBRARY_PATH %i/lib64
## BUILDIF [ $(uname) != Darwin ]
Source: ftp://ftp.fu-berlin.de/unix/gnu/%n/%n-%v/%n-%v.tar.bz2
%define cpu %(echo %cmsplatf | cut -d_ -f2)
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
