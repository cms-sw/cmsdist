### RPM external systemtools 19
## NOCOMPILER
Source: none

%if "%{?use_system_gcc:set}" == "set"
%define compilertools ccompiler cxxcompiler f77compiler
%else
%define compilertools %{nil}
%endif

%define systemtools                     sockets opengl x11 %compilertools
%define sockets_version                 1.0
%define opengl_version                  XFree4.2
%define x11_version                     R6

## INITENV SETV SOCKETS_VERSION         %sockets_version
## INITENV SETV OPENGL_VERSION          %opengl_version
## INITENV SETV X11_VERSION             %x11_version
## INITENV SETV PKGTOOLS_SYSTEM_TOOLS   %systemtools

%prep
%build
%install

