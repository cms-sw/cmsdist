case $(arch) in
  osx*) PERL5LIB_PATH=/lib/perl5/site_perl ;;
  * ) PERL5LIB_PATH=/share/perl5 ;;
esac
export PERL5LIB_PATH
