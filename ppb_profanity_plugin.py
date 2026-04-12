"""
PBEasy /ppb plugin for profanity (only in TMUX session)

Open Link with the PBEasy ppb (PrivatePasteBin) to comment or reply to a paste.
If no link is provided, will open ppb with no URL. Tab autocompletion will go
through all previous links in the current chat/room.

This plugin only works, if you're using profanity in a tmux session, but it
is a very convenient way to manage your pastes.
"""

import prof
import re
import os


_links = {}
_lastlink = {}


def _cmd_ppb(url):
    global _lastlink
    link = None

    # use arg if supplied
    if (url is not None):
        link = url
    else:
        jid = prof.get_current_recipient()
        room = prof.get_current_muc()

        # check if in chat window
        if (jid is not None):

            # check for link from recipient
            if jid in _lastlink.keys():
                link = _lastlink[jid]
            else:
                prof.cons_show("No links found from " + jid)

        # check if in muc window
        elif (room is not None):
            if room in _lastlink.keys():
                link = _lastlink[room]
            else:
                prof.cons_show("No links found from " + room)

    # open the browser if link found
    if (link is not None):
        prof.cons_show("Opening " + link + " in PBEasy ppb")
        _open_ppb(link)
    else:
        prof.cons_show("Opening ppb PrivateBin Browser")
        _open_ppb("")


def _open_ppb(url):
    cmd = 'tmux new-window -n ppb -e SSH_CONNECTION'
    cmd += ' "bash --login -c \'ppb'
    if url:
        cmd += f' -c \\"{url}\\"'
    cmd += '\'"'
    os.system(cmd)


def prof_init(version, status, account_name, fulljid):
    synopsis = [
        "/ppb",
        "/ppb [url]"
    ]
    description = "Will open PBEasy PrivateBin Helper. " \
        "Tab autocompletion will go through all previous links in the current chat/room"
    args = [
        ["[url]", "URL to open with ppb"]
    ]
    examples = [
        "/ppb http://pb.envs.net/?<paste>#<key>"
    ]

    prof.register_command("/ppb", 0, 1, synopsis, description,
                          args, examples, _cmd_ppb)


def prof_on_chat_win_focus(barejid):
    prof.completer_clear("/ppb")
    if barejid in _links:
        prof.completer_add("/ppb", _links[barejid])


def prof_on_room_win_focus(barejid):
    prof.completer_clear("/ppb")
    if barejid in _links:
        prof.completer_add("/ppb", _links[barejid])


def _process_message(barejid, current_jid, message):
    links = re.findall(r'(https?://\S+)', message)
    if (len(links) > 0):
        if barejid not in _links:
            _links[barejid] = []
        # add to list of links for barejid
        for link in links:
            if link not in _links[barejid]:
                _links[barejid].append(link)
        # add to autocompleter if message for current window
        if current_jid == barejid:
            prof.completer_add("/ppb", _links[barejid])
        # set last link for barejid
        _lastlink[barejid] = links[len(links)-1]


def prof_post_chat_message_display(barejid, resource, message):
    current_jid = prof.get_current_recipient()
    _process_message(barejid, current_jid, message)


def prof_post_room_message_display(barejid, nick, message):
    current_jid = prof.get_current_muc()
    _process_message(barejid, current_jid, message)


def prof_on_room_history_message(barejid, nick, message, timestamp):
    current_jid = prof.get_current_muc()
    _process_message(barejid, current_jid, message)
