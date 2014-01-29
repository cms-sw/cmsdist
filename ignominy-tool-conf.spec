### RPM cms ignominy-tool-conf 1.0
# with cmsBuild, change version only when a new
# tool is added 
 
Requires: gcc
Requires: systemtools
Requires: rulechecker
Requires: expat
Requires: libpng
Requires: libjpg
Requires: zlib
Requires: graphviz

%define skipreqtools ccompiler f77compiler opengl x11
%define use_system_java yes

## IMPORT scramv1-tool-conf
