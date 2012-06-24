### RPM cms cms-sdt-pages 1.0
## NOCOMPILER

%prep
%build
%install
echo "<html><H1>Hello world!</h1></html>" > %cmsroot/WEB/index.html
