### RPM external libungif 4.1.4

Source: http://switch.dl.sourceforge.net/sourceforge/giflib/%{n}-%{realversion}.tar.gz

%prep
%setup -n %{n}-%{realversion}

%build
# Update to detect aarch64 and ppc64le
rm -f ./config.{sub,guess}
curl -L -k -s -o ./config.sub 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD'
curl -L -k -s -o ./config.guess 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD'
chmod +x ./config.{sub,guess}

./configure --prefix=%{i} --disable-static
make %{makeprocesses}

%install
make install
# Strip libraries, we are not going to debug them.
%define strip_files %{i}/lib
# Drop all the perl scripts. They are not needed and force the installation of
# more packages on Ubuntu.
%define drop_files %{i}/bin
# bla bla
