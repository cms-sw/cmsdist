### RPM external libjpg 9
Source: http://www.ijg.org/files/jpegsrc.v%{realversion}.tar.gz

%prep
%setup -n jpeg-%{realversion}

# Update config.{guess,sub} scripts to detect aarch64 and ppc64le
rm -f %{_tmppath}/config.{sub,guess}
curl -L -k -s -o %{_tmppath}/config.guess 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD'
curl -L -k -s -o %{_tmppath}/config.sub 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD'
for CONFIG_GUESS_FILE in $(find $RPM_BUILD_DIR -name 'config.guess')
do
  rm -f $CONFIG_GUESS_FILE
  cp %{_tmppath}/config.guess $CONFIG_GUESS_FILE
  chmod +x $CONFIG_GUESS_FILE
done
for CONFIG_SUB_FILE in $(find $RPM_BUILD_DIR -name 'config.sub')
do
  rm -f $CONFIG_SUB_FILE
  cp %{_tmppath}/config.sub $CONFIG_SUB_FILE
  chmod +x $CONFIG_SUB_FILE
done

%build
./configure --prefix=%{i} --enable-shared --disable-static

make %makeprocesses
%install
mkdir -p %{i}/lib
mkdir -p %{i}/bin
mkdir -p %{i}/include
mkdir -p %{i}/man/man1
make install

# Strip libraries, we are not going to debug them.
%define strip_files %{i}/lib
# Don't need archive libraries.
rm -f %{i}/lib/*.{l,}a
# Look up documentation online.
%define drop_files %{i}/{share,man}
