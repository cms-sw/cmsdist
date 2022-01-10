### RPM external correctionlib 2.1.0
## INITENV +PATH PYTHON27PATH %i/${PYTHON_LIB_SITE_PACKAGES}
%define tag v%{realversion}cms0
Source: none

Requires: zlib python

%prep

%build
git clone https://github.com/cms-nanoAOD/correctionlib.git --recursive -b %{tag} --depth 1
cd correctionlib
make

%install
cd correctionlib
make install PREFIX=%i/${PYTHON_LIB_SITE_PACKAGES}/correctionlib
mkdir -p %i/bin
