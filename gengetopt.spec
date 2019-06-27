### RPM external gengetopt 2.22.6
Source: ftp://ftp.gnu.org/gnu/gengetopt/gengetopt-%{realversion}.tar.gz
Patch0: gengetopt-parallelbuild

BuildRequires: autotools

%prep
%setup -q -n gengetopt-%{realversion}

%patch0 -p1 

# Regenerate build scripts
autoreconf -fiv

%build
# Only keep bin folder 
./configure --disable-silent-rules \
	    --prefix=%{i}

make %{makeprocesses}

%install
make install

rm -rf %{i}/share
# bla bla
