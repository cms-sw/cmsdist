### RPM external pcre 4.4-XXXX
Source: ftp://ftp.csx.cam.ac.uk/pub/software/programming/%n/%n-%realversion.tar.bz2

%prep
%setup -n %n-%{realversion}

%post
%{relocateConfig}bin/pcre-config
