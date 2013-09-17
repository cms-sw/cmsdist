### RPM external icc composer_xe_2013
## NOCOMPILER
## INITENV CMD_SH  source /oplashare/sw/linux/intel_licence.sh
## INITENV CMD_SH  source /oplashare/sw/linux/x86_64/intel/xe2013/composer_xe_2013/bin/compilervars.sh intel64
%define mic %(case %cmsplatf in (*_mic_*) echo true;; (*) echo false;; esac)

Source: none
%if "%mic" == "true"
#Add in seed intel-mic-gpl-2.1.4982-15.el6.x86_64 for following provides
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
%endif

%prep
%build
%install
cd %i
ln -s /oplashare/sw/linux/x86_64/intel/xe2013/composer_xe_2013 installation
