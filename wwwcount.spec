#
# Conditional build:
# _without_database	- without database support (wwwcount works in old way)
# _with_db3		- use db3 instead of db package
#
Summary:	WWW Hit Access Counter
Summary(pl):	Licznik dostepu do strony WWW
Name:		wwwcount
Version:	2.6
Release:	7
Epoch:		1
Group:		Networking/Utilities
License:	BSD-like
Source0:	http://www.muquit.com/muquit/software/Count/Count2.6/download/src/%{name}%{version}.tar.gz
Source1:	http://www.muquit.com/muquit/software/Count/Count2.6/download/docs/%{name}%{version}docs.tar.gz
Source2:	%{name}.cfg
Source3:	%{name}.logrotate
Patch0:		%{name}-pld.patch
URL:		http://www.muquit.com/muquit/software/Count/Count2.6/Count.html
BuildRequires:	automake
%{!?_without_database:%{?_with_db3:BuildRequires:	db3-devel}}
%{!?_without_database:%{!?_with_db3:BuildRequires:	db-devel}}
Requires(post):	/bin/hostname
Requires(post):	fileutils
Requires(post):	sed
Requires:	httpd
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		httpdir		/home/services/httpd
%define		cgidir		%{httpdir}/cgi-bin

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
cp -f /usr/share/automake/config.* .
%configure2_13 \
	%{?_without_database:--without-database}

./Count-config
./build --all

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/logrotate.d,%{cgidir}} \
	$RPM_BUILD_ROOT/var/{log/httpd,lib/wwwcount/{data,db,log/archiv}} \
	$RPM_BUILD_ROOT{%{_libdir}/wwwcount,%{_bindir}}

install bin/Count.cgi $RPM_BUILD_ROOT%{cgidir}/wwwcount.cgi
%{!?_without_database:install bin/count_admin.cgi $RPM_BUILD_ROOT%{cgidir}/wwwcount_admin.cgi}
%{!?_without_database:install bin/count_admin_help.cgi $RPM_BUILD_ROOT%{cgidir}/wwwcount_admin_help.cgi}
install bin/{extdgts,mkstrip,mwhich} $RPM_BUILD_ROOT%{_bindir}
%{!?_without_database:install bin/{editdb,dumpdb,rgbtxt2db} $RPM_BUILD_ROOT%{_bindir}}
install data/data/* $RPM_BUILD_ROOT/var/lib/wwwcount/data
install data/rgb.txt $RPM_BUILD_ROOT%{_libdir}/wwwcount

install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}
install %{SOURCE3} $RPM_BUILD_ROOT/etc/logrotate.d/%{name}

cp -rf data/digits $RPM_BUILD_ROOT%{_libdir}/wwwcount
cp -rf data/fonts $RPM_BUILD_ROOT%{_libdir}/wwwcount

touch $RPM_BUILD_ROOT/var/lib/wwwcount/log/wwwcount-{error,visitor}

rm -rf %{name}%{version}docs/{dirsync,prehtml,scripts,tmp,README,gzip.arc,mkarc.sh}
rm -rf %{name}%{version}docs/Count%{version}/download

%clean
rm -rf $RPM_BUILD_ROOT

%post
umask 022
sed %{_sysconfdir}/wwwcount.cfg -e "s/%HOSTNAME%/`hostname -f`/g" \
	-e "s/%DOMAINNAME%/`hostname -d`/g" \
	-e "s/%IPNAME%/`hostname -i`/g" > %{_sysconfdir}/wwwcount.cfg.rpmtmp
mv -f %{_sysconfdir}/wwwcount.cfg.rpmtmp %{_sysconfdir}/wwwcount.cfg

%files
%defattr(644,root,root,755)
%doc README TODO %{name}%{version}docs/*
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{cgidir}/wwwcount.cgi
%{!?_without_database:%attr(755,root,root) %{cgidir}/wwwcount_*.cgi}
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/wwwcount.cfg
%attr(775,root,http) %dir /var/lib/wwwcount
%attr(775,root,http) %dir /var/lib/wwwcount/log
%attr(775,root,http) %dir /var/lib/wwwcount/log/archiv
%{?_without_database:%attr(775,root,http) %dir /var/lib/wwwcount/data}
%{!?_without_database:%attr(775,root,http) %dir /var/lib/wwwcount/db}
%{?_without_database:%attr(664,root,http) %config(noreplace) %verify(not size mtime md5) /var/lib/wwwcount/data/*}
%attr(664,root,http) %config(noreplace) %verify(not size mtime md5) /var/lib/wwwcount/log/wwwcount*
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/logrotate.d/*
%{_libdir}/wwwcount
