%define	name	rocksndiamonds
%define version 3.2.6.1
%define rel	6
%define release %mkrel %rel
%define	Summary	A boulderdash like game

Name:		%{name}
Summary:	%{Summary}
Version:	%{version}
Release:	%{release}
Source0:	http://www.artsoft.org/RELEASES/unix/rocksndiamonds/%{name}-%{version}.tar.bz2
Source11:	%{name}.16.png
Source12:	%{name}.32.png
Source13:	%{name}.48.png
URL:		http://www.artsoft.org/rocksndiamonds/
License:	GPL
Group:		Games/Arcade
BuildRequires:	SDL-devel
BuildRequires:	SDL_mixer-devel
BuildRequires:	SDL_image-devel
BuildRequires:	SDL_net-devel
BuildRequires:	libsmpeg-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
This is a nice little game with color graphics and sound for your
Unix system.

If you know the game "Boulderdash" (Commodore C64) or "Emerald Mine"
(Amiga) or "Supaplex" (PC), you know what "ROCKS'N'DIAMONDS" is about.

%prep
%setup -q
perl -pi -e 's!.*RO_GAME_DIR\s*=.*!RO_GAME_DIR = %{_gamesdatadir}/%{name}!; s!.*RW_GAME_DIR\s*=.*!RW_GAME_DIR = /var/games/%{name}!' Makefile

%build
make sdl OPTIONS="%optflags" CC="gcc %ldflags"

%install
rm -rf $RPM_BUILD_ROOT

# Install stuff
mkdir -p $RPM_BUILD_ROOT%{_gamesbindir} $RPM_BUILD_ROOT%{_gamesdatadir}/%{name} $RPM_BUILD_ROOT%{_mandir}/man1
cp -a %{name} $RPM_BUILD_ROOT%{_gamesbindir}/%{name}
cp -a graphics levels sounds music $RPM_BUILD_ROOT%{_gamesdatadir}/%{name}
cp -a *.1 $RPM_BUILD_ROOT%{_mandir}/man1

# Install scores
mkdir -p $RPM_BUILD_ROOT/var/games/%{name}
install -d $RPM_BUILD_ROOT/var/games/%{name}/scores


# Menu
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Rocks n Diamonds
Comment=%Summary
Exec=%_gamesbindir/%{name}
Icon=%name
Terminal=false
Type=Application
StartupNotify=true
Categories=X-MandrivaLinux-MoreApplications-Games-Arcade;Game;ArcadeGame;
EOF


# Icon
install -m644 %{SOURCE11} -D $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png
install -m644 %{SOURCE12} -D $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
install -m644 %{SOURCE13} -D $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png

%pre
if [ -d %{_gamesdatadir}/%{name}/scores ]; then
	mkdir -p /var/games/%{name}/
	mv %{_gamesdatadir}/%{name}/scores /var/games/%{name}/
fi

