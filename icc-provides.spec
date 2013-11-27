### RPM external icc-provides composer_xe_2013
## NOCOMPILER
%define mic %(case %cmsplatf in (*_mic_*) echo true;; (*) echo false;; esac)
Source: none
%if "%mic" == "true"
Provides: libifport.so.5()(64bit)
Provides: libirc.so()(64bit)
%endif

%prep
%build
%install
