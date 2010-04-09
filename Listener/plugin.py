###
# Copyright (c) 2010, quantumlemur
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

import socket
import threading
import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircmsgs as ircmsgs
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks


class Listener(callbacks.Plugin):
    """Add the help for "@plugin help Listener" here
    This should describe *how* to use this plugin."""
    threaded = True

    def __init__(self, irc):
        self.__parent = super(Listener, self)
        self.__parent.__init__(irc)
#    def start(self, irc, msg, args):
        self.irc = irc
        self.buffer = ''
        self.channel = '#testytest'  # set this
        self.host = 'localhost'  # ...and this
        self.port = 56789  # ...and this.
        self.listenerThread = self.ListeningThread(self.irc, self.channel, self.host, self.port)
        self.listenerThread.start()
#    start = wrap(start)


    class ListeningThread(threading.Thread):
        def __init__(self, irc, channel, host, port):
            threading.Thread.__init__(self)
            self.irc = irc
            self.channel = channel
            self.host = host
            self.port = port
            self.buffer = ''
            self.active = True
            self.listener = socket.socket()
            self.listener.settimeout(2)
            self.listener.bind((self.host, self.port))
            self.listener.listen(4)

        def run(self):
            while self.active:
                try:
                    conn, addr = self.listener.accept()
                    self.buffer = conn.recv(4092)
                    conn.close()
                except IOError:
                    pass
                if self.buffer:
                    self.irc.queueMsg(ircmsgs.privmsg(self.channel, self.buffer))
                    self.buffer = ''
            self.listener.close()

        def stop(self):
            self.active = False


    def stop(self, irc, msg, args):
        """takes no arguments

        Tries to close the listening socket"""
        self.listenerThread.stop()
    stop = wrap(stop)

Class = Listener


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
