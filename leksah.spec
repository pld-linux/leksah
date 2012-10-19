Summary:	Haskell IDE
Name:		leksah
Version:	0.12.1.3
Release:	0.1
License:	GPL
Group:		Development/Tools
Source0:	http://hackage.haskell.org/packages/archive/leksah/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	7b239fbcd67d969890e299fb7afb5985
Source1:	%{name}.desktop
Source2:	%{name}_loadsession.desktop
Source3:	%{name}.xml
Patch0:		haddock.patch
URL:		http://leksah.org/
BuildRequires:	ghc >= 6.12.3
BuildRequires:	rpmbuild(macros) >= 1.608
BuildRequires:	desktop-file-utils
%requires_releq	ghc
Requires:	hicolor-icon-theme
Requires:	leksah-server
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Leksah is an Integrated Development Environment for Haskell written in
Haskell. Leksah uses GTK+ as GUI Toolkit.

%prep
%setup -q
%patch0

%build
runhaskell Setup.hs configure -v2 --enable-library-profiling \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/128x128/apps \
	$RPM_BUILD_ROOT/%{_datadir}/mime/packages \
	$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
rm -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT/%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

install pics/leksah.png $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/128x128/apps/leksah.png

desktop-file-install \
	--add-category="Development" \
	--add-category="X-DevelopmentTools" \
	--dir=$RPM_BUILD_ROOT%{_desktopdir} %{SOURCE1}

desktop-file-install \
	--add-category="Development" \
	--add-category="X-DevelopmentTools" \
	--dir=$RPM_BUILD_ROOT%{_desktopdir} %{SOURCE2}

install %{SOURCE3} $RPM_BUILD_ROOT/%{_datadir}/mime/packages

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor
%update_desktop_database
%update_mime_database
%ghc_pkg_recache

%postun
%update_icon_cache hicolor
%update_desktop_database
%update_mime_database
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{name}
%dir %{_datadir}/%{name}-%{version}
%dir %{_datadir}/%{name}-%{version}/data
%dir %{_datadir}/%{name}-%{version}/data/leksah-welcome
%dir %{_datadir}/%{name}-%{version}/data/leksah-welcome/src
%dir %{_datadir}/%{name}-%{version}/pics
%dir %{_datadir}/%{name}-%{version}/language-specs
%{_datadir}/%{name}-%{version}/LICENSE
%{_datadir}/%{name}-%{version}/Readme
%{_datadir}/%{name}-%{version}/pics/*
%{_datadir}/%{name}-%{version}/data/*.lksh*
%{_datadir}/%{name}-%{version}/data/leksah.menu
%{_datadir}/%{name}-%{version}/data/LICENSE
%{_datadir}/%{name}-%{version}/data/welcome.txt
%{_datadir}/%{name}-%{version}/data/leksah-welcome/*.*
%{_datadir}/%{name}-%{version}/data/leksah-welcome/src/Main.hs
%{_datadir}/%{name}-%{version}/language-specs/*
%{_desktopdir}/%{name}.desktop
%{_desktopdir}/%{name}_loadsession.desktop
%{_datadir}/mime/packages/leksah.xml
%{_iconsdir}/hicolor/128x128/apps/leksah.png
