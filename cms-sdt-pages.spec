### RPM cms cms-sdt-pages 1.0
## NOCOMPILER

%prep
%build
%install
echo "<html><H1>CMS SDT web pages</h1></html>" > %cmsroot/WEB/index.html
