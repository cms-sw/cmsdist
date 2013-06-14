### RPM virtual x11 2.3.2
Source: none
Provides: libICE.so.6  
Provides: libOSMesa.so.4  
Provides: libSM.so.6  
Provides: libX11.so.6  
Provides: libXTrap.so.6  
Provides: libXaw.so.6  
Provides: libXaw.so.7  
Provides: libXcursor.so.1  
Provides: libXext.so.6  
Provides: libXfont.so.1  
Provides: libXft.so.1  
Provides: libXft.so.2  
Provides: libXi.so.6  
Provides: libXmu.so.6  
Provides: libXmuu.so.1  
Provides: libXp.so.6  
Provides: libXpm.so.4  
Provides: libXrandr.so.2  
Provides: libXrender.so.1  
Provides: libXt.so.6  
Provides: libXtst.so.6  
Provides: libXv.so.1  
Provides: libdps.so.1  
Provides: libdpstk.so.1  
Provides: libpsres.so.1  
Provides: libximcp.so  
Provides: libxlcDef.so  
Provides: libxlcUTF8Load.so  
Provides: libxlibi18n.so  
Provides: libxlocale.so  
Provides: libxomGeneric.so  
Provides: xpm  
Provides: XFree86-libs 
%prep
%build
%install
echo 'This is only a virtual package, please install your distribution XFree86-libs.rpm or equivalent'> %{i}/README 
