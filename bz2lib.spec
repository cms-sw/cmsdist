### RPM external bz2lib 1.0.6
Source: http://www.bzip.org/%{realversion}/bzip2-%{realversion}.tar.gz

%prep
%setup -n bzip2-%{realversion}
sed -e 's/ -shared/ -dynamiclib/' \
    -e 's/ -Wl,-soname -Wl,[^ ]*//' \
    -e 's/libbz2\.so/libbz2.dylib/g' \
    < Makefile-libbz2_so > Makefile-libbz2_dylib

%build
case "%{cmsplatf}" in osx*) so=dylib ;; *) so=so ;; esac
make %{makeprocesses} -f Makefile-libbz2_$so

%install
case "%{cmsplatf}" in osx*) so=dylib ;; *) so=so ;; esac
make install PREFIX=%{i}
cp libbz2.${so}* %{i}/lib # make install does not copy shared libs
ln -s libbz2.${so}.%realversion %{i}/lib/libbz2.$so

# Fix symlinks that would otherwise point to the build area
ln -sf bzdiff %{i}/bin/bzcmp
ln -sf bzgrep %{i}/bin/bzegrep
ln -sf bzgrep %{i}/bin/bzfgrep
ln -sf bzmore %{i}/bin/bzless

# Strip libraries, we are not going to debug them.
%define strip_files %{i}/lib
# Look up documentation online.
%define drop_files %{i}/man
