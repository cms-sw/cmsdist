### RPM external rivet 1.3.0
Source: http://www.hepforge.org/archive/rivet/Rivet-%{realversion}.tar.gz
Requires: hepmc boost fastjet swig gsl
%prep
%setup -n Rivet-%{realversion}
./configure --prefix=%i --with-boost=${BOOST_ROOT} --with-hepmc=$HEPMC_ROOT --with-fastjet=$FASTJET_ROOT --with-gsl=$GSL_ROOT --disable-doxygen --disable-pdfmanual --disable-pyext --with-pic
%build
make
%install
make install
