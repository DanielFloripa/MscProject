#!/bin/bash

# Copyright (C) 2013 Ole Tange and Free Software Foundation, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This script downloads the latest version of GNU Parallel, checks
# the signature and installs it.
#
# It first tries to install it globally.
# If that fails, it does a personal installation.
# If that fails, it copies to $HOME/bin

# Download and run the script directly by:
#   (wget -O - pi.dk/3 || curl pi.dk/3/ || fetch -o - http://pi.dk/3) | bash

# tail on openindiana must be /usr/xpg4/bin/tail
TAIL=$(echo | tail -n 1 2>/dev/null && echo tail || (echo | /usr/xpg4/bin/tail -n 1 && echo /usr/xpg4/bin/tail))
# grep on openindiana must be /usr/xpg4/bin/grep
GREP=$(echo | grep -vE . 2>/dev/null && echo grep || (echo | /usr/xpg4/bin/grep -vE . && echo /usr/xpg4/bin/grep))
# FreeBSD prefers 'fetch', MacOS prefers 'curl', Linux prefers 'wget'
GET=$(
    (fetch -o /dev/null file:///bin/sh && echo fetch -o -) ||
    (curl -h >/dev/null && echo curl -L) || 
    (wget -h >/dev/null && echo wget -qO -) ||
    echo 'No wget, curl, fetch: Please inform parallel@gnu.org what you use for downloading URLs' >&2
)
if test "$GET" = ""; then
  exit 1
fi

if ! perl -e 1; then
  echo No perl installed. GNU Parallel depends on perl. Install perl and retry
  exit 1
fi

LANG=C
LATEST=$($GET http://ftpmirror.gnu.org/parallel | perl -ne '/.*(parallel-\d{8})/ and print $1."\n"' | sort | $TAIL -n1)
if test \! -e $LATEST.tar.bz2; then
  # Source tar does not exist
  rm -f $LATEST.tar.bz2 $LATEST.tar.bz2.sig
  $GET http://ftpmirror.gnu.org/parallel/$LATEST.tar.bz2 > $LATEST.tar.bz2
  $GET http://ftpmirror.gnu.org/parallel/$LATEST.tar.bz2.sig > $LATEST.tar.bz2.sig
fi

bzip2 -dc $LATEST.tar.bz2 | tar xf -
cd $LATEST || exit 2
if ./configure && make && make install; then
  echo
  echo GNU $LATEST installed globally
else
  if ./configure --prefix=$HOME && make && make install; then
    echo
    echo GNU $LATEST installed in $HOME/bin
  else
    mkdir -p $HOME/bin/;
    chmod 755 src/*;
    cp src/parallel src/sem src/sql src/niceload $HOME/bin;
    echo
    echo GNU $LATEST copied to $HOME/bin
  fi

  # Is $HOME/bin already in $PATH?
  if echo $PATH | grep $HOME/bin >/dev/null; then
    # $HOME/bin is already in $PATH
    true
  else
    # Add $HOME/bin to $PATH for both bash and csh
    echo 'PATH=$PATH:$HOME/bin' >> $HOME/.bashrc
    echo 'setenv PATH ${PATH}:${HOME}/bin' >> $HOME/.cshrc
  fi

  # Is $HOME/share/man already in $MANPATH?
  if echo $MANPATH | grep $HOME/share/man >/dev/null; then
    # $HOME/share/man is already in $MANPATH
    true
  else
    # Add $HOME/share/man to $MANPATH for both bash and csh
    echo 'MANPATH=$MANPATH:$HOME/share/man' >> $HOME/.bashrc
    echo 'setenv MANPATH ${MANPATH}:${HOME}/share/man' >> $HOME/.cshrc
  fi
fi