#!/usr/bin/env python
# -*- coding: utf-8

# Copyright (C) 2013 Stefan Hacker <dd0t@users.sourceforge.net>
# Copyright (C) 2012-2014 Natenom <natenom@googlemail.com>
# Copyright (C) 2015 Stunner1984 <cws4689@hotmail.com>
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
                                  ('botlist', commaSeperatedStrings, []),
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

        try:
            # Get server connections
            meta = manager.getMeta();
            connServers = meta.getBootedServers();

            # Get all users and store in memory
            userCount = 0
            for serv in connServers:
                userlist = serv.getUsers()
                for user in userlist:
                    entry = "%i-%s" % (serv.id(), userlist[user].name)
                    log.debug("User chan: %s - Server: %i - %s", userlist[user].channel, serv.id(), entry)
                    setattr(sleepbot, entry, userlist[user].channel)
                    userCount = userCount + 1
            log.debug("Successfully took snap shot of user positions into memory for %i users" % userCount)
        except:
            log.debug("Could not load user data into memory. Will track moving forward.")

    def disconnected(self): pass

    # --------------- Call back functions ---------------

    def userStateChanged(self, server, state, context=None):
        log = self.log()
        sid = server.id()
        active = 0

        if (self.cfg().sleepbot.limit >= 0):
            climit = self.cfg().sleepbot
            curchan = state.channel
            active = 1
        if active == 1:
            log.debug("User %s entered monitored channel %i which has a limit set to %i", state.name, curchan, climit.limit)

            userlist = server.getUsers()
            botlist = self.cfg().sleepbot.botlist
            chanCount = 0
            for user in userlist:
                if(userlist[user].channel == curchan):
                    chanCount = chanCount + 1
                    log.debug("user %s and chanCount %i", user, chanCount)
                    for user in userlist:
                        if(user.name == botlist):
                            for botlist in user.name:
                                if(user.channel == curchan):
                                    chanCount = chanCount - 1
                                    log.debug("botlist %s and chanCount %i after musicbots", user, chanCount)
            
            if (chanCount > climit.limit):
                # Check if channel has ACL present
                exceptions = self.cfg().sleepbot.exceptions
                botfound = 0
                if exceptions:
                    getID = [state.name]
                    userID = server.getUserIds(getID)
                    groupList = server.getACL(state.channel)
                    for group in groupList[1]:
                        for exception in exceptions:
                            if (group.name == exception):
                                for members in group.members:
                                    if (members == userID[state.name]):
                                        botfound = 1
                                        log.debug("chanCount %i set after exceptions, botfound %i", chanCount, botfound)
                                        return(1)
            
                if botfound == 0:
                    # Channel is now occupied
                    try:
                        server.sendMessage(self.session, '.gotobed')
                        server.sendMessage(self.session, '-gotobed')
                        log.debug("chanCount %i, climit %i, limit %i", chanCount, climit, limit)
                    except:
                        log.debug("Unable to put bots to sleep")

                if botfound == 1:
                    # Channel is unoccupied
                    try:
                        server.sendMessage(self.session, '.wakeup')
                        server.sendMessage(self.session, '-wakeup')
                        log.debug("chanCount %i, climit %i, limit %i", chanCount, climit, limit)
                    except:
                        log.debug("Unable to wakeup bots")

        # Putting users new current channel into memory for later reference

        entry = "%i-%s" % (server.id(), state.name)
        setattr(sleepbot, entry, state.channel)
        testing = getattr(sleepbot, "%s" % entry)
        log.debug("Current channel stored as %s for %s as entry %s", testing, state.name, entry)

    def userConnected(self, server, state, context=None): pass
    def userDisconnected(self, server, state, context=None): pass
    def userTextMessage(self, server, user, message, current=None): pass
    def channelCreated(self, server, state, context=None): pass
    def channelRemoved(self, server, state, context=None): pass
    def channelStateChanged(self, server, state, context=None): pass