### RPM external log4cplus 1.0.2

Source: http://switch.dl.sourceforge.net/sourceforge/%n/%{n}-%{v}.tar.gz

%build
./configure --prefix=%i
case $(uname)-$(uname -m) in
  Darwin*)
   perl -p -i -e "s|\/\* #undef socklen_t \*\/|#undef socklen_t|" include/log4cplus/config.h;; 
esac
make 

%install
make install


%changelog
* Mon Feb 27 2006 Stefano Argiro <stefano.argiro@cern.ch> 
- Initial build.


