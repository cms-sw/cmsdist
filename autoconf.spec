### RPM external autoconf 2.60
Source: http://ftp.gnu.org/gnu/%n/%n-%v.tar.gz

%build
./configure --prefix=%i
make
%install
make install
perl -p -i -e "s|#\!.*perl(.*)|#!/usr/bin/env perl$1|" %{i}/bin/autom4te \
                                                       %{i}/bin/autoheader \
                                                       %{i}/bin/autoreconf \
                                                       %{i}/bin/ifnames \
                                                       %{i}/bin/autoscan \
                                                       %{i}/bin/autoupdate
%post
%{relocateConfig}bin/autoconf
%{relocateConfig}bin/autoheader
%{relocateConfig}bin/autom4te
%{relocateConfig}bin/autoreconf
%{relocateConfig}bin/autoscan
%{relocateConfig}bin/autoupdate
%{relocateConfig}bin/ifnames
%{relocateConfig}share/autoconf/autom4te.cfg
