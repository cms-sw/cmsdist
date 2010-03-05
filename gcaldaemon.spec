### RPM external gcaldaemon 1.0

# Install instructions from http://gcaldaemon.sourceforge.net/usage11.html 

Requires: java-jdk
Source: http://downloads.sourceforge.net/project/%n/linux/%realversion/%{n}-linux-%{realversion}-beta16.zip?use_mirror=surfnet&output=/%{n}-linux-%{realversion}-beta16.zip

%prep
# You are at %_builddir
unzip %_sourcedir/%{n}-linux-%{realversion}-beta16.zip

%build

%install
cp -rp %_builddir/GCALDaemon/* %i/
chmod 755 %i/bin/*sh

# Dependencies
rm -rf %i/etc/profile.d
mkdir -p %i/etc/profile.d
for x in %pkgreqs; do
  case $x in /* ) continue ;; esac
  p=%{instroot}/%{cmsplatf}/$(echo $x | sed 's/\([^+]*\)+\(.*\)+\([A-Z0-9].*\)/\1 \2 \3/' | tr ' ' '/')
  echo ". $p/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
  echo "source $p/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
done

%post
# The relocation below is also needed for dependencies
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh

