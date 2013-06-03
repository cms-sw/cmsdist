### RPM external batch-only-virtual 1.0.0
Source: none
Provides: libGLU.so.1
Provides: libGLU.so.1.3
%prep
%build
%install
echo 'This is only a virtual package, please install your distribution X11 libraries, which should include these libraries. This rpm should _only_ be used on systems with no interactive users and where it is not possible to install the system X11 libraries.'> %{i}/README 
