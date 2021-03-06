"""
 Copyright (c) 2013 Popeye

 Permission is hereby granted, free of charge, to any person
 obtaining a copy of this software and associated documentation
 files (the "Software"), to deal in the Software without
 restriction, including without limitation the rights to use,
 copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the
 Software is furnished to do so, subject to the following
 conditions:

 The above copyright notice and this permission notice shall be
 included in all copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
 OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
 HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
 WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
 OTHER DEALINGS IN THE SOFTWARE.
"""
import xbmc
import xbmcaddon

import re

__settings__ = xbmcaddon.Addon(id='script.service.sabnzbd')
__icon__ = __settings__.getAddonInfo("icon")

IS_PAUSED = __settings__.getSetting('sab_paused').lower() == 'true'
SPEED = __settings__.getSetting('sab_speed').lower()
ONLINE_ONLY = __settings__.getSetting('online_only').lower() == 'true'
SHOW_NOTIFICATION = __settings__.getSetting('show_notification').lower() == 'true'

class XBMCPlayer(xbmc.Player):
    def __init__( self, *args, **kwargs ):
        self.script_controlled = False

    def onPlayBackStarted( self ):
        if not (ONLINE_ONLY and is_local_file()):
            pause()
            self.script_controlled = True

    def onPlayBackEnded( self ):
        if self.script_controlled:
            resume()
            self.script_controlled = False

    def onPlayBackStopped( self ):
        if self.script_controlled:
            resume()
            self.script_controlled = False

    def sleep(self, s):
        xbmc.sleep(s)

player = XBMCPlayer(xbmc.PLAYER_CORE_AUTO)

def pause():
    if IS_PAUSED:
        if SHOW_NOTIFICATION:
            xbmc.executebuiltin('Notification("PauseSABnzbdService", "Paused", 500, %s)' % __icon__)
        xbmc.executebuiltin('XBMC.RunPlugin(plugin://plugin.program.sabnzbd/?mode=sab_action&sab_mode=pause)')
    else:
        if SHOW_NOTIFICATION:
            xbmc.executebuiltin('Notification("PauseSABnzbdService", "Speed %s KB/s", 500, %s)' % (SPEED, __icon__))
        xbmc.executebuiltin('XBMC.RunPlugin(plugin://plugin.program.sabnzbd/?mode=sab_action&sab_mode=config&sab_name=speedlimit&sab_value=%s)' 
                             % SPEED)

def resume():
    if IS_PAUSED:
        if SHOW_NOTIFICATION:
            xbmc.executebuiltin('Notification("PauseSABnzbdService", "Resumed", 500, %s)' % __icon__)
        xbmc.executebuiltin('XBMC.RunPlugin(plugin://plugin.program.sabnzbd/?mode=sab_action&sab_mode=resume)')
    else:
        if SHOW_NOTIFICATION:
            xbmc.executebuiltin('Notification("PauseSABnzbdService", "Speed reset", 500, %s)' % __icon__)
        xbmc.executebuiltin('XBMC.RunPlugin(plugin://plugin.program.sabnzbd/?mode=sab_action&sab_mode=config&sab_name=speedlimit&sab_value=)')

def is_local_file():
    RE_ONLINE = '^http|^rt|^ftp|^mms'
    if re.search(RE_ONLINE, player.getPlayingFile(), re.IGNORECASE):
        return False
    else:
        return True

while (not xbmc.abortRequested):
    player.sleep(500)
