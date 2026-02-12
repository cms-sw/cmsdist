### RPM external gmake 4.4.1
Source: https://ftp.gnu.org/gnu/make/make-%{realversion}.tar.gz

# do not merge: test comment
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
