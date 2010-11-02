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
# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/rivet.xml
<tool name="rivet" version="%v">
<lib name="rivet"/>
<client>
<environment name="RIVET_BASE" default="%i"/>
<environment name="LIBDIR" default="$RIVET_BASE/lib"/>
<environment name="INCLUDE" default="$RIVET_BASE/include"/>
<environment name="PDFPATH" default="$RIVET_BASE/share"/>
</client>
<runtime name="PATH" value="$RIVET_BASE/bin"/>
<runtime name="LD_LIBRARY_PATH" value="$RIVET_BASE/lib"/>
<runtime name="PYTHONPATH" value="$RIVET_BASE/lib/python2.6/site-packages"/>
<runtime name="RIVET_ANALYSIS_PATH" value="$RIVET_BASE/lib"/>
</tool>
EOF_TOOLFILE
%post
%{relocateConfig}etc/scram.d/rivet.xml
