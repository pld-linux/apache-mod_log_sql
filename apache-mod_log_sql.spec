# todo: split *.so to subpackages: mysql/dbi/ssl
%define		mod_name	log_sql
%define		apxs		/usr/sbin/apxs
Summary:	SQL logging module for Apache
Summary(pl.UTF-8):	Moduł logowania zapytań do Apache do bazy SQL
Name:		apache-mod_%{mod_name}
# NOTE: remember about apache1-mod_log_sql when updating!
Version:	1.101
Release:	1
License:	Apache (?)
Group:		Networking/Daemons/HTTP
Source0:	http://www.outoforder.cc/downloads/mod_log_sql/mod_%{mod_name}-%{version}.tar.bz2
# Source0-md5:	16157f311eba364d8ee467078e7cc086
Patch0:		mod_%{mod_name}-acam_libexecdir.patch
Patch1:		mod_%{mod_name}-subdirs.patch
URL:		http://www.outoforder.cc/projects/apache/mod_log_sql/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.0.40
BuildRequires:	apr-devel >= 1:1.0.0
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libdbi-devel >= 0.7.0
BuildRequires:	libtool
BuildRequires:	mysql-devel >= 3.23.30
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sed >= 4.0
Requires:	apache(modules-api) = %apache_modules_api
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)/conf.d

%description
mod_log_sql is a logging module for Apache 1.3 and 2.0 which logs all
requests to a database.

%description -l pl.UTF-8
mod_log_sql jest modułem logującym dla Apache 1.3 i 2.0, który pozwala
na logowanie wszystkich zapytań do bazy danych.

%prep
%setup -q -n mod_%{mod_name}-%{version}
%patch -P0 -p0
%patch -P1 -p1

rm -f docs/{Makefile*,*.xml} contrib/Makefile*
sed -i -e "s:apr-config:apr-1-config:g" aclocal.m4
sed -i -e "s:apu-config:apu-1-config:g" aclocal.m4

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%configure \
	--with-apxs=%{apxs}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_pkglibdir}}

install -p .libs/*.so $RPM_BUILD_ROOT%{_pkglibdir}
#install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}.conf

echo 'LoadModule %{mod_name}_module	modules/mod_%{mod_name}.so' > \
	$RPM_BUILD_ROOT%{_sysconfdir}/90_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart

%postun
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGELOG TODO contrib docs LICENSE
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*.so
