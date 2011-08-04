### RPM external libpng 1.2.46
Source: http://downloads.sourceforge.net/libpng/libpng12/%realversion/%n-%realversion.tar.bz2
%define online %(case %cmsplatf in (*onl_*_*) echo true;; (*) echo false;; esac)

%if "%online" != "true"
Requires: zlib
%endif

%prep
%setup -n %n-%{realversion}
 
%build
./configure --prefix=%{i}
make %makeprocesses

%install
make install
# We remove pkg-config files for two reasons:
# * it's actually not required (macosx does not even have it).
# * rpm 4.8 adds a dependency on the system /usr/bin/pkg-config 
#   on linux.
# In the case at some point we build a package that can be build
# only via pkg-config we have to think on how to ship our own
# version.
rm -rf %i/lib/pkgconfig
%post
%{relocateConfig}bin/libpng-config
%{relocateConfig}bin/libpng12-config
%{relocateConfig}lib/libpng.la
%{relocateConfig}lib/libpng12.la
