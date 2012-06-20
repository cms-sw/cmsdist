### RPM cms-sdt-pages 1.0
## NOCOMPILER

%prep
%build
%install
echo "<H1>Hello world!</h1>" > %cmsroot/WEB/index.html
