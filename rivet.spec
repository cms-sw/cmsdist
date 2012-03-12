### RPM external rivet 1.5.1
Source: http://www.hepforge.org/archive/rivet/Rivet-%{realversion}.tar.gz

Requires: hepmc boost fastjet swig gsl
Patch0: rivet-1.4.0
Patch1: rivet-1.5.1-fix-gcc47
%prep
%setup -n Rivet-%{realversion}
%patch0 -p0
%patch1 -p1
./configure --prefix=%i --with-boost=${BOOST_ROOT} --with-hepmc=$HEPMC_ROOT --with-fastjet=$FASTJET_ROOT --with-gsl=$GSL_ROOT --disable-doxygen --disable-pdfmanual --with-pic
# The following hack insures that the bins with the library linked explicitly
# rather than indirectly, as required by the gold linker
perl -p -i -e "s|LIBS = $|LIBS = -lHepMC|g" bin/Makefile
%build
make
%install
make install
# The following creates a (for now) empty directory consistent with the 
# tool definition (probably the PYTHONPATH entry could be removed there,
# too, but I'm still not sure if there is a use case for the python or not)
mkdir -p %i/lib/python2.6/site-packages

