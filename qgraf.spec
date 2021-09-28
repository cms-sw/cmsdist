### RPM external qgraf 3.4.2
%define versionmajmin %(echo %v | cut -d. -f1,2)
Source: http://anonymous:anonymous@qgraf.tecnico.ulisboa.pt/v%{versionmajmin}/qgraf-%{realversion}.tgz

%prep
%setup -q -c -n qgraf-%{realversion}

%build
FC="$(which gfortran)"

${FC} qgraf*.f -o qgraf -O2

%install
mkdir %{i}/bin
cp qgraf %{i}/bin
