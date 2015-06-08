#!/usr/bin/env python
# -*- coding: utf-8

# Copyright (C) 2013 Stefan Hacker <dd0t@users.sourceforge.net>
# Copyright (C) 2015 Cory Stunson  <cws4689@hotmail.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:

# - Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
# - Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# - Neither the name of the Mumble Developers nor the names of its
#   contributors may be used to endorse or promote products derived from this
#   software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# `AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE FOUNDATION OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

# --------------- Imports ---------------

from mumo_module import (commaSeperatedIntegers, commaSeperatedStrings,
                         MumoModule)
import re


# --------------- Module configuration ---------------

class sleepbot(MumoModule):
    default_config = {'sleepbot': (
                                  ('servers', commaSeperatedIntegers, []),
                                  ('limit', int, 0),
                                  ('exceptions', commaSeperatedStrings, []),
                                  )
                     }
    
    
    # --------------- Module Initialization ---------------
    
    def __init__(self, name, manager, configuration=None):
        MumoModule.__init__(self, name, manager, configuration)
        self.murmur = manager.getMurmurModule()
    
    def connected(self):
        manager = self.manager()
        log = self.log()
        log.debug("Register for Server callbacks")
        
        servers = self.cfg().sleepbot.servers
        if not servers:
            servers = manager.SERVERS_ALL
        
        manager.subscribeServerCallbacks(self, servers)
        
        
        # --------------- Get all users current position and store to memory ---------------
        try:
            userCount = 0
            for serv in connServers:
                userlist = serv.getUsers()
                for user in userlist:
                    entry = "%i-%s" % (serv.id(), userlist[user].name)
                    setattr(sleepbot, entry, userlist[user].channel)
                    userCount = userCount + 1
            log.debug("Successfully took snap shot of user positions into memory for %i users" % userCount)
                #except:
#log.debug("Could not load user data into memory. Will track moving forward.")
            
    def disconnected(self): pass


# --------------- Call back functions ---------------

def userStateChanged(self, server, state, context=None):
    log = self.log()
        sid = server.id()
        
        monitored = 0
        
        # --------------- Global config ---------------
        try:
            if self.cfg().sleepbot.limit > 0:
                climit = self.cfg().sleepbot
                curchan = state.channel
                monitored = 1
            if monitored == 1:
                log.debug("User %s entered channel and is not empty", state.name, curchan, climit.limit)
        except:
                log.debug("Unable to determine config")
            
            # --------------- Get information on all connected users ---------------
            userlist = server.getUsers()
            exceptions = 0
            chanCount = userlist + exceptions
            for user in userlist:
                if userlist[user].channel == curchan:
                    chanCount = chanCount + 1
            
            
                # --------------- Check if occupied/unoccupied ---------------
                if chanCount > climit.limit:
                    
                    # Channel is now occupied
                    try:
                        server.sendMessage(state.channel, '.wakeup')
                        server.sendMessage(state.channel, '-wakeup')
                    except:
                        log.debug("Unable to Wakeup bots")

        if chanCount < climit.limit
            
            # Channel is unoccupied
            try:
                server.sendMessage(state.channel, '.gotobed')
                server.sendMessage(state.channel, '-gotobed')
                    except:
                        log.debug("Unable to Sleep bots")

# Putting users new current channel into memory for later reference

entry = "%i-%s" % (server.id(), state.name)
    setattr(sleepbot, entry, state.channel)
        testing = getattr(sleepbot, "%s" % entry)

def userConnected(self, server, state, context=None): pass

def userDisconnected(self, server, state, context=None): pass
    
def userTextMessage(self, server, user, message, current=None): pass
    
def channelCreated(self, server, state, context=None): pass
    
def channelRemoved(self, server, state, context=None): pass
    
def channelStateChanged(self, server, state, context=None): pass
