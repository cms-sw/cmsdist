### RPM external qgraf 3.1.4
Source: https://gosam.hepforge.org/gosam-installer/qgraf-%{realversion}.tgz

%prep
%setup -q -c -n qgraf-%{realversion}

%build
FC="$(which gfortran)"

${FC} qgraf*.f -o qgraf -O2

%install
mkdir %{i}/bin
cp qgraf %{i}/bin
