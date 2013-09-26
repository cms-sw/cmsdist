### RPM external bz2lib 1.0.5
# Build system patches by Lassi A. Tuura <lat@iki.fi>
%define mic %(case %cmsplatf in (*_mic_*) echo true;; (*) echo false;; esac)
%define make_opts %{nil}
%if "%mic" == "true"
Requires: icc
%define make_opts CXX="icpc -fPIC -mmic"  CC="icc -fPIC -mmic"
%endif
Source: http://www.bzip.org/%{realversion}/bzip2-%{realversion}.tar.gz
%define cpu %(echo "%{cmsplatf}" | cut -f2 -d_)
Provides: libbz2.so.1
%if "%{cpu}" == "amd64"
Provides: libbz2.so.1()(64bit)
%endif

%define isdarwin %(case %{cmsos} in (osx*) echo 1 ;; (*) echo 0 ;; esac)

%prep
%setup -n bzip2-%{realversion}
case %{cmsplatf} in
   *_mic_* )
   sed -i -e 's|CC=.*|CC=icc -fPIC -mmic|' Makefile-libbz2_so
   sed -i -e 's|CC=.*|CC=icc -fPIC -mmic|' Makefile
   ;;
esac
sed -e 's/ -shared/ -dynamiclib/' \
    -e 's/ -Wl,-soname -Wl,[^ ]*//' \
    -e 's/libbz2\.so/libbz2.dylib/g' \
    < Makefile-libbz2_so > Makefile-libbz2_dylib

%build
%if %isdarwin
so=dylib
%else
so=so
%endif
%{make_opts} make %{makeprocesses} -f Makefile-libbz2_$so

%install
%if %isdarwin
so=dylib
%else
so=so
%endif
%{make_opts} make install PREFIX=%{i}
# For bzip2 1.0.5, the library appears to retain the name libbz2.so.1.0.4
# rather than libbz2.so.1.0.5 as one would expect, so use this "tmpversion"
# instead of realversion
%define tmpversion 1.0.4
cp libbz2.${so}.%{tmpversion} %{i}/lib
ln -s libbz2.${so}.%{tmpversion} %{i}/lib/libbz2.$so
ln -s libbz2.${so}.%{tmpversion} %{i}/lib/libbz2.${so}.`echo %{tmpversion} | cut -d. -f 1,2`
ln -s libbz2.${so}.%{tmpversion} %{i}/lib/libbz2.${so}.`echo %{tmpversion} | cut -d. -f 1`
ln -sf bzdiff %{i}/bin/bzcmp
ln -sf bzgrep %{i}/bin/bzegrep
ln -sf bzgrep %{i}/bin/bzfgrep
ln -sf bzmore %{i}/bin/bzless

# Strip libraries, we are not going to debug them.
%define strip_files %{i}/lib
# Look up documentation online.
%define drop_files %{i}/man
