Summary:	WWW Hit Access Counter
Summary(pl):	Licznik dostepu do strony WWW
Name:		wwwcount
Version:	2.4
Release:	3
Group:		Networking/Utilities
Group(pl):	Sieciowe/Narzêdzia
Copyright:	GPL
Requires:	httpd
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Source0:	wwwcount-%{version}.tar.gz
Source1:	wwwcount.cfg
Source2:	%{name}.logrotate
Patch:		wwwcount-pld.patch

%description
wwwcount is a cgi script for apache (and other http daemons),
which prododuces nice picture with number of people visited
your website. You can use your custom fonts with wwwcount.

%description -l pl
wwwcount jest skryptem cgi do apache (i innych serwerów http),
który generuje piêkny obrazek z ilo¶ci± osób które odwiedzi³y
twoj± stronê. Mo¿esz u¿ywaæ tak¿e swoich unikalnych czcionek.

%prep
%setup  -q
%patch -p1

%build
./Count-config
CFLAGS="$RPM_OPT_FLAGS" LDFLAGS="-s" \
  ./configure %{_target_platform} --prefix=/usr
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/logrotate.d
install -d $RPM_BUILD_ROOT/home/httpd/cgi-bin
install -d $RPM_BUILD_ROOT/var/{log/httpd,lib/wwwcount}
install -d $RPM_BUILD_ROOT%{_libdir}/wwwcount/digits/{A,B,C,D,E}

install src/Count.cgi $RPM_BUILD_ROOT/home/httpd/cgi-bin/wwwcount.cgi
install $RPM_SOURCE_DIR/wwwcount.cfg $RPM_BUILD_ROOT/etc
install wcount/data/* $RPM_BUILD_ROOT/var/lib/wwwcount
install wcount/rgb.txt $RPM_BUILD_ROOT%{_libdir}/wwwcount

install %{SOURCE2} $RPM_BUILD_ROOT/etc/logrotate.d/%{name}

for FONT in A B C D E; do
  install wcount/digits/$FONT/* $RPM_BUILD_ROOT%{_libdir}/wwwcount/digits/$FONT
done

touch $RPM_BUILD_ROOT/var/log/httpd/wwwcount

%post
TMPFILE=`mktemp /tmp/wwwcount-XXXXXX`
mv /etc/wwwcount.cfg $TMPFILE
cat $TMPFILE | sed "s/%HOSTNAME%/`hostname -f`/g" | \
  sed "s/%DOMAINNAME%/`hostname -d`/g" | \
  sed "s/%IPNAME%/`hostname -i`/g" > /etc/wwwcount.cfg
chmod 644 /etc/wwwcount.cfg
rm -f $TMPFILE  

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc docs/*
%attr(755,root,root) /home/httpd/cgi-bin/wwwcount.cgi
%config /etc/wwwcount.cfg
%attr(775,http,http) %dir /var/lib/wwwcount
%attr(664,http,http) /var/lib/wwwcount/*
%attr(640,root,root) /var/log/httpd/wwwcount
%attr(640,root,root) %config(noreplace) /etc/logrotate.d/*
%{_libdir}/wwwcount
