### RPM external gmake 4.2.1
Source: ftp://ftp.gnu.org/gnu/make/make-%{realversion}.tar.gz

#https://github.com/osresearch/heads/blob/make-4.2.1/patches/make-4.2.1.patch
Patch0: make-4.2.1

%prep
%setup -n make-%{realversion}
%patch0 -p1

%build
./configure --prefix=%{i}

make %{makeprocesses}

%install
make install
rm -rf %{i}/{man,info}
# Put in the symlink
cd %{i}/bin
ln -sf make gmake
