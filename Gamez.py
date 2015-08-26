#!/usr/bin/env python2.7
# Author: John van IJzendoorn
#
# This file is part of GamezServer.
#
# GamezServer is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# GamezServer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GamezServer.  If not, see <http://www.gnu.org/licenses/>.

# Check needed software dependencies to nudge users to fix their setup
from __future__ import with_statement

import time
import signal
import sys
import subprocess
import traceback

import os
sys.path.insert(1, os.path.abspath(os.path.join(os.path.dirname(__file__), 'lib')))

import shutil
import shutil_custom

shuitl.copyfile = shutil_custom.copyfile_custom

if sys.version_info < (2,7):
    print "Sorry, requires Python 2.7.x"
    sys.exit(1)

if sys.hexversion >= 0x020600F0:
    from multiprocessing import freeze_support  # @UnresolvedImport

import certifi
for env_cert_var in ['REQUESTS_CA_BUNDLE', 'CURL_CA_BUNDLE']:
    ca_cert_loc = os.environ.get(env_cert_var)
    if (not isinstance(ca_cert_loc, basestring)) or (not os.path.isfile(ca_cert_loc)):
        os.environ[env_cert_var] = certifi.where()

if sys.version_info >= (2, 7, 9):
    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context
else:
    try:
 Headphones/          SickBeard-TVRage/    photostation2/
JRE/                 SubMovies/           phpMyAdmin/
MalwareRemover/      SuperSync/           qmysql/
Maraschino/          SurveillanceStation/ spotweb/
Mylar/               Transmission/        subliminal/
NZBGet/              VideoStationPro/     update_qpkg_conf.sh*
[/share/MD0_DATA/.qpkg] # git clone --recursive https://github.com/metabrainz/mu     sicbrainz-server.git musicbrainz-server
Cloning into 'musicbrainz-server'...
remote: Counting objects: 256722, done.
remote: Compressing objects: 100% (123/123), done.
remote: Total 256722 (delta 63), reused 0 (delta 0), pack-reused 256595
Receiving objects: 100% (256722/256722), 75.82 MiB | 3.98 MiB/s, done.
Resolving deltas: 100% (202035/202035), done.
Checking connectivity... done.
/Apps/git/libexec/git-core/git-submodule: line 159: /usr/bin/perl: No such file      or directory
/Apps/git/libexec/git-core/git-submodule: line 159: /usr/bin/perl: No such file      or directory
[/share/MD0_DATA/.qpkg] # cd musicbrainz-server
[/share/MD0_DATA/.qpkg/musicbrainz-server] # ls
AUTHORS                          gulpfile.js
COPYING.md                       inc/
HACKING-CAA.md                   lib/
HACKING.md                       musicbrainz.yml
INSTALL-MASTER.md                npm-shrinkwrap.json
INSTALL.md                       package.json
Makefile.PL                      po/
README.md                        postgresql-musicbrainz-collate/
admin/                           postgresql-musicbrainz-unaccent/
app.psgi                         root/
bin/                             script/
contrib/                         t/
docs/                            upgrade.json*
fabfile.py                       upgrade.sh*
[/share/MD0_DATA/.qpkg/musicbrainz-server] # more INSTALL-MASTER.md
Installing a master MusicBrainz server
======================================

