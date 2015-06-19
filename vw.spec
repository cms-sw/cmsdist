### RPM external vw v7.3
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

%define pkg vw
Source: git://github.com/JohnLangford/vowpal_wabbit?obj=master/%realversion&export=%pkg&output=/%pkg.tar.gz
Requires: boost autotools zlib

%prep
%setup -n %pkg

%build
./configure --prefix=%i --with-boost=$BOOST_ROOT --with-zlib=$ZLIB_ROOT
make %{makeprocesses}

%install
make install
