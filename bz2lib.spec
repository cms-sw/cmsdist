### RPM external bz2lib 1.0.6
Source: http://www.bzip.org/%{realversion}/bzip2-%{realversion}.tar.gz
%define cpu %(echo "%{cmsplatf}" | cut -f2 -d_)

%define isdarwin %(case %{cmsos} in (osx*) echo 1 ;; (*) echo 0 ;; esac)

%prep
%setup -n bzip2-%{realversion}
sed -e 's/ -shared/ -dynamiclib/' \
    -e 's/ -Wl,-soname -Wl,[^ ]*//' \
    -e 's/libbz2\.so/libbz2.dylib/g' \
    < Makefile-libbz2_so > Makefile-libbz2_dylib

%build
%if %isdarwin
make %{makeprocesses} -f Makefile-libbz2_dylib
%else
make %{makeprocesses} -f Makefile-libbz2_so
%endif

%install
make install PREFIX=%{i}
%if %isdarwin
%define soname dylib
%else
%define soname so
%endif
cp libbz2.%{soname}.%{realversion} %{i}/lib
ln -s libbz2.%{soname}.%{realversion} %{i}/lib/libbz2.%{soname}
ln -s libbz2.%{soname}.%{realversion} %{i}/lib/libbz2.%{soname}.$(echo %{realversion} | cut -d. -f 1,2)
ln -s libbz2.%{soname}.%{realversion} %{i}/lib/libbz2.%{soname}.$(echo %{realversion} | cut -d. -f 1)
ln -sf bzdiff %{i}/bin/bzcmp
ln -sf bzgrep %{i}/bin/bzegrep
ln -sf bzgrep %{i}/bin/bzfgrep
ln -sf bzmore %{i}/bin/bzless

%define strip_files %{i}/lib
%define drop_files %{i}/man
# bla bla
