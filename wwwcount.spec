# TODO: use /usr/lib/cgi-bin instead of /home/services
#
# Conditional build:
%bcond_without	database	# without database support (wwwcount works in old way)
%bcond_with	db3		# use db3 instead of db package
#
Summary:	WWW Hit Access Counter
Summary(pl.UTF-8):	Licznik dostępu do strony WWW
Name:		wwwcount
Version:	2.6
Release:	10
Epoch:		1
Group:		Networking/Utilities
License:	BSD-like
Source0:	http://www.muquit.com/muquit/software/Count/Count2.6/Count2.6/download/src/%{name}%{version}.tar.gz
# Source0-md5:	1d584bb21fe401480c69fe2f08879b8d
Source1:	http://www.muquit.com/muquit/software/Count/Count2.6/Count2.6/download/docs/%{name}%{version}docs.tar.gz
# Source1-md5:	867648585ee461d9062501c9d279d59e
Source2:	%{name}.cfg
Source3:	%{name}.logrotate
Patch0:		%{name}-pld.patch
Patch1:		%{name}-errno.patch
Patch2:		%{name}-db41.patch
URL:		http://www.muquit.com/muquit/software/Count/Count2.6/Count.html
BuildRequires:	automake
%if %{with database}
%{!?with_db3:BuildRequires:	db-devel}
%{?with_db3:BuildRequires:	db3-devel}
%endif
BuildRequires:	freetype1-devel
Requires(post):	/bin/hostname
Requires(post):	fileutils
Requires(post):	sed
Requires:	webserver
Conflicts:	logrotate < 3.8.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		httpdir		/home/services/httpd
%define		cgidir		%{httpdir}/cgi-bin

%description
wwwcount is a cgi script for apache (and other HTTP daemons), which
prododuces nice picture with number of people visited your website.
You can use your custom fonts with wwwcount.

%description -l pl.UTF-8
wwwcount jest skryptem cgi do apache (i innych serwerów HTTP), który
generuje piękny obrazek z ilością osób które odwiedziły twoją stronę.
Możesz używać także swoich unikalnych czcionek.

%prep
%setup -q -n %{name}%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
tar xzf %{SOURCE1}

for a in `find -type f -name "*.pl*"`
do
	%{__perl} -pi -e 's@/usr/local/bin/perl@/usr/bin/perl@' $a
	%{__perl} -pi -e 's@c:\perl\bin\perl@/usr/bin/perl@' $a
done

%build
cp -f /usr/share/automake/config.* .
%configure2_13 \
	%{!?with_database:--without-database}

./build --all

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/logrotate.d,%{cgidir}} \
	$RPM_BUILD_ROOT/var/{log/httpd,lib/wwwcount/{data,db,log/archive}} \
	$RPM_BUILD_ROOT{%{_libdir}/wwwcount,%{_bindir}}

install bin/Count.cgi $RPM_BUILD_ROOT%{cgidir}/wwwcount.cgi
%{?with_database:install bin/count_admin.pl $RPM_BUILD_ROOT%{cgidir}/wwwcount_admin.cgi}
%{?with_database:install bin/count_admin_help.pl $RPM_BUILD_ROOT%{cgidir}/wwwcount_admin_help.cgi}
install bin/{extdgts,mkstrip,mwhich} $RPM_BUILD_ROOT%{_bindir}
%{?with_database:install bin/{editdb,dumpdb,rgbtxt2db} $RPM_BUILD_ROOT%{_bindir}}
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
%{?with_database:%attr(755,root,root) %{cgidir}/wwwcount_*.cgi}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/wwwcount.cfg
%attr(775,root,http) %dir /var/lib/wwwcount
%attr(775,root,http) %dir /var/lib/wwwcount/log
%attr(775,root,http) %dir /var/lib/wwwcount/log/archive
%{!?with_database:%attr(775,root,http) %dir /var/lib/wwwcount/data}
%{?with_database:%attr(775,root,http) %dir /var/lib/wwwcount/db}
%{!?with_database:%attr(664,root,http) %config(noreplace) %verify(not md5 mtime size) /var/lib/wwwcount/data/*}
%attr(664,root,http) %config(noreplace) %verify(not md5 mtime size) /var/lib/wwwcount/log/wwwcount*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/*
%{_libdir}/wwwcount
