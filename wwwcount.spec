#
# Conditional build:
# _without_database - without database support (wwwcount works in old way)
#
Summary:	WWW Hit Access Counter
Summary(pl):	Licznik dostepu do strony WWW
Name:		wwwcount
Version:	2.6
Release:	3
Epoch:		1
Group:		Networking/Utilities
License:	BSD-like
Source0:	http://www.muquit.com/muquit/software/Count/Count2.6/download/src/%{name}%{version}.tar.gz
Source1:	http://www.muquit.com/muquit/software/Count/Count2.6/download/docs/%{name}%{version}docs.tar.gz
Source2:	%{name}.cfg
Source3:	%{name}.logrotate
Patch0:		%{name}-pld.patch
URL:		http://www.muquit.com/muquit/software/Count/Count2.6/Count.html
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
%{!?_without_database:BuildRequires:	db3-devel}
Requires:	httpd

%description
wwwcount is a cgi script for apache (and other http daemons), which
prododuces nice picture with number of people visited your website.
You can use your custom fonts with wwwcount.

%description -l pl
wwwcount jest skryptem cgi do apache (i innych serwerów http), który
generuje piêkny obrazek z ilo¶ci± osób które odwiedzi³y twoj± stronê.
Mo¿esz u¿ywaæ tak¿e swoich unikalnych czcionek.

%prep
%setup -q -n %{name}%{version}
%patch -p1
tar xzf %{SOURCE1}

%build
#aclocal
#autoconf
%configure2_13 \
	%{?_without_database:--without-database}

./Count-config
./build --all

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/logrotate.d
install -d $RPM_BUILD_ROOT/home/httpd/cgi-bin
install -d $RPM_BUILD_ROOT/var/{log/httpd,lib/wwwcount/{data,db,log}}
install -d $RPM_BUILD_ROOT%{_libdir}/wwwcount
install -d $RPM_BUILD_ROOT%{_bindir}

install bin/Count.cgi $RPM_BUILD_ROOT/home/httpd/cgi-bin/wwwcount.cgi
%{!?_without_database:install bin/count_admin.cgi $RPM_BUILD_ROOT/home/httpd/cgi-bin/wwwcount_admin.cgi}
%{!?_without_database:install bin/count_admin_help.cgi $RPM_BUILD_ROOT/home/httpd/cgi-bin/wwwcount_admin_help.cgi}
install bin/{extdgts,mkstrip,mwhich} $RPM_BUILD_ROOT%{_bindir}
%{!?_without_database:install bin/{editdb,dumpdb,rgbtxt2db} $RPM_BUILD_ROOT%{_bindir}}
install data/data/* $RPM_BUILD_ROOT/var/lib/wwwcount/data
install data/rgb.txt $RPM_BUILD_ROOT%{_libdir}/wwwcount

install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}
install %{SOURCE3} $RPM_BUILD_ROOT/etc/logrotate.d/%{name}

cp -rf data/digits $RPM_BUILD_ROOT%{_libdir}/wwwcount
cp -rf data/fonts $RPM_BUILD_ROOT%{_libdir}/wwwcount

touch $RPM_BUILD_ROOT/var/lib/wwwcount/log/wwwcount-{error,visitor}

gzip -9nf README TODO
rm -rf %{name}%{version}docs/{dirsync,prehtml,scripts,tmp,README,gzip.arc,mkarc.sh}
rm -rf %{name}%{version}docs/Count%{version}/download

%post
TMPFILE=`mktemp /tmp/wwwcount-XXXXXX`
mv -f /etc/wwwcount.cfg $TMPFILE
cat $TMPFILE | sed "s/%HOSTNAME%/`hostname -f`/g" | \
  sed "s/%DOMAINNAME%/`hostname -d`/g" | \
  sed "s/%IPNAME%/`hostname -i`/g" > /etc/wwwcount.cfg
chmod 644 /etc/wwwcount.cfg
rm -f $TMPFILE  

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz %{name}%{version}docs/*
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) /home/httpd/cgi-bin/wwwcount.cgi
%{!?_without_database: %attr(755,root,root) /home/httpd/cgi-bin/wwwcount_*.cgi}
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/wwwcount.cfg
%attr(775,root,http) %dir /var/lib/wwwcount
%attr(775,root,http) %dir /var/lib/wwwcount/log
%{?bconf_off_database:%attr(775,root,http) %dir /var/lib/wwwcount/data}
%{!?bconf_off_database:%attr(775,root,http) %dir /var/lib/wwwcount/db}
%{?_without_database:%attr(664,root,http) %config(noreplace) %verify(not size mtime md5) /var/lib/wwwcount/data/*}
%attr(664,root,http) %config(noreplace) %verify(not size mtime md5) /var/lib/wwwcount/log/*
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/logrotate.d/*
%{_libdir}/wwwcount
