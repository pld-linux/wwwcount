Summary:	WWW Hit Access Counter
Summary(pl):	Licznik dostepu do strony WWW
Name:		wwwcount
Version:	2.4
Release:	1
Group:		Networking/Utilities
Group(pl):	Sieciowe/Narzêdzia
Copyright:	GPL
Requires:	httpd
BuildRoot:	/tmp/%{name}-%{version}-root
Source0:	wwwcount-%{version}.tar.gz
Source1:	wwwcount.cfg
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
  ./configure %{_target} --prefix=/usr
make


%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc
install -d $RPM_BUILD_ROOT/home/httpd/cgi-bin
install -d $RPM_BUILD_ROOT/var/{log,lib/wwwcount}
install -d $RPM_BUILD_ROOT%{_libdir}/wwwcount/digits/{A,B,C,D,E}

install src/Count.cgi $RPM_BUILD_ROOT/home/httpd/cgi-bin/wwwcount.cgi
install $RPM_SOURCE_DIR/wwwcount.cfg $RPM_BUILD_ROOT/etc
install wcount/data/* $RPM_BUILD_ROOT/var/lib/wwwcount
install wcount/rgb.txt $RPM_BUILD_ROOT%{_libdir}/wwwcount

for FONT in A B C D E; do
  install wcount/digits/$FONT/* $RPM_BUILD_ROOT%{_libdir}/wwwcount/digits/$FONT
done

touch $RPM_BUILD_ROOT/var/log/wwwcount.log

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
%doc docs/*
%defattr(644,root,root,755)
%attr(755,root,root) /home/httpd/cgi-bin/wwwcount.cgi
%config /etc/wwwcount.cfg
%attr(644,http,http,775) %dir /var/lib/wwwcount
%attr(664,http,http) /var/lib/wwwcount/*
%attr(640,root,root) /var/log/wwwcount.log
%{_libdir}/wwwcount

%changelog
* Wed Mar 24 1999 Marek Obuchowicz <elephant@pld.org.pl>
[2.4-1]
- First release for Polish(ed) Linux Distribution
