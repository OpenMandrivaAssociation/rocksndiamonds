%define	name	rocksndiamonds
%define version 3.2.4
%define rel	1
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
BuildRequires:	SDL_image-devel SDL_mixer-devel SDL_net-devel X11-devel alsa-lib-devel esound-devel
BuildRequires:	libsmpeg-devel

%description
This is a nice little game with color graphics and sound for your
Unix system.

If you know the game "Boulderdash" (Commodore C64) or "Emerald Mine"
(Amiga) or "Supaplex" (PC), you know what "ROCKS'N'DIAMONDS" is about.

%prep
%setup -q
perl -pi -e 's!.*RO_GAME_DIR\s*=.*!RO_GAME_DIR = %{_gamesdatadir}/%{name}!; s!.*RW_GAME_DIR\s*=.*!RW_GAME_DIR = /var/games/%{name}!' Makefile

%build
OPTIONS="%optflags" make sdl

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
mkdir -p $RPM_BUILD_ROOT/%{_menudir}
cat << EOF > $RPM_BUILD_ROOT/%{_menudir}/%{name}
?package(%{name}):command="%{_gamesbindir}/%{name}" icon="%{name}.png" \
  needs="x11" section="More Applications/Games/Arcade" title="Rocks n Diamonds" \
  longtitle="%{Summary}" xdg="true"
EOF
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

%post
%{update_menus}

%postun
%{clean_menus}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README COPYING
%attr(0755,root,root) %{_gamesbindir}/%{name}
%{_gamesdatadir}/%{name}
%_datadir/applications/mandriva*
%{_menudir}/%{name}
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_mandir}/man?/*
/var/games/%{name}
