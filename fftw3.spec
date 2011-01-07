### RPM external fftw3 3.2.2
Source: http://www.fftw.org/fftw-%realversion.tar.gz

%prep
%setup -n fftw-%realversion

%build
# This matches the configure options used to build FFTW3.1.2 for SL5
./configure --enable-shared --disable-dependency-tracking --enable-threads --prefix=%i
make %makeprocesses

%install
make install

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n.xml
<tool name="%n" version="%v">
  <lib name="fftw3"/>
  <client>
    <environment name="FFTW3_BASE" default="%i"/>
    <environment name="INCLUDE" default="$FFTW3_BASE/include"/>
    <environment name="LIBDIR" default="$FFTW3_BASE/lib"/>
  </client>
</tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n.xml