%if %mdkversion < 200900
%post
%{update_menus}
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README COPYING
%attr(0755,root,root) %{_gamesbindir}/%{name}
%{_gamesdatadir}/%{name}
%_datadir/applications/mandriva*
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_mandir}/man?/*
/var/games/%{name}


%changelog
* Thu May 05 2011 Oden Eriksson <oeriksson@mandriva.com> 3.2.6.1-5mdv2011.0
+ Revision: 669428
- mass rebuild

* Thu Feb 10 2011 Funda Wang <fwang@mandriva.org> 3.2.6.1-4
+ Revision: 637087
- rebuild
- tighten BR

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 3.2.6.1-3mdv2011.0
+ Revision: 607369
- rebuild

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 3.2.6.1-2mdv2010.1
+ Revision: 523925
- rebuilt for 2010.1

* Tue Jun 30 2009 Frederik Himpe <fhimpe@mandriva.org> 3.2.6.1-1mdv2010.0
+ Revision: 391100
- update to new version 3.2.6.1

* Sat Mar 07 2009 Antoine Ginies <aginies@mandriva.com> 3.2.4-2mdv2009.1
+ Revision: 351557
- rebuild

* Thu Jun 12 2008 Pixel <pixel@mandriva.com> 3.2.4-1mdv2009.0
+ Revision: 218433
- rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

  + Thierry Vignaud <tv@mandriva.org>
    - drop old menu
    - kill re-definition of %%buildroot on Pixel's request
    - buildrequires X11-devel instead of XFree86-devel

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Mon Nov 12 2007 Guillaume Rousse <guillomovitch@mandriva.org> 3.2.4-1mdv2008.1
+ Revision: 108339
- update to new version 3.2.4

  + Thierry Vignaud <tv@mandriva.org>
    - kill desktop-file-validate's 'warning: key "Encoding" in group "Desktop Entry" is deprecated'

* Fri Apr 20 2007 Olivier Blin <oblin@mandriva.com> 3.2.3-1mdv2008.0
+ Revision: 15620
- 3.2.3
- Import rocksndiamonds



* Wed Aug 23 2006 Götz Waschk <waschk@mandriva.org> 3.1.1-4mdv2007.0
- xdg menu
- fix buildrequires

* Sat Nov  5 2005 Olivier Blin <oblin@mandriva.com> 3.1.1-3mdk
- kill Patch0 (we already override options)
- specify game data dir in Makefile (#19627)
- kill wrapper script (the game now knows its data dir)
- specify game rw dir in Makefile (cleaner for scores)

* Mon Oct 17 2005 Olivier Blin <oblin@mandriva.com> 3.1.1-2mdk
- fix upgrade by moving scores to /var (#19213)

* Tue Oct 11 2005 Eskild Hustvedt <eskild@mandriva.org> 3.1.1-1mdk
- New version 3.1.1
- Renamed real executeable to .real
- Moved highscores to /var/games/rocksndiamonds
- A little cleanup

* Wed Aug 18 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 3.1.0-3mdk
- REbuild with new menu

* Thu Jul 08 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 3.1.0-2mdk
- fix buildrequires

* Thu Jul  8 2004 Michael Scherer <misc@mandrake.org> 3.1.0-1mdk
- New release 3.1.0

* Fri May 14 2004 Michael Scherer <misc@mandrake.org> 3.0.8-1mdk
- New release 3.0.8

* Thu Oct 16 2003 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 3.0.6-1mdk
- 3.0.6
- cosmetics

* Thu Aug 28 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 3.0.2-1mdk
- new version

* Wed Aug 13 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 3.0.0-1mdk
- new version

* Mon Jul 21 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 2.0.0-11mdk
- rebuild
- convert xpm icons to png icons
- change summary macro to avoid possible conflicts if we were to build debug package

* Wed Aug 14 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.0.0-10mdk
- Automated rebuild with gcc 3.2-0.3mdk

* Thu Jul 25 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.0.0-9mdk
- Automated rebuild with gcc3.2

* Sun Jul 21 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 2.0.0-8mdk
- recompile against new vorbis stuff

* Mon Apr 29 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 2.0.0-7mdk
- rebuild for new alsa

* Tue Jan 22 2002 Stefan van der Eijk <stefan@eijk.nu> 2.0.0-6mdk
- BuildRequires

* Fri Oct 12 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 2.0.0-5mdk
- rebuild for libpng3
- fix large-icon-not-in-package
- include man page

* Thu Jul  5 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 2.0.0-4mdk
- rebuild

* Mon May 14 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 2.0.0-3mdk
- revert Dadouification
- new SDL

* Sat Mar 24 2001 David BAUDENS <baudens@mandrakesoft.com> 2.0.0-2mdk
- PPC: build with gcc

* Fri Mar  9 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 2.0.0-1mdk
- 2.0.0 (many new goodies, including networked multiplayer)

* Sun Nov 05 2000 David BAUDENS <baudens@mandrakesoft.com> 1.4.0-5mdk
- Fix build for PPC

* Thu Oct 26 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 1.4.0-4mdk
- fix compile with gcc-2.96

* Wed Aug 23 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 1.4.0-3mdk
- automatically added packager tag

* Mon Aug 07 2000 Frederic Lepied <flepied@mandrakesoft.com> 1.4.0-2mdk
- automatically added BuildRequires

* Wed Aug  2 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 1.4.0-1mdk
- first package for Linux-Mandrake
