### RPM external icc-provides 2018.0.128
## NOCOMPILER
%define mic %(case %cmsplatf in (*_mic_*) echo true;; (*) echo false;; esac)
Source: none
Provides: libiomp5.so()(64bit)
Provides: libimf.so()(64bit)
Provides: libintlc.so.5()(64bit)
Provides: libirng.so()(64bit)
Provides: libsvml.so()(64bit)
Provides: libc.so.6()(64bit)
Provides: libc.so.6(GLIBC_2.2.5)(64bit)  
Provides: libdl.so.2(GLIBC_2.14)(64bit)
Provides: libutil.so.1(GLIBC_2.14)(64bit)
Provides: libc.so.6(GLIBC_2.14)(64bit)
Provides: libcilkrts.so.5()(64bit)
Provides: ld-linux-k1om.so.2()(64bit)
Provides: ld-linux-k1om.so.2(GLIBC_2.14)(64bit)
Provides: librt.so.1(GLIBC_2.14)(64bit)
Provides: libifcore.so.5()(64bit)
Provides: libifport.so.5()(64bit)
Provides: libirc.so()(64bit)
%prep
%build
%install
# bla bla
