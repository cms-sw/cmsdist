### RPM external gfortran-macosx 5664

# On macosx we compile using the system compiler,
# but it actually does not include gfortran.
# Using this spec we download a binary distribution
# of gfortran from http://r.research.att.com/
# which is compatible with the gcc shipped on the 
# system.

# Notice that we should update to 5664 (i.e. XCode 3.2.3)
# once available.
Source: http://r.research.att.com/gfortran-42-%realversion.pkg

%prep
pwd
/usr/bin/xar -xf %_sourcedir/gfortran-42-%realversion.pkg
mv *.pkg/Payload Payload.gz
%build
%install
pax --insecure -rz -f Payload.gz -s ',./usr,%i,'

# Only ship x86_64 binaries.
find %{i} ! -name '*.la' -type f -perm -a+x -exec lipo -thin x86_64 {} -output {} \;
# Drop unneeded files
%define drop_files %i/lib/gcc/powerpc-* %i/bin/powerpc-* i%i/libexec/gcc/powerpc %i/share
%define keep_archives yes
# bla bla
