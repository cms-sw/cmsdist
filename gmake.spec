### RPM external gmake 4.2.1
Source: ftp://ftp.gnu.org/gnu/make/make-%{realversion}.tar.gz

%prep
%setup -n make-%{realversion}

%build
./configure --prefix=%{i}

make %{makeprocesses}

%install
make install
rm -rf %{i}/{man,info}
# Put in the symlink
cd %{i}/bin
ln -sf make gmake
# bla bla