Before we begin: are you *absolutely sure* this is what you want? For the vast
majority of cases, you want either slave or standalone: slave if you'll be
automatically updating from the main MusicBrainz site, and standalone if you'll
be running otherwise. This document is only relevant if you intend to work on
something concerning the *production* of replication packets, or if you're
trying to create a complete fork of the MusicBrainz data for some reason. (It
might be useful if you're setting up something else and want to implement
MusicBrainz-like replication too, but that's probably not what got you here).

Still with us? Okay. Continue with the main INSTALL.md, but don't run InitDb.pl
at all yet. First, clone [dbmirror](https://github.com/metabrainz/dbmirror) and
build it with the makefile. Ensure that your DBDefs.pm file lists `RT_MASTER`
in the appropriate place. Then, run InitDb (probably with a data dump, as with
any other server setup), but including the `--pending` flag and the path to the
file `pending.so` created by the dbmirror build process. This should set up the
[/share/MD0_DATA/.qpkg/musicbrainz-server] # more INSTALL.md
Installing MusicBrainz Server
=============================

The easiest method of installing a local MusicBrainz Server may be to download t     he
[pre-configured virtual machine](http://musicbrainz.org/doc/MusicBrainz_Server/S     etup),
if there is a current image available. In case you only need a replicated
database, you should consider using [mbslave](https://bitbucket.org/lalinsky/mbs     lave).

If you want to manually set up MusicBrainz Server from source, read on!

Prerequisites
-------------

1.  A Unix based operating system

    The MusicBrainz development team uses a variety of Linux distributions, but
    Mac OS X will work just fine, if you're prepared to potentially jump through
    some hoops. If you are running Windows we recommend you set up a Ubuntu virt     ual
    machine.

    **This document will assume you are using Ubuntu for its instructions.**

2.  Perl (at least version 5.10.1)

    Perl comes bundled with most Linux operating systems, you can check your
    installed version of Perl with:

        perl -v

3.  PostgreSQL (at least version 9.1)

    PostgreSQL is required, along with its development libraries. To install
    using packages run the following, replacing 9.x with the latest version.

        sudo apt-get install postgresql-9.x postgresql-server-dev-9.x postgresql     -contrib-9.x postgresql-plperl-9.x

    Alternatively, you may compile PostgreSQL from source, but then make sure to
    also compile the cube extension found in contrib/cube. The database import
    script will take care of installing that extension into the database when it
    creates the database for you.

4.  Git

    The MusicBrainz development team uses Git for their DVCS. To install Git,
    run the following:

        sudo apt-get install git-core

5.  Memcached

    By default the MusicBrainz server requires a Memcached server running on the
    same server with default settings. To install Memcached, run the following:

        sudo apt-get install memcached

    You can change the memcached server name and port, or configure other datast     ores
    in lib/DBDefs.pm.

6.  Redis

    Sessions are stored in Redis, so a running Redis server is
    required.  Redis can be installed with the
    following command and will not need any further configuration:

        sudo apt-get install redis-server

    The databases and key prefix used by musicbrainz can be configured
    in lib/DBDefs.pm.  The defaults should be fine if you don't use
    your redis install for anything else.

7.  Node.js

    Node.js is required to build (and optionally minify) our JavaScript and CSS.
    If you plan on accessing musicbrainz-server inside a web browser, you should
    install Node and its package manager, npm. Do this by running:

        sudo apt-get install nodejs npm

    Depending on your Ubuntu version, another package might be required, too:

        sudo apt-get install nodejs-legacy

    This is only needed where it exists, so a warning about the package not bein     g
    found is not a problem.

8.  Standard Development Tools

    In order to install some of the required Perl and Postgresql modules, you'll
    need a C compiler and make. You can install a basic set of development tools
    with the command:

        sudo apt-get install build-essential


Server configuration
--------------------

1.  Download the source code.

        git clone --recursive git://github.com/metabrainz/musicbrainz-server.git
        cd musicbrainz-server

2.  Modify the server configuration file.

        cp lib/DBDefs.pm.sample lib/DBDefs.pm

    Fill in the appropriate values for `MB_SERVER_ROOT` and `WEB_SERVER`.
    If you are using a reverse proxy, you should set the environment variable
    MUSICBRAINZ_USE_PROXY=1 when starting the server.
    This makes the server aware of it when checking for the canonical uri.

    Determine what type of server this will be and set `REPLICATION_TYPE` accord     ingly:

    1.  `RT_SLAVE` (mirror server)

        A mirror server will always be in sync with the master database at
        http://musicbrainz.org by way of an hourly replication packet. Mirror
        servers do not allow any local editing. After the initial data import, t     he
        only changes allowed will be to load the next replication packet in turn     .

        Mirror servers will have their WikiDocs automatically kept up to date.

        If you are not setting up a mirror server for development purposes, make
        sure to set `DB_STAGING_SERVER` to 0.

        If you're setting up a slave server, make sure you have something set up
        for the READONLY database setting in lib/DBDefs.pm; it can just be a cop     y
        of what's in READWRITE if you don't need anything fancy.

    2.  `RT_STANDALONE`

        A stand alone server is recommended if you are setting up a server for
        development purposes. They do not accept the replication packets and wil     l
        require manually importing a new database dump in order to bring it up t     o
        date with the master database. Local editing is available, but keep in
        mind that none of your changes will be pushed up to http://musicbrainz.o     rg.

    3. `RT_MASTER`

        Almost certainly not what you want, this is what the main musicbrainz.or     g
        site runs on. It's different from standalone in that it's able to *produ     ce*
        replication packets to be applied on slaves. For more details, see
        INSTALL-MASTER.md


Installing Perl dependencies
----------------------------

The fundamental thing that needs to happen here is all the dependency Perl
modules get installed, somewhere where your server can find them. There are many
ways to make this happen, and the best choice will be very
site-dependent. MusicBrainz recommends the use of local::lib, which will install
Perl libraries into your home directory, and does not require root permissions
and avoids modifying the rest of your system.

Below outlines how to setup MusicBrainz server with local::lib.

1.  Prerequisites

    Before you get started you will actually need to have local::lib installed.
    There are also a few development headers that will be needed when installing
    dependencies. Run the following steps as a normal user on your system.

        sudo apt-get install libxml2-dev libpq-dev libexpat1-dev libdb-dev libic     u-dev liblocal-lib-perl cpanminus

2.  Enable local::lib

    local::lib requires a few environment variables are set. The easiest way to
    do this is via .bashrc, assuming you use bash as your shell. Simply run the
    following to append local::lib configuration to your bash configuration:

        echo 'eval $( perl -Mlocal::lib )' >> ~/.bashrc

    Next, to reload your configuration, either close and open your shell again,
    or run:

        source ~/.bashrc

3.  Install dependencies

    To install the dependencies for MusicBrainz Server, make sure you are
    in the MusicBrainz source code directory and run the following:

        cpanm --installdeps --notest .

    (Do not overlook the dot at the end of that command.)

Installing Node.js dependencies
-------------------------------

Node dependencies are managed using `npm`. To install these dependencies, run
the following inside the musicbrainz-server/ checkout:

    npm install

Node dependencies are installed under ./node\_modules.

We use Gulp as our JavaScript/CSS build system. This will be installed after
running the above. Calling `gulp` on its own will build everything necessary
to access the server in a web browser. It can be invoked by:

    ./node_modules/.bin/gulp

If you'd like, you can add ./node\_modules/.bin to your $PATH.


Creating the database
---------------------

1.  Install PostgreSQL Extensions

    Before you start, you need to install the PostgreSQL Extensions on your
    database server. To build the musicbrainz_unaccent extension run these
    commands:

        cd postgresql-musicbrainz-unaccent
        make
        sudo make install
        cd ..

    To build our collate extension you will need libicu and its development
    headers, to install these run:

        sudo apt-get install libicu-dev

    With libicu installed, you can build and install the collate extension by
    running:

        cd postgresql-musicbrainz-collate
        make
        sudo make install
        cd ..

2.  Setup PostgreSQL authentication

    For normal operation, the server only needs to connect from one or two OS
    users (whoever your web server/crontabs run as), to one database (the
    MusicBrainz Database), as one PostgreSQL user. The PostgreSQL database name
    and user name are given in DBDefs.pm (look for the `READWRITE` key).  For
    example, if you run your web server and crontabs as "www-user", the
    following configuration recipe may prove useful:

        # in pg_hba.conf (Note: The order of lines is important!):
        local    musicbrainz_db    musicbrainz    ident    map=mb_map

        # in pg_ident.conf:
        mb_map    www-user    musicbrainz

    Alternatively, if you are running a server for development purposes and
    don't require any special access permissions, the following configuration in
    pg_hba.conf will suffice (make sure to insert this line before any other
    permissions):

        local   all    all    trust

    Note that a running PostgreSQL will pick up changes to configuration files
    only when being told so via a `HUP` signal.

3.  Install a Perl module

    One PL/Perl database function requires the JSON::XS Perl module. Install it
    like so:

        sudo apt-get install libjson-xs-perl

4.  Create the database

    You have two options when it comes to the database. You can either opt for a
    clean database with just the schema (useful for developers with limited disk
    space), or you can import a full database dump.

    1.  Use a clean database

        To use a clean database, all you need to do is run:

            ./admin/InitDb.pl --createdb --clean

    2.  Import a database dump

        Our database dumps are provided twice a week and can be downloaded from
        ftp://ftp.musicbrainz.org/pub/musicbrainz/data/fullexport/
        or the European mirror server at
        ftp://eu.ftp.musicbrainz.org/MusicBrainz/data/fullexport/

        To get going, you need at least the mbdump.tar.bz2,
        mbdump-editor.tar.bz2 and mbdump-derived.tar.bz2 archives, but you can
        grab whichever dumps suit your needs.

        Assuming the dumps have been downloaded to /tmp/dumps/ you can verify
        that the data is correct by running:

            pushd /tmp/dumps/ && md5sum -c MD5SUMS && popd

        You can also verify that the data dumps were indeed created by
        MusicBrainz verifying them against our GPG signing key:

            gpg --recv-keys C777580F
            gpg --verify-files /tmp/dumps/*.asc

        If this is OK and you wish to continue, you can import them with:

            ./admin/InitDb.pl --createdb --import /tmp/dumps/mbdump*.tar.bz2 --e     cho

        `--echo` just gives us a bit more feedback in case this goes wrong, you
        may leave it off. Remember to change the paths to your mbdump*.tar.bz2
        files, if they are not in /tmp/dumps/.

        By default, the archives will be extracted into the `/tmp` directory as
        an intermediate step. You may specify a different location with the
        `--tmp-dir` option.

    NOTE: on a fresh postgresql install you may see the following error:

        CreateFunctions.sql:33: ERROR:  language "plpgsql" does not exist

    To resolve that login to postgresql with the "postgres" user (or any other
    postgresql user with SUPERUSER privileges) and load the "plpgsql" language
    into the database with the following command:

        postgres=# CREATE LANGUAGE plpgsql;

    MusicBrainz Server doesn't enforce any statement timeouts on any SQL it runs     .
    If this is an issue in your setup, you may want to set a timeout at the
    database level:

        ALTER DATABASE musicbrainz_db SET statement_timeout TO 60000;


Starting the server
-------------------

You should now have everything ready to run the development server!

The development server is a lightweight HTTP server that gives good debug
output and is much more convenient than having to set up a standalone
server. Just run:

    plackup -Ilib -r

Visiting http://your.machines.ip.address:5000/ should now present you with
your own running instance of the MusicBrainz Server.

If you'd like a more permanent setup,
[the plackup documentation](https://metacpan.org/pod/plackup) may prove useful
in setting up a server such as nginx, using FastCGI.


Translations
------------

If you intend to run a server with translations, there are a few steps to follow     :

1.  Prerequisites

    Make sure gettext is installed (you need msgmerge and msgfmt, at least),
    and the transifex client 'tx'
    (http://help.transifex.com/features/client/index.html):

        sudo apt-get install gettext transifex-client

    Configure a username and password in ~/.transifexrc using the format listed
    on the above page.

2.  Change to the po directory

        cd po/

3.  Get translations

        tx pull -l {a list of languages you want to pull}

    This will download the .po files for your language(s) of choice to the po/
    folder with the correct filenames.

4.  Install translations

        make install

    This will compile and install the files to
    lib/LocaleData/{language}/LC\_MESSAGES/{domain}.mo

5.  Add the languages to MB\_LANGUAGES in DBDefs.pm. These should be formatted
    {lang}-{country}, e.g. 'es', or 'fr-ca', in a space-separated list.

6.  Ensure you have a system locale for any languages you want to use, and for
    some languages, be wary of https://rt.cpan.org/Public/Bug/Display.html?id=78     341

    For many languages, this will suffice:

        sudo apt-get install language-pack-{language code}

    To work around the linked CPAN bug, you may need to edit the file for Locale     ::Util
    to add entries to LANG2COUNTRY. Suggested ones include:

    * es => 'ES'
    * et => 'EE'
    * el => 'GR'
    * sl => 'SI' (this one is there in 1.20, but needs amendment)


Troubleshooting
---------------

If you have any difficulties, feel free to ask in #musicbrainz-devel on
irc.freenode.net, or email the [developer mailing list](http://lists.musicbrainz     .org/mailman/listinfo/musicbrainz-devel).

Please report any issues on our [bug tracker](http://tickets.musicbrainz.org/).

Good luck, and happy hacking!
[/share/MD0_DATA/.qpkg/musicbrainz-server] # perl -v

This is perl, v5.10.0 built for i686-unknown-linux-gnu

Copyright 1987-2007, Larry Wall

Perl may be copied only under the terms of either the Artistic License or the
GNU General Public License, which may be found in the Perl 5 source kit.

Complete documentation for Perl, including FAQ lists, should be found on
this system using "man perl" or "perldoc perl".  If you have access to the
Internet, point your browser at http://www.perl.org/, the Perl Home Page.

[/share/MD0_DATA/.qpkg/musicbrainz-server] # sudo apt-get install postgresql-9.x      postgresql-server-dev-9.x postgresql-contrib-9.x postgresql-plperl-9.x
sudo: unknown user: root
sudo: unable to initialize policy plugin
[/share/MD0_DATA/.qpkg/musicbrainz-server] # apt-get install postgresql-9.x post     gresql-server-dev-9.x postgresql-contrib-9.x postgresql-plperl-9.x
-sh: apt-get: command not found
[/share/MD0_DATA/.qpkg/musicbrainz-server] # ipkg install memcached
Package memcached (1.3.0-2) installed in root is up to date.
Nothing to be done
Successfully terminated.
[/share/MD0_DATA/.qpkg/musicbrainz-server] # ipkg  install redis-server
Nothing to be done
An error ocurred, return value: 4.
Collected errors:
Cannot find package redis-server.
Check the spelling or perhaps run 'ipkg update'
[/share/MD0_DATA/.qpkg/musicbrainz-server] # ipkg update
Downloading http://ipkg.nslu2-linux.org/feeds/optware/cs05q1armel/cross/stable/P     ackages
Updated list of available packages in /opt/lib/ipkg/lists/cs05q1armel
Downloading http://ipkg.nslu2-linux.org/feeds/optware/ts509/cross/unstable/Packa     ges.gz
Inflating http://ipkg.nslu2-linux.org/feeds/optware/ts509/cross/unstable/Package     s.gz
Updated list of available packages in /opt/lib/ipkg/lists/ts509
Successfully terminated.
[/share/MD0_DATA/.qpkg/musicbrainz-server] # ipkg install redis
Package redis (2.4.17-1) installed in root is up to date.
Nothing to be done
Successfully terminated.
[/share/MD0_DATA/.qpkg/musicbrainz-server] # ipkg list redis
redis - 2.0.4-1 - Redis is an advanced key-value store.
redis - 2.4.17-1 - Redis is an advanced key-value store.
Successfully terminated.
[/share/MD0_DATA/.qpkg/musicbrainz-server] # ipkg list nodejs
Successfully terminated.
[/share/MD0_DATA/.qpkg/musicbrainz-server] # ipkg install nodejs npm
Nothing to be done
An error ocurred, return value: 4.
Collected errors:
Cannot find package nodejs.
Check the spelling or perhaps run 'ipkg update'
Cannot find package npm.
Check the spelling or perhaps run 'ipkg update'
[/share/MD0_DATA/.qpkg/musicbrainz-server] # cp lib/DBDefs.pm.sample lib/DBDefs.     pm
[/share/MD0_DATA/.qpkg/musicbrainz-server] # vi lib/DBDefs.pm

# The server root, i.e. the parent directory of admin, bin, lib, root, etc.
# By default, this uses the path of lib/DBDefs/Default.pm, minus '/lib/DBDefs/De
sub MB_SERVER_ROOT    { "/share/MD0_DATA/Web/musicbrainz/musicbrainz-server" }
# Where static files are located
# sub STATIC_FILES_DIR { my $self= shift; $self->MB_SERVER_ROOT . '/root/static'

################################################################################
# The Database
################################################################################

# Configuring databases here is required; there are no defaults.
MusicBrainz::Server::DatabaseConnectionFactory->register_databases(
    # How to connect when we need read-write access to the database
    READWRITE => {
        database    => "musicbrainz_db",
        username    => "musicbrainz",
        password        => "musicbrainz",
#       host            => "",
#       port            => "",
    },
    # How to connect to a test database
    TEST => {
[/share/MD0_DATA/.qpkg/musicbrainz-server] # cd ../Web
-sh: cd: ../Web: No such file or directory
[/share/MD0_DATA/.qpkg/musicbrainz-server] # cd ..
[/share/MD0_DATA/.qpkg] # ls
BitTorrentSync/      PHP/                 git/
CloudLink/           PlexMediaServer/     homewizard/
CouchPotato2/        PostgreSQL/          maracopy/
DSv3/                Python/              maraschino.cpy/
Dropbox/             QMariaDB/            musicbrainz-server/
GamezServer/         QNAP-Plex-Fix/       musicstation/
Headphones/          SickBeard-TVRage/    nodejs/
JRE/                 SubMovies/           photostation2/
MalwareRemover/      SuperSync/           phpMyAdmin/
Maraschino/          SurveillanceStation/ qmysql/
Mylar/               Transmission/        spotweb/
NZBGet/              VideoStationPro/     subliminal/
Optware/             autorun@             update_qpkg_conf.sh*
[/share/MD0_DATA/.qpkg] # cd ../Web
[/share/MD0_DATA/Web] # ls
@Recycle/     cops/         mediawiki/    phpPgAdmin@   transmission@
Optware@      index.php*    phpMyAdmin@   spotweb@
[/share/MD0_DATA/Web] # cd ../.qpkg
[/share/MD0_DATA/.qpkg] # ;s
-sh: syntax error near unexpected token `;'
[/share/MD0_DATA/.qpkg] # ls
BitTorrentSync/      PHP/                 git/
CloudLink/           PlexMediaServer/     homewizard/
CouchPotato2/        PostgreSQL/          maracopy/
DSv3/                Python/              maraschino.cpy/
Dropbox/             QMariaDB/            musicbrainz-server/
GamezServer/         QNAP-Plex-Fix/       musicstation/
Headphones/          SickBeard-TVRage/    nodejs/
JRE/                 SubMovies/           photostation2/
MalwareRemover/      SuperSync/           phpMyAdmin/
Maraschino/          SurveillanceStation/ qmysql/
Mylar/               Transmission/        spotweb/
NZBGet/              VideoStationPro/     subliminal/
Optware/             autorun@             update_qpkg_conf.sh*
[/share/MD0_DATA/.qpkg] # cd music*
[/share/MD0_DATA/.qpkg/musicbrainz-server] # ;s
-sh: syntax error near unexpected token `;'
[/share/MD0_DATA/.qpkg/musicbrainz-server] # ls
AUTHORS                          gulpfile.js
COPYING.md                       inc/
HACKING-CAA.md                   lib/
HACKING.md                       musicbrainz.yml
INSTALL-MASTER.md                npm-shrinkwrap.json
INSTALL.md                       package.json
Makefile.PL                      po/
README.md                        postgresql-musicbrainz-collate/
admin/                           postgresql-musicbrainz-unaccent/
app.psgi                         root/
bin/                             script/
contrib/                         t/
docs/                            upgrade.json*
fabfile.py                       upgrade.sh*
[/share/MD0_DATA/.qpkg/musicbrainz-server] # cat INSTALL.md
Installing MusicBrainz Server
=============================

The easiest method of installing a local MusicBrainz Server may be to download t     he
[pre-configured virtual machine](http://musicbrainz.org/doc/MusicBrainz_Server/S     etup),
if there is a current image available. In case you only need a replicated
database, you should consider using [mbslave](https://bitbucket.org/lalinsky/mbs     lave).

If you want to manually set up MusicBrainz Server from source, read on!

Prerequisites
-------------

1.  A Unix based operating system

    The MusicBrainz development team uses a variety of Linux distributions, but
    Mac OS X will work just fine, if you're prepared to potentially jump through
    some hoops. If you are running Windows we recommend you set up a Ubuntu virt     ual
    machine.

    **This document will assume you are using Ubuntu for its instructions.**

2.  Perl (at least version 5.10.1)

    Perl comes bundled with most Linux operating systems, you can check your
    installed version of Perl with:

        perl -v

3.  PostgreSQL (at least version 9.1)

    PostgreSQL is required, along with its development libraries. To install
    using packages run the following, replacing 9.x with the latest version.

        sudo apt-get install postgresql-9.x postgresql-server-dev-9.x postgresql     -contrib-9.x postgresql-plperl-9.x

    Alternatively, you may compile PostgreSQL from source, but then make sure to
    also compile the cube extension found in contrib/cube. The database import
    script will take care of installing that extension into the database when it
    creates the database for you.

4.  Git

    The MusicBrainz development team uses Git for their DVCS. To install Git,
    run the following:

        sudo apt-get install git-core

5.  Memcached

    By default the MusicBrainz server requires a Memcached server running on the
    same server with default settings. To install Memcached, run the following:

        sudo apt-get install memcached

    You can change the memcached server name and port, or configure other datast     ores
    in lib/DBDefs.pm.

6.  Redis

    Sessions are stored in Redis, so a running Redis server is
    required.  Redis can be installed with the
    following command and will not need any further configuration:

        sudo apt-get install redis-server

    The databases and key prefix used by musicbrainz can be configured
    in lib/DBDefs.pm.  The defaults should be fine if you don't use
    your redis install for anything else.

7.  Node.js

    Node.js is required to build (and optionally minify) our JavaScript and CSS.
    If you plan on accessing musicbrainz-server inside a web browser, you should
    install Node and its package manager, npm. Do this by running:

        sudo apt-get install nodejs npm

    Depending on your Ubuntu version, another package might be required, too:

        sudo apt-get install nodejs-legacy

    This is only needed where it exists, so a warning about the package not bein     g
    found is not a problem.

8.  Standard Development Tools

    In order to install some of the required Perl and Postgresql modules, you'll
    need a C compiler and make. You can install a basic set of development tools
    with the command:

        sudo apt-get install build-essential


Server configuration
--------------------

1.  Download the source code.

        git clone --recursive git://github.com/metabrainz/musicbrainz-server.git
        cd musicbrainz-server

2.  Modify the server configuration file.

        cp lib/DBDefs.pm.sample lib/DBDefs.pm

    Fill in the appropriate values for `MB_SERVER_ROOT` and `WEB_SERVER`.
    If you are using a reverse proxy, you should set the environment variable
    MUSICBRAINZ_USE_PROXY=1 when starting the server.
    This makes the server aware of it when checking for the canonical uri.

    Determine what type of server this will be and set `REPLICATION_TYPE` accord     ingly:

    1.  `RT_SLAVE` (mirror server)

        A mirror server will always be in sync with the master database at
        http://musicbrainz.org by way of an hourly replication packet. Mirror
        servers do not allow any local editing. After the initial data import, t     he
        only changes allowed will be to load the next replication packet in turn     .

        Mirror servers will have their WikiDocs automatically kept up to date.

        If you are not setting up a mirror server for development purposes, make
        sure to set `DB_STAGING_SERVER` to 0.

        If you're setting up a slave server, make sure you have something set up
        for the READONLY database setting in lib/DBDefs.pm; it can just be a cop     y
        of what's in READWRITE if you don't need anything fancy.

    2.  `RT_STANDALONE`

        A stand alone server is recommended if you are setting up a server for
        development purposes. They do not accept the replication packets and wil     l
        require manually importing a new database dump in order to bring it up t     o
        date with the master database. Local editing is available, but keep in
        mind that none of your changes will be pushed up to http://musicbrainz.o     rg.

    3. `RT_MASTER`

        Almost certainly not what you want, this is what the main musicbrainz.or     g
        site runs on. It's different from standalone in that it's able to *produ     ce*
        replication packets to be applied on slaves. For more details, see
        INSTALL-MASTER.md


Installing Perl dependencies
----------------------------

The fundamental thing that needs to happen here is all the dependency Perl
modules get installed, somewhere where your server can find them. There are many
ways to make this happen, and the best choice will be very
site-dependent. MusicBrainz recommends the use of local::lib, which will install
Perl libraries into your home directory, and does not require root permissions
and avoids modifying the rest of your system.

Below outlines how to setup MusicBrainz server with local::lib.

1.  Prerequisites

    Before you get started you will actually need to have local::lib installed.
    There are also a few development headers that will be needed when installing
    dependencies. Run the following steps as a normal user on your system.

        sudo apt-get install libxml2-dev libpq-dev libexpat1-dev libdb-dev libic     u-dev liblocal-lib-perl cpanminus

2.  Enable local::lib

    local::lib requires a few environment variables are set. The easiest way to
    do this is via .bashrc, assuming you use bash as your shell. Simply run the
    following to append local::lib configuration to your bash configuration:

        echo 'eval $( perl -Mlocal::lib )' >> ~/.bashrc

    Next, to reload your configuration, either close and open your shell again,
    or run:

        source ~/.bashrc

3.  Install dependencies

    To install the dependencies for MusicBrainz Server, make sure you are
    in the MusicBrainz source code directory and run the following:

        cpanm --installdeps --notest .

    (Do not overlook the dot at the end of that command.)

Installing Node.js dependencies
-------------------------------

Node dependencies are managed using `npm`. To install these dependencies, run
the following inside the musicbrainz-server/ checkout:

    npm install

Node dependencies are installed under ./node\_modules.

We use Gulp as our JavaScript/CSS build system. This will be installed after
running the above. Calling `gulp` on its own will build everything necessary
to access the server in a web browser. It can be invoked by:

    ./node_modules/.bin/gulp

If you'd like, you can add ./node\_modules/.bin to your $PATH.


Creating the database
---------------------

1.  Install PostgreSQL Extensions

    Before you start, you need to install the PostgreSQL Extensions on your
    database server. To build the musicbrainz_unaccent extension run these
    commands:

        cd postgresql-musicbrainz-unaccent
        make
        sudo make install
        cd ..

    To build our collate extension you will need libicu and its development
    headers, to install these run:

        sudo apt-get install libicu-dev

    With libicu installed, you can build and install the collate extension by
    running:

        cd postgresql-musicbrainz-collate
        make
        sudo make install
        cd ..

2.  Setup PostgreSQL authentication

    For normal operation, the server only needs to connect from one or two OS
    users (whoever your web server/crontabs run as), to one database (the
    MusicBrainz Database), as one PostgreSQL user. The PostgreSQL database name
    and user name are given in DBDefs.pm (look for the `READWRITE` key).  For
    example, if you run your web server and crontabs as "www-user", the
    following configuration recipe may prove useful:

        # in pg_hba.conf (Note: The order of lines is important!):
        local    musicbrainz_db    musicbrainz    ident    map=mb_map

        # in pg_ident.conf:
        mb_map    www-user    musicbrainz

    Alternatively, if you are running a server for development purposes and
    don't require any special access permissions, the following configuration in
    pg_hba.conf will suffice (make sure to insert this line before any other
    permissions):

        local   all    all    trust

    Note that a running PostgreSQL will pick up changes to configuration files
    only when being told so via a `HUP` signal.

3.  Install a Perl module

    One PL/Perl database function requires the JSON::XS Perl module. Install it
    like so:

        sudo apt-get install libjson-xs-perl

4.  Create the database

    You have two options when it comes to the database. You can either opt for a
    clean database with just the schema (useful for developers with limited disk
    space), or you can import a full database dump.

    1.  Use a clean database

        To use a clean database, all you need to do is run:

            ./admin/InitDb.pl --createdb --clean

    2.  Import a database dump

        Our database dumps are provided twice a week and can be downloaded from
        ftp://ftp.musicbrainz.org/pub/musicbrainz/data/fullexport/
        or the European mirror server at
        ftp://eu.ftp.musicbrainz.org/MusicBrainz/data/fullexport/

        To get going, you need at least the mbdump.tar.bz2,
        mbdump-editor.tar.bz2 and mbdump-derived.tar.bz2 archives, but you can
        grab whichever dumps suit your needs.

        Assuming the dumps have been downloaded to /tmp/dumps/ you can verify
        that the data is correct by running:

            pushd /tmp/dumps/ && md5sum -c MD5SUMS && popd

        You can also verify that the data dumps were indeed created by
        MusicBrainz verifying them against our GPG signing key:

            gpg --recv-keys C777580F
            gpg --verify-files /tmp/dumps/*.asc

        If this is OK and you wish to continue, you can import them with:

            ./admin/InitDb.pl --createdb --import /tmp/dumps/mbdump*.tar.bz2 --e     cho

        `--echo` just gives us a bit more feedback in case this goes wrong, you
        may leave it off. Remember to change the paths to your mbdump*.tar.bz2
        files, if they are not in /tmp/dumps/.

        By default, the archives will be extracted into the `/tmp` directory as
        an intermediate step. You may specify a different location with the
        `--tmp-dir` option.

    NOTE: on a fresh postgresql install you may see the following error:

        CreateFunctions.sql:33: ERROR:  language "plpgsql" does not exist

    To resolve that login to postgresql with the "postgres" user (or any other
    postgresql user with SUPERUSER privileges) and load the "plpgsql" language
    into the database with the following command:

        postgres=# CREATE LANGUAGE plpgsql;

    MusicBrainz Server doesn't enforce any statement timeouts on any SQL it runs     .
    If this is an issue in your setup, you may want to set a timeout at the
    database level:

        ALTER DATABASE musicbrainz_db SET statement_timeout TO 60000;


Starting the server
-------------------

You should now have everything ready to run the development server!

The development server is a lightweight HTTP server that gives good debug
output and is much more convenient than having to set up a standalone
server. Just run:

    plackup -Ilib -r

Visiting http://your.machines.ip.address:5000/ should now present you with
your own running instance of the MusicBrainz Server.

If you'd like a more permanent setup,
[the plackup documentation](https://metacpan.org/pod/plackup) may prove useful
in setting up a server such as nginx, using FastCGI.


Translations
------------

If you intend to run a server with translations, there are a few steps to follow     :

1.  Prerequisites

    Make sure gettext is installed (you need msgmerge and msgfmt, at least),
    and the transifex client 'tx'
    (http://help.transifex.com/features/client/index.html):

        sudo apt-get install gettext transifex-client

    Configure a username and password in ~/.transifexrc using the format listed
    on the above page.

2.  Change to the po directory

        cd po/

3.  Get translations

        tx pull -l {a list of languages you want to pull}

    This will download the .po files for your language(s) of choice to the po/
    folder with the correct filenames.

4.  Install translations

        make install

    This will compile and install the files to
    lib/LocaleData/{language}/LC\_MESSAGES/{domain}.mo

5.  Add the languages to MB\_LANGUAGES in DBDefs.pm. These should be formatted
    {lang}-{country}, e.g. 'es', or 'fr-ca', in a space-separated list.

6.  Ensure you have a system locale for any languages you want to use, and for
    some languages, be wary of https://rt.cpan.org/Public/Bug/Display.html?id=78     341

    For many languages, this will suffice:

        sudo apt-get install language-pack-{language code}

    To work around the linked CPAN bug, you may need to edit the file for Locale     ::Util
    to add entries to LANG2COUNTRY. Suggested ones include:

    * es => 'ES'
    * et => 'EE'
    * el => 'GR'
    * sl => 'SI' (this one is there in 1.20, but needs amendment)


Troubleshooting
---------------

If you have any difficulties, feel free to ask in #musicbrainz-devel on
irc.freenode.net, or email the [developer mailing list](http://lists.musicbrainz     .org/mailman/listinfo/musicbrainz-devel).

Please report any issues on our [bug tracker](http://tickets.musicbrainz.org/).

Good luck, and happy hacking!
[/share/MD0_DATA/.qpkg/musicbrainz-server] # more INSTALL.md
Installing MusicBrainz Server
=============================

The easiest method of installing a local MusicBrainz Server may be to download t     he
[pre-configured virtual machine](http://musicbrainz.org/doc/MusicBrainz_Server/S     etup),
if there is a current image available. In case you only need a replicated
database, you should consider using [mbslave](https://bitbucket.org/lalinsky/mbs     lave).

If you want to manually set up MusicBrainz Server from source, read on!

Prerequisites
-------------

1.  A Unix based operating system

    The MusicBrainz development team uses a variety of Linux distributions, but
    Mac OS X will work just fine, if you're prepared to potentially jump through
    some hoops. If you are running Windows we recommend you set up a Ubuntu virt     ual
    machine.

    **This document will assume you are using Ubuntu for its instructions.**

2.  Perl (at least version 5.10.1)

    Perl comes bundled with most Linux operating systems, you can check your
    installed version of Perl with:

        perl -v

3.  PostgreSQL (at least version 9.1)

    PostgreSQL is required, along with its development libraries. To install
    using packages run the following, replacing 9.x with the latest version.

        sudo apt-get install postgresql-9.x postgresql-server-dev-9.x postgresql     -contrib-9.x postgresql-plperl-9.x

    Alternatively, you may compile PostgreSQL from source, but then make sure to
    also compile the cube extension found in contrib/cube. The database import
    script will take care of installing that extension into the database when it
    creates the database for you.

4.  Git

    The MusicBrainz development team uses Git for their DVCS. To install Git,
    run the following:

        sudo apt-get install git-core

5.  Memcached

    By default the MusicBrainz server requires a Memcached server running on the
    same server with default settings. To install Memcached, run the following:

        sudo apt-get install memcached

    You can change the memcached server name and port, or configure other datast     ores
    in lib/DBDefs.pm.

6.  Redis

    Sessions are stored in Redis, so a running Redis server is
    required.  Redis can be installed with the
    following command and will not need any further configuration:

        sudo apt-get install redis-server

    The databases and key prefix used by musicbrainz can be configured
    in lib/DBDefs.pm.  The defaults should be fine if you don't use
    your redis install for anything else.

7.  Node.js

    Node.js is required to build (and optionally minify) our JavaScript and CSS.
    If you plan on accessing musicbrainz-server inside a web browser, you should
    install Node and its package manager, npm. Do this by running:

        sudo apt-get install nodejs npm

    Depending on your Ubuntu version, another package might be required, too:

        sudo apt-get install nodejs-legacy

    This is only needed where it exists, so a warning about the package not bein     g
    found is not a problem.

8.  Standard Development Tools

    In order to install some of the required Perl and Postgresql modules, you'll
    need a C compiler and make. You can install a basic set of development tools
    with the command:

        sudo apt-get install build-essential


Server configuration
--------------------

1.  Download the source code.

        git clone --recursive git://github.com/metabrainz/musicbrainz-server.git
        cd musicbrainz-server

2.  Modify the server configuration file.

        cp lib/DBDefs.pm.sample lib/DBDefs.pm

    Fill in the appropriate values for `MB_SERVER_ROOT` and `WEB_SERVER`.
    If you are using a reverse proxy, you should set the environment variable
    MUSICBRAINZ_USE_PROXY=1 when starting the server.
    This makes the server aware of it when checking for the canonical uri.

    Determine what type of server this will be and set `REPLICATION_TYPE` accord     ingly:

    1.  `RT_SLAVE` (mirror server)

[/share/MD0_DATA/.qpkg/musicbrainz-server] # vi lib/DBDefs.pm
# * RT_MASTER - This is a master replication server.  Changes are allowed, and
#               they result in replication packets being produced.
# * RT_SLAVE  - This is a slave replication server.  After loading a snapshot
#               produced by a master, the only changes allowed are those made
#               by applying the next replication packet in turn.  If the slave
#               server is not going to be used for development work, change
#               DB_STAGING_SERVER to 0.
#
#               A READONLY database connection must be configured if you
#               choose RT_SLAVE, as well as the usual READWRITE.
# * RT_STANDALONE - This server neither generates nor uses replication
#               packets.  Changes to the database are allowed.
sub REPLICATION_TYPE { RT_SLAVE }

# If you plan to use the RT_SLAVE setting (replicated data from MusicBrainz' Liv
# you must sign in at https://metabrainz.org and generate an access token to acc
# the replication packets. Enter the access token below:
# NOTE: DO NOT EXPOSE THIS ACCESS TOKEN PUBLICLY!
#
sub REPLICATION_ACCESS_TOKEN { "" }

################################################################################
# GPG Signature
I lib/DBDefs.pm [Modified] 124/495 25%
# * RT_MASTER - This is a master replication server.  Changes are allowed, and
#               they result in replication packets being produced.
# * RT_SLAVE  - This is a slave replication server.  After loading a snapshot
#               produced by a master, the only changes allowed are those made
#               by applying the next replication packet in turn.  If the slave
#               server is not going to be used for development work, change
#               DB_STAGING_SERVER to 0.
#
#               A READONLY database connection must be configured if you
#               choose RT_SLAVE, as well as the usual READWRITE.
# * RT_STANDALONE - This server neither generates nor uses replication
#               packets.  Changes to the database are allowed.
sub REPLICATION_TYPE { RT_SLAVE }

# If you plan to use the RT_SLAVE setting (replicated data from MusicBrainz' Live Dat
# you must sign in at https://metabrainz.org and generate an access token to access
# the replication packets. Enter the access token below:
# NOTE: DO NOT EXPOSE THIS ACCESS TOKEN PUBLICLY!
#
# sub REPLICATION_ACCESS_TOKEN { "" }

################################################################################
# GPG Signature
[/share/MD0_DATA/.qpkg/musicbrainz-server] # cd ../
[/share/MD0_DATA/.qpkg] # ls
BitTorrentSync/      Mylar/               SubMovies/           musicbrainz-server/
CloudLink/           NZBGet/              SuperSync/           musicstation/
CouchPotato2/        Optware/             SurveillanceStation/ nodejs/
DSv3/                PHP/                 Transmission/        photostation2/
Dropbox/             PlexMediaServer/     VideoStationPro/     phpMyAdmin/
GamezServer/         PostgreSQL/          autorun@             qmysql/
Headphones/          Python/              git/                 spotweb/
JRE/                 QMariaDB/            homewizard/          subliminal/
MalwareRemover/      QNAP-Plex-Fix/       maracopy/            update_qpkg_conf.sh*
Maraschino/          SickBeard-TVRage/    maraschino.cpy/
[/share/MD0_DATA/.qpkg] # cd GamezServer
[/share/MD0_DATA/.qpkg/GamezServer] # ls
GamezServer/    GamezServer.sh*
[/share/MD0_DATA/.qpkg/GamezServer] # ./GamezServer.sh restart
x86_64
Restarting GamezServer
x86_64
Shutting down GamezServer...
GamezServer is not running?
x86_64
GamezServer prestartup checks...
 Checking for git...  Found!
mkdir: Cannot create directory `/share/MD0_DATA/.qpkg/GamezServer/Repository/lib': No such file or directory
ln: /share/MD0_DATA/.qpkg/GamezServer/Repository/lib/python: No such file or directory
ln: /share/MD0_DATA/.qpkg/GamezServer/Repository/bin: No such file or directory
Updating GamezServer
HEAD is now at 9634af9 Fixed post process when there is no file
Already up-to-date.
Starting GamezServer
Info - Verifying DB Schema
Info - Building Tables
Info - Registering Background Processes
Info - Starting Service
[26/Aug/2015:15:03:47] ENGINE Bus STARTING
[26/Aug/2015:15:03:47] ENGINE Started monitor thread 'Monitor'.
[26/Aug/2015:15:03:47] ENGINE Started monitor thread '_TimeoutMonitor'.
[26/Aug/2015:15:03:47] ENGINE Started monitor thread 'Monitor'.
[26/Aug/2015:15:03:47] ENGINE Started monitor thread 'Monitor'.
[26/Aug/2015:15:03:47] ENGINE Started monitor thread 'Autoreloader'.
[26/Aug/2015:15:03:52] ENGINE Error in 'start' listener <bound method Server.start of <cherrypy._cpserver.Server object at 0xf701f74c>>
Traceback (most recent call last):
  File "/share/MD0_DATA/.qpkg/GamezServer/GamezServer/cherrypy/process/wspbus.py", line 205, in publish
    output.append(listener(*args, **kwargs))
  File "/share/MD0_DATA/.qpkg/GamezServer/GamezServer/cherrypy/_cpserver.py", line 168, in start
    ServerAdapter.start(self)
  File "/share/MD0_DATA/.qpkg/GamezServer/GamezServer/cherrypy/process/servers.py", line 170, in start
    wait_for_free_port(*self.bind_addr)
  File "/share/MD0_DATA/.qpkg/GamezServer/GamezServer/cherrypy/process/servers.py", line 438, in wait_for_free_port
    raise IOError("Port %r not free on %r" % (port, host))
IOError: Port 8085 not free on '127.0.0.1'

[26/Aug/2015:15:03:52] ENGINE Shutting down due to error in start listener:
Traceback (most recent call last):
  File "/share/MD0_DATA/.qpkg/GamezServer/GamezServer/cherrypy/process/wspbus.py", line 243, in start
    self.publish('start')
  File "/share/MD0_DATA/.qpkg/GamezServer/GamezServer/cherrypy/process/wspbus.py", line 223, in publish
    raise exc
ChannelFailures: IOError("Port 8085 not free on '127.0.0.1'",)

[26/Aug/2015:15:03:52] ENGINE Bus STOPPING
[26/Aug/2015:15:03:52] ENGINE HTTP Server cherrypy._cpwsgi_server.CPWSGIServer(('127.0.0.1', 8085)) already shut down
[26/Aug/2015:15:03:52] ENGINE Stopped thread 'Monitor'.
[26/Aug/2015:15:03:52] ENGINE Stopped thread 'Autoreloader'.
[26/Aug/2015:15:03:52] ENGINE Stopped thread 'Monitor'.
[26/Aug/2015:15:03:52] ENGINE Stopped thread '_TimeoutMonitor'.
[26/Aug/2015:15:03:52] ENGINE Stopped thread 'Monitor'.
[26/Aug/2015:15:03:52] ENGINE Bus STOPPED
[26/Aug/2015:15:03:52] ENGINE Bus EXITING
[26/Aug/2015:15:03:52] ENGINE Bus EXITED
[/share/MD0_DATA/.qpkg/GamezServer] # ps -e |grep Game
ps: invalid option -- e
BusyBox v1.10.3 (2012-02-17 10:53:18 UTC) multi-call binary

Usage: ps

Report process status

Options:
        w       Wide output

[/share/MD0_DATA/.qpkg/GamezServer] # ps |grep Game
 9616 admin     2260 S    grep Game
22700 admin     2572 S    /bin/sh /etc/rcS.d/QS127GamezServer start
22832 admin     141m S    /usr/bin/python2.7 GamezServer.py --daemon --datadir /shar
[/share/MD0_DATA/.qpkg/GamezServer] # kill 22832
[/share/MD0_DATA/.qpkg/GamezServer] # ps |grep Game
11272 admin     2260 S    grep Game
[/share/MD0_DATA/.qpkg/GamezServer] # ./GamezServer.sh start
x86_64
GamezServer prestartup checks...
 Checking for git...  Found!
mkdir: Cannot create directory `/share/MD0_DATA/.qpkg/GamezServer/Repository/lib': No such file or directory
ln: /share/MD0_DATA/.qpkg/GamezServer/Repository/lib/python: No such file or directory
ln: /share/MD0_DATA/.qpkg/GamezServer/Repository/bin: No such file or directory
Updating GamezServer
HEAD is now at 9634af9 Fixed post process when there is no file
Already up-to-date.
Starting GamezServer
Info - Verifying DB Schema
Info - Building Tables
Info - Registering Background Processes
Info - Starting Service
[26/Aug/2015:15:05:17] ENGINE Bus STARTING
[26/Aug/2015:15:05:17] ENGINE Started monitor thread 'Monitor'.
[26/Aug/2015:15:05:17] ENGINE Started monitor thread '_TimeoutMonitor'.
[26/Aug/2015:15:05:17] ENGINE Started monitor thread 'Monitor'.
[26/Aug/2015:15:05:17] ENGINE Started monitor thread 'Monitor'.
[26/Aug/2015:15:05:17] ENGINE Started monitor thread 'Autoreloader'.
[26/Aug/2015:15:05:17] ENGINE Serving on http://127.0.0.1:8085
[26/Aug/2015:15:05:17] ENGINE Bus STARTED
^C[26/Aug/2015:15:07:07] ENGINE Keyboard Interrupt: shutting down bus
[26/Aug/2015:15:07:07] ENGINE Bus STOPPING
[26/Aug/2015:15:07:07] ENGINE HTTP Server cherrypy._cpwsgi_server.CPWSGIServer(('127.0.0.1', 8085)) shut down
[26/Aug/2015:15:07:07] ENGINE Stopped thread 'Monitor'.
[26/Aug/2015:15:07:07] ENGINE Stopped thread 'Autoreloader'.
[26/Aug/2015:15:07:07] ENGINE Stopped thread 'Monitor'.
[26/Aug/2015:15:07:07] ENGINE Stopped thread '_TimeoutMonitor'.
[26/Aug/2015:15:07:07] ENGINE Stopped thread 'Monitor'.
[26/Aug/2015:15:07:07] ENGINE Bus STOPPED
[26/Aug/2015:15:07:07] ENGINE Bus EXITING
[26/Aug/2015:15:07:07] ENGINE Bus EXITED
[26/Aug/2015:15:07:07] ENGINE Waiting for child threads to terminate...
[/share/MD0_DATA/.qpkg/GamezServer] # cat GamezServer.sh
#! /bin/sh

QPKG_NAME=GamezServer
QPKG_DIR=$(/sbin/getcfg $QPKG_NAME Install_Path -f /etc/config/qpkg.conf)
PID_FILE=/tmp/$QPKG_NAME.pid
DAEMON=/usr/bin/python2.7
DAEMON_OPTS="GamezServer.py --daemon --datadir $QPKG_DIR/config --pidfile $PID_FILE"

#Determin Arch
ver="none"
if /bin/uname -m | grep "armv5tejl"; then ver="arm"; fi
if /bin/uname -m | grep "armv5tel"; then ver="arm"; fi
if /bin/uname -m | grep "i686"; then ver="x86"; fi
if /bin/uname -m | grep "x86_64"; then ver="x86"; fi
if /bin/uname -m | grep "armv7l"; then ver="x31"; fi
arch="$(/bin/uname -m)"
[ $ver = "none" ] && err_log "Could not determine architecture $arch"
export PATH=${QPKG_DIR}/${ver}/bin-utils:/Apps/bin:/usr/local/bin:$PATH
export LD_LIBRARY_PATH=${QPKG_DIR}/${ver}/lib:/usr/local/lib:$LD_LIBRARY_PATH
export PYTHONPATH=$QPKG_DIR/Repository/lib/python

CheckQpkgEnabled() { #Is the QPKG enabled? if not exit the script
        if [ $(/sbin/getcfg ${QPKG_NAME} Enable -u -d FALSE -f /etc/config/qpkg.conf) = UNKNOWN ]; then
                /sbin/setcfg ${QPKG_NAME} Enable TRUE -f /etc/config/qpkg.conf
        elif [ $(/sbin/getcfg ${QPKG_NAME} Enable -u -d FALSE -f /etc/config/qpkg.conf) != TRUE ]; then
                /bin/echo "${QPKG_NAME} is disabled."
                exit 1
        fi
        if [ `/sbin/getcfg "git" Enable -u -d FALSE -f /etc/config/qpkg.conf` = UNKNOWN ]; then
                /sbin/setcfg "git" Enable TRUE -f /etc/config/qpkg.conf
        elif [ `/sbin/getcfg "git" Enable -u -d FALSE -f /etc/config/qpkg.conf` != TRUE ]; then
                echo "git is disabled."
                exit 1
        fi
        if [ `/sbin/getcfg "Python" Enable -u -d FALSE -f /etc/config/qpkg.conf` = UNKNOWN ]; then
                /sbin/setcfg "Python" Enable TRUE -f /etc/config/qpkg.conf
        elif [ `/sbin/getcfg "Python" Enable -u -d FALSE -f /etc/config/qpkg.conf` != TRUE ]; then
                echo "Python is disabled."
                exit 1
        fi
        [ -x /Apps/bin/git ] || /etc/init.d/git.sh restart && sleep 2
        [ -x $DAEMON ] || /etc/init.d/python.sh restart && sleep 2
}

ConfigPython(){ #checks if the daemon exists and will link /usr/bin/python to it
        #python dependency checking
        if [ ! -x $DAEMON ]; then
                /sbin/write_log "Failed to start $QPKG_NAME, $DAEMON was not found. Please re-install the Pythton qpkg." 1
                exit 1
        fi
        [ -d $QPKG_DIR/Repository/lib ] || /bin/mkdir $QPKG_DIR/Repository/lib
        [ -d $QPKG_DIR/Repository/lib/python ] || ln -sf $QPKG_DIR/${ver}/python $QPKG_DIR/Repository/lib/python
        [ -d $QPKG_DIR/Repository/bin ] || ln -sf $QPKG_DIR/${ver}/bin $QPKG_DIR/Repository/bin
       if [ $ver = "x31" ]; then
                PY_DIR=$(/sbin/getcfg Python Install_Path -f /etc/config/qpkg.conf)
                [ -f ${PY_DIR}/lib/python2.7/lib-dynload/_ctypes.so ] || cp $QPKG_DIR/${ver}/lib/_ctypes.so ${PY_DIR}/lib/python2.7/lib-dynload/_ctypes.so
                [ -f ${PY_DIR}/lib/python2.7/lib-dynload/_sqlite3.so ] || cp $QPKG_DIR/${ver}/lib/_sqlite3.so ${PY_DIR}/lib/python2.7/lib-dynload/_sqlite3.so
                [ -f ${PY_DIR}/lib/python2.7/lib-dynload/_ssl.so ] || cp $QPKG_DIR/${ver}/lib/_ssl.so ${PY_DIR}/lib/python2.7/lib-dynload/_ssl.so
                [ -f ${PY_DIR}/lib/python2.7/lib-dynload/zlib.so ] || cp $QPKG_DIR/${ver}/lib/zlib.so ${PY_DIR}/lib/python2.7/lib-dynload/zlib.so
        fi
}

CheckForGit(){ #Does git exist?
        /bin/echo -n " Checking for git..."
        if [ ! -f /Apps/bin/git ]; then
                if [ -x /etc/init.d/git.sh ]; then
                        /bin/echo "  Starting git..."
                        /etc/init.d/git.sh start
                        sleep 2
                else #catch all
                        /bin/echo "  No git qpkg found, please install it"
                        /sbin/write_log "Failed to start $QPKG_NAME, no git found." 1
                        exit 1
                fi
        else
                /bin/echo "  Found!"
        fi
}

CheckQpkgRunning() { #Is the QPKG already running? if so, exit the script
        if [ -f $PID_FILE ]; then
                #grab pid from pid file
                Pid=$(/bin/cat $PID_FILE)
                if [ -d /proc/$Pid ]; then
                        /bin/echo " $QPKG_NAME is already running"
                        exit 1
                fi
        fi
        #ok, we survived so the QPKG should not be running
}

UpdateQpkg(){ # does a git pull to update to the latest code
        /bin/echo "Updating $QPKG_NAME"
        GIT_URL="git://github.com/mldesk/GamezServer.git"
        GIT_URL1="http://github.com/mldesk/GamezServer.git"
        #git clone/pull the qpkg
        [ -d $QPKG_DIR/$QPKG_NAME/.git ] || git clone $GIT_URL $QPKG_DIR/$QPKG_NAME || git clone $GIT_URL1 $QPKG_DIR/$QPKG_NAME
        cd $QPKG_DIR/$QPKG_NAME && git reset --hard HEAD && git pull && /bin/sync
}

StartQpkg(){ #Starts the qpkg
        /bin/echo "Starting $QPKG_NAME"
        cd $QPKG_DIR/$QPKG_NAME
        [ -d $QPKG_DIR/$QPKG_NAME/lib/unrar2 ] && [ ! -f $QPKG_DIR/$QPKG_NAME/lib/unrar2/unrar ] && /bin/ln -sf ${QPKG_DIR}/${ver}/bin-utils/unrar $QPKG_DIR/$QPKG_NAME/lib/unrar2/unrar
        PATH=${PATH} ${DAEMON} ${DAEMON_OPTS}
}

ShutdownQPKG() { #kills a proces based on a PID in a given PID file
        /bin/echo "Shutting down ${QPKG_NAME}... "
        if [ -f $PID_FILE ]; then
                #grab pid from pid file
                Pid=$(/bin/cat $PID_FILE)
                i=0
                /bin/kill $Pid
                /bin/echo -n " Waiting for ${QPKG_NAME} to shut down: "
                while [ -d /proc/$Pid ]; do
                        sleep 1
                        let i+=1
                        /bin/echo -n "$i, "
                        if [ $i = 45 ]; then
                                /bin/echo " Tired of waiting, killing ${QPKG_NAME} now"
                                /bin/kill -9 $Pid
                                /bin/rm -f $PID_FILE
                                exit 1
                        fi
                done
                /bin/rm -f $PID_FILE
                /bin/echo "Done"
        else
                /bin/echo "${QPKG_NAME} is not running?"
        fi
}

case "$1" in
  start)
        CheckQpkgEnabled #Check if the QPKG is enabled, else exit
        /bin/echo "$QPKG_NAME prestartup checks..."
        CheckQpkgRunning #Check if the QPKG is not running, else exit
        CheckForGit      #Check for git, start qpkg if needed
        ConfigPython     #Check for Python, exit if not found
        UpdateQpkg               #do a git pull
        StartQpkg                #Finally Start the qpkg

        ;;
  stop)
        ShutdownQPKG
        ;;
  restart)
        echo "Restarting $QPKG_NAME"
        $0 stop
        $0 start
        ;;
  *)
        N=/etc/init.d/$QPKG_NAME.sh
        echo "Usage: $N {start|stop|restart}" >&2
        exit 1
        ;;
esac
[/share/MD0_DATA/.qpkg/GamezServer] # ls
GamezServer/    GamezServer.sh*
[/share/MD0_DATA/.qpkg/GamezServer] # mv GamezServer.sh GamezServer.old
[/share/MD0_DATA/.qpkg/GamezServer] # ls
GamezServer/     GamezServer.old*                                   2.sh GamezServer.shr.sh                                cp ../CouchPotato2/CouchPotato.sh GamezServ
[/share/MD0_DATA/.qpkg/GamezServer] # ls
GamezServer/     GamezServer.old* GamezServer.sh*
[/share/MD0_DATA/.qpkg/GamezServer] # vi GamezServer.sh
#! /bin/sh

QPKG_NAME=GamezServer
QPKG_DIR=$(/sbin/getcfg $QPKG_NAME Install_Path -f /etc/config/qpkg.conf)
PATH="/opt/bin:/usr/bin/:$PATH"
PID_FILE="$QPKG_DIR/config/gamezserver.pid"
DAEMON=/opt/bin/python2.7
DAEMON_OPTS="GamezServer.py --data_dir $QPKG_DIR/config --daemon --pid_file $PID_FILE

CheckQpkgEnabled() { #Is the QPKG enabled? if not exit the script
        if [ $(/sbin/getcfg ${QPKG_NAME} Enable -u -d FALSE -f /etc/config/qpkg.conf)
                /sbin/setcfg ${QPKG_NAME} Enable TRUE -f /etc/config/qpkg.conf
        elif [ $(/sbin/getcfg ${QPKG_NAME} Enable -u -d FALSE -f /etc/config/qpkg.con
                /bin/echo "${QPKG_NAME} is disabled."
                exit 1
        fi
}

ConfigPython(){ #checks if the daemon exists and will link /usr/bin/python to it
        #python dependency checking
        if [ ! -x $DAEMON ]; then
                /sbin/write_log "Faile./GamezServer.sh restart
Restarting GamezServer
Shutting down GamezServer...
GamezServer is not running?
GamezServer prestartup checks...
 Checking for /opt...  Found!
Updating GamezServer
./GamezServer.sh: line 65: /opt/bin/git: No such file or directory
Starting GamezServer
/opt/bin/python2.7: can't open file 'GamezServer.py': [Errno 2] No such file or directory
[/share/MD0_DATA/.qpkg/GamezServer] # ls
GamezServer/     GamezServer.old* GamezServer.sh*
[/share/MD0_DATA/.qpkg/GamezServer] # cd GamezServer
[/share/MD0_DATA/.qpkg/GamezServer/GamezServer] # ls
GamezServer/                    Logs/
GamezServer.Python.pyproj       OpenSSL/
GamezServer.Python.pyproj.user  README.md
GamezServer.Python.sln          cherrypy/
GamezServer.db                  dexml/
GamezServer.ini                 lxml/
GamezServer.py                  post-process/
[/share/MD0_DATA/.qpkg/GamezServer/GamezServer] # cd ..
[/share/MD0_DATA/.qpkg/GamezServer] # vi GamezServer.sh
#! /bin/sh

QPKG_NAME=GamezServer
QPKG_DIR=$(/sbin/getcfg $QPKG_NAME Install_Path -f /etc/config/qpkg.conf)
PATH="/opt/bin:/usr/bin/:$PATH"
PID_FILE="$QPKG_DIR/config/gamezserver.pid"
DAEMON=/opt/bin/python2.7
DAEMON_OPTS="GamezServer.py --data_dir $QPKG_DIR/config --daemon --pid_file $PID_FILE

CheckQpkgEnabled() { #Is the QPKG enabled? if not exit the script
        if [ $(/sbin/getcfg ${QPKG_NAME} Enable -u -d FALSE -f /etc/config/qpkg.conf)
                /sbin/setcfg ${QPKG_NAME} Enable TRUE -f /etc/config/qpkg.conf
        elif [ $(/sbin/getcfg ${QPKG_NAME} Enable -u -d FALSE -f /etc/config/qpkg.con
                /bin/echo "${QPKG_NAME} is disabled."
                exit 1
        fi
}

ConfigPython(){ #checks if the daemon exists and will link /usr/bin/python to it
        #python dependency checking
        if [ ! -x $DAEMON ]; then
                /sbin/write_log "Failed to start $QPKG_NAME, $DAEMON was not found. P
                exit 1
[/share/MD0_DATA/.qpkg/GamezServer] # ./GamezServer.sh restart
Restarting GamezServer
Shutting down GamezServer...
GamezServer is not running?
GamezServer prestartup checks...
 Checking for /opt...  Found!
Updating GamezServer
./GamezServer.sh: line 65: /opt/bin/git: No such file or directory
Starting GamezServer
Info - Verifying DB Schema
Info - Building Tables
Info - Registering Background Processes
Info - Starting Service
[26/Aug/2015:16:02:35] ENGINE Bus STARTING
[26/Aug/2015:16:02:35] ENGINE Started monitor thread '_TimeoutMonitor'.
[26/Aug/2015:16:02:35] ENGINE Started monitor thread 'Monitor'.
[26/Aug/2015:16:02:35] ENGINE Started monitor thread 'Monitor'.
[26/Aug/2015:16:02:35] ENGINE Started monitor thread 'Monitor'.
[26/Aug/2015:16:02:35] ENGINE Started monitor thread 'Autoreloader'.
[26/Aug/2015:16:02:35] ENGINE Serving on http://127.0.0.1:8085
[26/Aug/2015:16:02:35] ENGINE Bus STARTED

^C[26/Aug/2015:16:04:38] ENGINE Keyboard Interrupt: shutting down bus
[26/Aug/2015:16:04:38] ENGINE Bus STOPPING
[26/Aug/2015:16:04:38] ENGINE HTTP Server cherrypy._cpwsgi_server.CPWSGIServer(('127.0.0.1', 8085)) shut down
[26/Aug/2015:16:04:38] ENGINE Stopped thread '_TimeoutMonitor'.
[26/Aug/2015:16:04:38] ENGINE Stopped thread 'Autoreloader'.
[26/Aug/2015:16:04:38] ENGINE Stopped thread 'Monitor'.
[26/Aug/2015:16:04:38] ENGINE Stopped thread 'Monitor'.
[26/Aug/2015:16:04:38] ENGINE Stopped thread 'Monitor'.
[26/Aug/2015:16:04:38] ENGINE Bus STOPPED
[26/Aug/2015:16:04:38] ENGINE Bus EXITING
[26/Aug/2015:16:04:38] ENGINE Bus EXITED
[26/Aug/2015:16:04:38] ENGINE Waiting for child threads to terminate...
[/share/MD0_DATA/.qpkg/GamezServer] # ls
GamezServer/                    GamezServer.sh*
GamezServer.Python.pyproj       Logs/
GamezServer.Python.pyproj.user  OpenSSL/
GamezServer.Python.sln          README.md
GamezServer.db                  cherrypy/
GamezServer.ini                 dexml/
GamezServer.old*                lxml/
GamezServer.py                  post-process/
[/share/MD0_DATA/.qpkg/GamezServer] # cat README.md
# Gamez Server
Gamez Server is currently in pre-release development. The 1.0.0 release is slated for 6/1/2015. There may be bugs and minimal functionality in the application.

Gamez Server is an automated downloader for video games. The user adds the games they wish to download and Gamez will attempt to find the game and download it.

Requirements:
* Python 2.7
* Post processing currently only supported on Windows

Current Functionality:
* Syncs Games from the Game DB
* Supports all platforms on the Game DB
* Add Individual Game
* Add All Games by Platform
* Configurable Header
* Configurable Footer
* Sabnzbd+ Integration
* Usenet-Crawler Search Provider
* Simple Post Processing
* Force Search
* Force Search for new (previously un-snatched)
* Configurable Search Provider Search Order
* Automated Upgrade Search and One-Click Upgrade
* Auto-Searches Game When Added
* Configuration to always try new version
* Configuration to auto-open browser on start
* Status Management

Future Plans
* Additional Search Providers
* Add Blackhole Torrent Downloader
* Add Notifications
* Add Configuration to limit extensions for files copied during post process
* Add Configuration to delete source folder after post processing is complete
* Add Cover Art
* Add Upcoming Releases Page
[/share/MD0_DATA/.qpkg/GamezServer] # ls
GamezServer/                    GamezServer.sh*
GamezServer.Python.pyproj       Logs/
GamezServer.Python.pyproj.user  OpenSSL/
GamezServer.Python.sln          README.md
GamezServer.db                  cherrypy/
GamezServer.ini                 dexml/
GamezServer.old*                lxml/
GamezServer.py                  post-process/
[/share/MD0_DATA/.qpkg/GamezServer] # cat GamezServer.ini
[global]
server.socket_host="127.0.0.1"
server.socket_port=8085
[/share/MD0_DATA/.qpkg/GamezServer] # ps |grep Gam
28002 admin     2260 S    grep Gam
[/share/MD0_DATA/.qpkg/GamezServer] # cd ..
-sh: cd: ..: No such file or directory
[/share/MD0_DATA/.qpkg/GamezServer] # cd ..
-sh: cd: ..: No such file or directory
[/share/MD0_DATA/.qpkg/GamezServer] # cd ..
-sh: cd: ..: No such file or directory
[/share/MD0_DATA/.qpkg/GamezServer] # cd
[~] # ls
Library@            index_default.html
[~] # cd /share/MD0_DATA/.qpkg
[/share/MD0_DATA/.qpkg] # ls
BitTorrentSync/      NZBGet/              SuperSync/           musicstation/
CloudLink/           Optware/             SurveillanceStation/ nodejs/
CouchPotato2/        PHP/                 Transmission/        photostation2/
DSv3/                PlexMediaServer/     VideoStationPro/     phpMyAdmin/
Dropbox/             PostgreSQL/          autorun@             qmysql/
Headphones/          Python/              git/                 spotweb/
JRE/                 QMariaDB/            homewizard/          subliminal/
MalwareRemover/      QNAP-Plex-Fix/       maracopy/            update_qpkg_conf.sh*
Maraschino/          SickBeard-TVRage/    maraschino.cpy/
Mylar/               SubMovies/           musicbrainz-server/
[/share/MD0_DATA/.qpkg] # cd Si*
[/share/MD0_DATA/.qpkg/SickBeard-TVRage] # ls
Repository/          arm/                 sickbeard-tvrage.sh* x86/
SickBeard-TVRage/    config/              x31/
[/share/MD0_DATA/.qpkg/SickBeard-TVRage] # ls -la
drwxr-xr-x    8 admin    administ      4096 Jan  7  2015 ./
drwxrwxrwx   39 admin    administ      4096 Aug 26 17:21 ../
-rw-r--r--    1 admin    administ     58854 Jan  7  2015 .list
-rw-r--r--    1 admin    administ      2971 Oct 20  2014 .qpkg_icon.gif
-rw-r--r--    1 admin    administ      3997 Oct 20  2014 .qpkg_icon_80.gif
-rw-r--r--    1 admin    administ      2371 Oct 20  2014 .qpkg_icon_gray.gif
-rwxr-xr-x    1 admin    administ       864 Jan  7  2015 .uninstall.sh*
drwxr-xr-x    3 admin    administ      4096 Jan  7  2015 Repository/
drwxr-xr-x   10 admin    administ      4096 Aug 25 15:30 SickBeard-TVRage/
drwxr-xr-x    6 admin    administ      4096 Nov  8  2014 arm/
drwxr-xr-x    5 admin    administ      4096 Aug 26 17:09 config/
-rwxr-xr-x    1 admin    administ      5703 Dec 23  2014 sickbeard-tvrage.sh*
drwxr-xr-x    6 admin    administ      4096 Nov  8  2014 x31/
drwxr-xr-x    6 admin    administ      4096 Nov  8  2014 x86/
[/share/MD0_DATA/.qpkg/SickBeard-TVRage] # cd Si*
[/share/MD0_DATA/.qpkg/SickBeard-TVRage/SickBeard-TVRage] # ls -la
drwxr-xr-x   10 admin    administ      4096 Aug 25 15:30 ./
drwxr-xr-x    8 admin    administ      4096 Jan  7  2015 ../
drwxr-xr-x    8 admin    administ      4096 Aug 26 16:09 .git/
-rw-------    1 admin    administ      1221 Aug 18 15:08 .gitattributes
-rw-r--r--    1 admin    administ       762 Apr 17 15:26 .gitignore
-rw-------    1 admin    administ       334 Aug  5 09:14 .travis.yml
-rw-------    1 admin    administ        98 Aug  5 09:14 CHANGES.md
-rw-r--r--    1 admin    administ     35130 Jan  7  2015 COPYING.txt
-rwx------    1 admin    administ     22117 Aug 25 15:30 SickBeard.py*
-rw-------    1 admin    administ       748 Aug  5 09:14 TODO.txt
drwxr-xr-x    3 admin    administ      4096 Aug 17 14:12 autoProcessTV/
-rw-r--r--    1 admin    administ      6184 Aug 17 14:12 contributing.md
-rw-r--r--    1 admin    administ      8950 Jan  7  2015 googlecode_upload.py
drwxr-xr-x    3 admin    administ      4096 Jan  7  2015 gui/
drwxr-xr-x   55 admin    administ      4096 Aug 17 14:12 lib/
-rw-------    1 admin    administ        95 Aug  5 09:14 news.md
-rw-r--r--    1 admin    administ      2468 Aug 17 14:12 readme.md
-rw-r--r--    1 admin    administ        23 Aug 17 14:12 requirements.txt
drwx------    2 admin    administ      4096 Aug 25 15:30 runscripts/
-rw-------    1 admin    administ      8638 Aug  5 09:14 setup.py
drwxr-xr-x    9 admin    administ      4096 Aug 25 15:31 sickbeard/
drwxr-xr-x    2 admin    administ      4096 Aug  5 09:14 tests/
drwxr-xr-x    4 admin    administ      4096 Jun 27 21:17 tornado/
-rw-------    1 admin    administ      2741 Aug  5 09:14 updater.py
[/share/MD0_DATA/.qpkg/SickBeard-TVRage/SickBeard-TVRage] # more SickBeard.py
#!/usr/bin/env python2.7
# Author: Nic Wolfe <nic@wolfeden.ca>
# URL: http://code.google.com/p/sickbeard/
#
# This file is part of SickRage.
#
# SickRage is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SickRage is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SickRage.  If not, see <http://www.gnu.org/licenses/>.

# Check needed software dependencies to nudge users to fix their setup
from __future__ import with_statement

--More-- (3% of 22117 bytes)
[/share/MD0_DATA/.qpkg/SickBeard-TVRage/SickBeard-TVRage] # more SickBeard.py
#!/usr/bin/env python2.7
# Author: Nic Wolfe <nic@wolfeden.ca>
# URL: http://code.google.com/p/sickbeard/
#
# This file is part of SickRage.
#
# SickRage is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SickRage is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SickRage.  If not, see <http://www.gnu.org/licenses/>.

# Check needed software dependencies to nudge users to fix their setup
from __future__ import with_statement

import codecs
codecs.register(lambda name: codecs.lookup('utf-8') if name == 'cp65001' else None)

import time
import signal
import sys
import subprocess
import traceback

import os
sys.path.insert(1, os.path.abspath(os.path.join(os.path.dirname(__file__), 'lib')))

import shutil
import shutil_custom

shutil.copyfile = shutil_custom.copyfile_custom

if sys.version_info < (2, 7):
    print "Sorry, requires Python 2.7.x"
    sys.exit(1)

# We only need this for compiling an EXE and I will just always do that on 2.7+
if sys.hexversion >= 0x020600F0:
    from multiprocessing import freeze_support  # @UnresolvedImport

import certifi
for env_cert_var in ['REQUESTS_CA_BUNDLE', 'CURL_CA_BUNDLE']:
    ca_cert_loc = os.environ.get(env_cert_var)
    if (not isinstance(ca_cert_loc, basestring)) or (not os.path.isfile(ca_cert_loc)):
        os.environ[env_cert_var] = certifi.where()

if sys.version_info >= (2, 7, 9):
    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context
else:
    try:
        import cryptography
    except ImportError:
        try:
            from OpenSSL.version import __version__ as pyOpenSSL_Version
            if int(pyOpenSSL_Version.replace('.', '')[:3]) > 13:
                raise ImportError
        except ImportError:
            print('\nSNI is disabled with pyOpenSSL >= 0.14 when the cryptography module is missing,\n' +
                    'you will encounter SSL errors with HTTPS! To fix this issue:\n' +
                    'pip install pyopenssl==0.13.1 (easy) or pip install cryptography (pita)')


import locale
import datetime
import threading
import getopt

import sickbeard
from sickbeard import db, logger, network_timezones, failed_history, name_cache
from sickbeard.tv import TVShow
from sickbeard.webserveInit import SRWebServer
from sickbeard.databases.mainDB import MIN_DB_VERSION, MAX_DB_VERSION
from sickbeard.event_queue import Events
from configobj import ConfigObj
from sickbeard import encodingKludge as ek

throwaway = datetime.datetime.strptime('20110101', '%Y%m%d')

signal.signal(signal.SIGINT, sickbeard.sig_handler)
signal.signal(signal.SIGTERM, sickbeard.sig_handler)


class SickRage(object):
    def __init__(self):
        # system event callback for shutdown/restart
        sickbeard.events = Events(self.shutdown)

        # daemon constants
        self.runAsDaemon = False
        self.CREATEPID = False
        self.PIDFILE = ''

        # webserver constants
        self.webserver = None
        self.forcedPort = None
        self.noLaunch = False

    def help_message(self):
        """
        print help message for commandline options
        """
        help_msg = "\n"
        help_msg += "Usage: " + sickbeard.MY_FULLNAME + " <option> <another option>\n"
        help_msg += "\n"
        help_msg += "Options:\n"
        help_msg += "\n"
        help_msg += "    -h          --help              Prints this message\n"
        help_msg += "    -q          --quiet             Disables logging to console\n"
        help_msg += "                --nolaunch          Suppress launching web browser on startup\n"

        if sys.platform == 'win32' or sys.platform == 'darwin':
            help_msg += "    -d          --daemon            Running as real daemon is not supported on Windows\n"
            help_msg += "                                    On Windows and MAC, --daemon is substituted with: --quiet --nolaunch\n"
        else:
            help_msg += "    -d          --daemon            Run as double forked daemon (includes options --quiet --nolaunch)\n"
            help_msg += "                --pidfile=<path>    Combined with --daemon creates a pidfile (full path including filename)\n"
--More-- (20% of 22117 bytes)
[/share/MD0_DATA/.qpkg/SickBeard-TVRage/SickBeard-TVRage] #
[/share/MD0_DATA/.qpkg/SickBeard-TVRage/SickBeard-TVRage] #
[/share/MD0_DATA/.qpkg/SickBeard-TVRage/SickBeard-TVRage] # more SickBeard.py
#!/usr/bin/env python2.7
# Author: Nic Wolfe <nic@wolfeden.ca>
# URL: http://code.google.com/p/sickbeard/
#
# This file is part of SickRage.
#
# SickRage is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SickRage is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SickRage.  If not, see <http://www.gnu.org/licenses/>.

# Check needed software dependencies to nudge users to fix their setup
from __future__ import with_statement

import codecs
codecs.register(lambda name: codecs.lookup('utf-8') if name == 'cp65001' else None)

import time
import signal
import sys
import subprocess
import traceback

import os
sys.path.insert(1, os.path.abspath(os.path.join(os.path.dirname(__file__), 'lib')))

import shutil
import shutil_custom

shutil.copyfile = shutil_custom.copyfile_custom

if sys.version_info < (2, 7):
    print "Sorry, requires Python 2.7.x"
    sys.exit(1)

# We only need this for compiling an EXE and I will just always do that on 2.7+
if sys.hexversion >= 0x020600F0:
    from multiprocessing import freeze_support  # @UnresolvedImport

import certifi
for env_cert_var in ['REQUESTS_CA_BUNDLE', 'CURL_CA_BUNDLE']:
    ca_cert_loc = os.environ.get(env_cert_var)
    if (not isinstance(ca_cert_loc, basestring)) or (not os.path.isfile(ca_cert_loc)):
        os.environ[env_cert_var] = certifi.where()

if sys.version_info >= (2, 7, 9):
    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context
else:
    try:
        import cryptography
    except ImportError:
        try:
            from OpenSSL.version import __version__ as pyOpenSSL_Version
            if int(pyOpenSSL_Version.replace('.', '')[:3]) > 13:
                raise ImportError
        except ImportError:
            print('\nSNI is disabled with pyOpenSSL >= 0.14 when the cryptography module is missing,\n' +
                    'you will encounter SSL errors with HTTPS! To fix this issue:\n' +
                    'pip install pyopenssl==0.13.1 (easy) or pip install cryptography (pita)')

import locale
import datetime
import threading
import getopt

import sickbeard
from sickbeard import db, logger, network_timezones, failed_history, name_cache
from sickbeard.tv import TVShow
from sickbeard.webserveInit import SRWebServer
from sickbeard.databases.mainDB import MIN_DB_VERSION, MAX_DB_VERSION
from sickbeard.event_queue import Events
from configobj import ConfigObj
from sickbeard import encodingKludge as ek

throwaway = datetime.datetime.strptime('20110101', '%Y%m%d')

signal.signal(signal.SIGINT, Gamez.sig_handler)
signal.signal(signal.SIGTERM, Gamez.sig_handler)

class Gamez(object):
    def __init__(self):
        # system event callback for shutdown/restart
        Gamez.events = Events(self.shutdown)
        
        # deamon constants
        self.runAsDaemon = False
        self.CREATEPID = False
        self.PIDFILE = ''
        
        # webserver constants
        self.webserver = None
        self.forcedPort = None
        self.noLaunch = False
        
    def help_message(self):
         """
         print help message for commandlin optione
         """
         help_msg = "\n"
         help_msg += "Usage: " + Gamez.MY_FULLNAME + " <options>\n" 
         help_msg += "\n"
         # lot more of help text
         return help_msg
         
    def start(self):
        # do some preliminary stuff
        Gamez.MY_FULLNAME = os.path.normpath(os.path.abspath(__file__))
        Gamez.MY_NAME = os.path.basename(Gamez.MY_FULLNAME)
        Gamez.PROG_DIR = os.path.dirname(Gamez.MY_FULLNAME)
        Gamez.DATA_DIR = Gamez.PROG_DIR
        Gamez.MY_ARGS = sys.argv[1:]
        Gamez.SYS_ENCODING = None
        
        try 
            locale.setlocale(locale.LC_ALL, "")
            Gamez.SYS_ENCODING = locale.getpreferredencoding()
        except (locale.Error, IOError):
            pass
       # For OSes that are poorly configured I'll just randomly force UTF-8
        if not Gamez.SYS_ENCODING or Gamez.SYS_ENCODING in ('ANSI_X3.4-1968', 'US-ASCII', 'ASCII'):
            Gamez.SYS_ENCODING = 'UTF-8'

        if not hasattr(sys, "setdefaultencoding"):
            reload(sys)

        if sys.platform == 'win32':
            if sys.getwindowsversion()[0] >= 6 and sys.stdout.encoding == 'cp65001':
                Gamez.SYS_ENCODING = 'UTF-8'

        try:
            # pylint: disable=E1101
            # On non-unicode builds this will raise an AttributeError, if encoding type is not valid it throws a LookupError
            sys.setdefaultencoding(Gamez.SYS_ENCODING)
        except:
            sys.exit("Sorry, you MUST add the Gamez folder to the PYTHONPATH environment variable\n" +
                     "or find another way to force Python to use " + Gamez.SYS_ENCODING + " for string encoding.")

        # Need console logging for SickBeard.py and SickBeard-console.exe
        self.consoleLogging = (not hasattr(sys, "frozen")) or (Gamez.MY_NAME.lower().find('-console') > 0)

        # Rename the main thread
        threading.currentThread().name = "MAIN"

        try:
            opts, args = getopt.getopt(sys.argv[1:], "hfqdp::",
                                       ['help', 'quiet', 'nolaunch', 'daemon', 'pidfile=', 'port=',
                                        'datadir=', 'config=', 'noresize'])  # @UnusedVariable
        except getopt.GetoptError:
            sys.exit(self.help_message())

        for o, a in opts:
            # Prints help message
            if o in ('-h', '--help'):
                sys.exit(self.help_message())

            # For now we'll just silence the logging
            if o in ('-q', '--quiet'):
                self.consoleLogging = False

            # Suppress launching web browser
            # Needed for OSes without default browser assigned
            # Prevent duplicate browser window when restarting in the app
            if o in ('--nolaunch',):
                self.noLaunch = True

            # Override default/configured port
            if o in ('-p', '--port'):
                try:
                    self.forcedPort = int(a)
                except ValueError:
                    sys.exit("Port: " + str(a) + " is not a number. Exiting.")

            # Run as a double forked daemon
            if o in ('-d', '--daemon'):
                self.runAsDaemon = True
                # When running as daemon disable consoleLogging and don't start browser
                self.consoleLogging = False
                self.noLaunch = True

                if sys.platform == 'win32' or sys.platform == 'darwin':
                    self.runAsDaemon = False

            # Write a pidfile if requested
            if o in ('--pidfile',):
                self.CREATEPID = True
                self.PIDFILE = str(a)

                # If the pidfile already exists, sickbeard may still be running, so exit
                if os.path.exists(self.PIDFILE):
                    sys.exit("PID file: " + self.PIDFILE + " already exists. Exiting.")

            # Specify folder to load the config file from
            if o in ('--config',):
                Gamez.CONFIG_FILE = os.path.abspath(a)

            # Specify folder to use as the data dir
            if o in ('--datadir',):
                Gamez.DATA_DIR = os.path.abspath(a)

            # Prevent resizing of the banner/posters even if PIL is installed
            if o in ('--noresize',):
                Gamez.NO_RESIZE = True

        # The pidfile is only useful in daemon mode, make sure we can write the file properly
        if self.CREATEPID:
            if self.runAsDaemon:
                pid_dir = os.path.dirname(self.PIDFILE)
                if not os.access(pid_dir, os.F_OK):
                    sys.exit("PID dir: " + pid_dir + " doesn't exist. Exiting.")
                if not os.access(pid_dir, os.W_OK):
                    sys.exit("PID dir: " + pid_dir + " must be writable (write permissions). Exiting.")

            else:
                if self.consoleLogging:
                    sys.stdout.write("Not running in daemon mode. PID file creation disabled.\n")

                self.CREATEPID = False

        # If they don't specify a config file then put it in the data dir
        if not Gamez.CONFIG_FILE: 
            Gamez.CONFIG_FILE = os.path.join(Gamez.DATA_DIR, "config.ini")
            
        # Make sure that we can create the data dir
        if not os.access(Gamez.DATA_DIR, os.F_OK):
            try:
                os.makedirs(Gamez.DATA_DIR, 0744)
            except os.error, e:
                raise SystemExit("Unable to create datadir '" + Gamez.DATA_DIR + "'")

        # Make sure we can write to the data dir
        if not os.access(Gamez.DATA_DIR, os.W_OK):
            raise SystemExit("Datadir must be writeable '" + Gamez.DATA_DIR + "'")

        # Make sure we can write to the config file
        if not os.access(Gamez.CONFIG_FILE, os.W_OK):
            if os.path.isfile(Gamez.CONFIG_FILE):
                raise SystemExit("Config file '" + Gamez.CONFIG_FILE + "' must be writeable.")
            elif not os.access(os.path.dirname(Gamez.CONFIG_FILE), os.W_OK):
                raise SystemExit(
                    "Config file root dir '" + os.path.dirname(Gamez.CONFIG_FILE) + "' must be writeable.")

        os.chdir(Gamez.DATA_DIR)

        # Check if we need to perform a restore first
        try:
            restoreDir = os.path.join(Gamez.DATA_DIR, 'restore')
            if self.consoleLogging and os.path.exists(restoreDir):
                if self.restoreDB(restoreDir, Gamez.DATA_DIR):
                    sys.stdout.write("Restore: restoring DB and config.ini successful...\n")
                else:
                    sys.stdout.write("Restore: restoring DB and config.ini FAILED!\n")
        except Exception as e:
            sys.stdout.write("Restore: restoring DB and config.ini FAILED!\n")

        # Load the config and publish it to the Gamez package
        if self.consoleLogging and not os.path.isfile(Gamez.CONFIG_FILE):
            sys.stdout.write("Unable to find '" + Gamez.CONFIG_FILE + "' , all settings will be default!" + "\n")

        Gamez.CFG = ConfigObj(Gamez.CONFIG_FILE)

        # Initialize the config and our threads
        Gamez.initialize(consoleLogging=self.consoleLogging)

        if self.runAsDaemon:
            self.daemonize()

        # Get PID
        Gamez.PID = os.getpid()

        # Fix clients old files
#        self.fix_clients_nonsense()

        # Build from the DB to start with
#        self.loadShowsFromDB()

        if self.forcedPort:
            logger.log(u"Forcing web server to port " + str(self.forcedPort))
            self.startPort = self.forcedPort
        else:
            self.startPort = Gamez.WEB_PORT

        if Gamez.WEB_LOG:
            self.log_dir = Gamez.LOG_DIR
        else:
            self.log_dir = None

        # Gamez.WEB_HOST is available as a configuration value in various
        # places but is not configurable. It is supported here for historic reasons.
        if Gamez.WEB_HOST and Gamez.WEB_HOST != '0.0.0.0':
            self.webhost = Gamez.WEB_HOST
        else:
            if Gamez.WEB_IPV6:
                self.webhost = '::'
            else:
                self.webhost = '0.0.0.0'

        # web server options
        self.web_options = {
            'port': int(self.startPort),
            'host': self.webhost,
            'data_root': os.path.join(Gamez.PROG_DIR, 'gui', Gamez.GUI_NAME),
            'web_root': Gamez.WEB_ROOT,
            'log_dir': self.log_dir,
            'username': Gamez.WEB_USERNAME,
            'password': Gamez.WEB_PASSWORD,
            'enable_https': Gamez.ENABLE_HTTPS,
            'handle_reverse_proxy': Gamez.HANDLE_REVERSE_PROXY,
            'https_cert': os.path.join(Gamez.PROG_DIR, Gamez.HTTPS_CERT),
            'https_key': os.path.join(Gamez.PROG_DIR, Gamez.HTTPS_KEY),
        }

        # start web server
        self.webserver = SRWebServer(self.web_options)
        self.webserver.start()

        if self.consoleLogging:
            print "Starting up Gamez " + Gamez.BRANCH + " from " + Gamez.CONFIG_FILE

        # Fire up all our threads
        Gamez.start()

        # Build internal name cache
        name_cache.buildNameCache()

        # Prepopulate network timezones, it isn't thread safe
        network_timezones.update_network_dict()

        # sure, why not?
        if Gamez.USE_FAILED_DOWNLOADS:
            failed_history.trimHistory()

        # Check for metadata indexer updates for shows (Disabled until we use api)
        #sickbeard.showUpdateScheduler.forceRun()

        # Launch browser
        if Gamez.LAUNCH_BROWSER and not (self.noLaunch or self.runAsDaemon):
            Gamez.launchBrowser('https' if Gamez.ENABLE_HTTPS else 'http', self.startPort, Gamez.WEB_ROOT)

        # main loop
        while (True):
            time.sleep(1)

    def daemonize(self):
        """
        Fork off as a daemon
        """
        # pylint: disable=E1101
        # Make a non-session-leader child process
        try:
            pid = os.fork()  # @UndefinedVariable - only available in UNIX
            if pid != 0:
                os._exit(0)
        except OSError, e:
            sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        os.setsid()  # @UndefinedVariable - only available in UNIX

        # Make sure I can read my own files and shut out others
        prev = os.umask(0)
        os.umask(prev and int('077', 8))

        # Make the child a session-leader by detaching from the terminal
        try:
            pid = os.fork()  # @UndefinedVariable - only available in UNIX
            if pid != 0:
                os._exit(0)
        except OSError, e:
            sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        # Write pid
        if self.CREATEPID:
            pid = str(os.getpid())
            logger.log(u"Writing PID: " + pid + " to " + str(self.PIDFILE))
            try:
                file(self.PIDFILE, 'w').write("%s\n" % pid)
            except IOError, e:
                logger.log_error_and_exit(
                    u"Unable to write PID file: " + self.PIDFILE + " Error: " + str(e.strerror) + " [" + str(
                        e.errno) + "]")

        # Redirect all output
        sys.stdout.flush()
        sys.stderr.flush()

        devnull = getattr(os, 'devnull', '/dev/null')
        stdin = file(devnull, 'r')
        stdout = file(devnull, 'a+')
        stderr = file(devnull, 'a+')
        os.dup2(stdin.fileno(), sys.stdin.fileno())
        os.dup2(stdout.fileno(), sys.stdout.fileno())
        os.dup2(stderr.fileno(), sys.stderr.fileno())

    def remove_pid_file(self, PIDFILE):
        try:
            if os.path.exists(PIDFILE):
                os.remove(PIDFILE)

        except (IOError, OSError):
            return False

        return True

#change to games  
    def loadShowsFromDB(self):
        """
        Populates the showList with shows from the database
        """

        logger.log(u"Loading initial show list", logger.DEBUG)

        myDB = db.DBConnection()
        sqlResults = myDB.select("SELECT * FROM tv_shows;")

        sickbeard.showList = []
        for sqlShow in sqlResults:
            try:
                curShow = TVShow(int(sqlShow["indexer"]), int(sqlShow["indexer_id"]))
                curShow.nextEpisode()
                sickbeard.showList.append(curShow)
            except Exception, e:
                logger.log(
                    u"There was an error creating the show in " + sqlShow["location"] + ": " + str(e).decode('utf-8'),
                    logger.ERROR)
                logger.log(traceback.format_exc(), logger.DEBUG)


    def restoreDB(self, srcDir, dstDir):
        try:
            filesList = ['Gamez.db', 'config.ini', 'failed.db', 'cache.db']

            for filename in filesList:
                srcFile = os.path.join(srcDir, filename)
                dstFile = os.path.join(dstDir, filename)
                bakFile = os.path.join(dstDir, '{0}.bak-{1}'.format(filename, datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d_%H%M%S')))
                if os.path.isfile(dstFile):
                    shutil.move(dstFile, bakFile)
                shutil.move(srcFile, dstFile)
            return True
        except:
            return False

    def shutdown(self, type):
        if Gamez.started:
            # stop all tasks
            Gamez.halt()

            # save all shows to DB
            Gamez.saveAll()

            # shutdown web server
            if self.webserver:
                logger.log("Shutting down Tornado")
                self.webserver.shutDown()
                try:
                    self.webserver.join(10)
                except:
                    pass

            # if run as daemon delete the pidfile
            if self.runAsDaemon and self.CREATEPID:
                self.remove_pid_file(self.PIDFILE)

            if type == Gamez.events.SystemEvent.RESTART:
                install_type = Gamez.versionCheckScheduler.action.install_type

                popen_list = []

                if install_type in ('git', 'source'):
                    popen_list = [sys.executable, Gamez.MY_FULLNAME]
                elif install_type == 'win':
                    if hasattr(sys, 'frozen'):
                        # c:\dir\to\updater.exe 12345 c:\dir\to\Gamez.exe
                        popen_list = [os.path.join(Gamez.PROG_DIR, 'updater.exe'), str(Gamez.PID),
                                      sys.executable]
                    else:
                        logger.log(u"Unknown SR launch method, please file a bug report about this", logger.ERROR)
                        popen_list = [sys.executable, os.path.join(Gamez.PROG_DIR, 'updater.py'),
                                      str(Gamez.PID),
                                      sys.executable,
                                      Gamez.MY_FULLNAME]

                if popen_list and not Gamez.NO_RESTART:
                    popen_list += Gamez.MY_ARGS
                    if '--nolaunch' not in popen_list:
                        popen_list += ['--nolaunch']
                    logger.log(u"Restarting Gamez with " + str(popen_list))
                    logger.shutdown() #shutdown the logger to make sure it's released the logfile BEFORE it restarts SR.
                    subprocess.Popen(popen_list, cwd=os.getcwd())

        # system exit
        logger.shutdown() #Make sure the logger has stopped, just in case
        os._exit(0)


if __name__ == "__main__":
    if sys.hexversion >= 0x020600F0:
        freeze_support()

    # start Gamez
    Gamez().start()
            
