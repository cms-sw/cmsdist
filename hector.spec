### RPM external hector 1_3_2-CMS3
%define rname Hector
%define realversion %(echo %v | cut -d- -f1 )
Requires: root
Source: http://www.fynu.ucl.ac.be/themes/he/ggamma/hector/%{rname}_%{realversion}.tbz

%prep
%setup -q -n %{rname}

%build
make 

%install

tar -c . | tar -x -C %i
