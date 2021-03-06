# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from typing import List  # noqa: F401

from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from Xlib import display as xdisplay
import os
import subprocess


@hook.subscribe.startup_once
def autostart():
  home = os.path.expanduser('~/.config/qtile/autostart.sh') # path to my script, under my user directory
  subprocess.call([home])

  
mod = "mod4"
terminal = guess_terminal()

keys = [
    # Switch between windows in current stack pane
    Key([mod], "j", lazy.layout.down(),
        desc="Move focus down in stack pane"),
    Key([mod], "k", lazy.layout.up(),
        desc="Move focus up in stack pane"),
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),
    Key([mod, "control"], "j", lazy.layout.grow_down()),
    Key([mod, "control"], "k", lazy.layout.grow_up()),
    Key([mod, "control"], "h", lazy.layout.grow_left()),
    Key([mod, "control"], "l", lazy.layout.grow_right()),


    # Swap panes of split stack
    Key([mod], "Tab", lazy.layout.next(),
        desc="Swap panes of split stack"),

    # Switch window focus to other pane(s) of stack
    Key([mod, "shift"], "space", lazy.layout.rotate(),
        desc="Switch window focus to other pane(s) of stack"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),

    # Toggle between different layouts as defined below
    Key([mod], "space", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),

    Key([mod, "control"], "r", lazy.restart(), desc="Restart qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown qtile"),
    #Key([mod], "r", lazy.spawn("dmenu_run"),
    Key([mod], "r", lazy.spawn("rofi -show run"),
        desc="Spawn a command using a prompt widget"),
    Key([], "XF86MonBrightnessUp", lazy.spawn("xbacklight -inc 5")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("xbacklight -dec 5")),
    Key([mod], "w", lazy.spawn("qutebrowser")),
    Key([mod], "f", lazy.spawn("alacritty -e ranger")),
    Key([mod],"a", lazy.spawn("rofi -show window")),
]

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen(),
            desc="Switch to group {}".format(i.name)),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(i.name)),
        # Or, use below if you prefer not to switch to that group.
        # # mod1 + shift + letter of group = move focused window to group
        # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
        #     desc="move focused window to group {}".format(i.name)),
    ])

layouts = [
    layout.Max(),
    #layout.Columns(
    #    margin = 8,
    #    border_focus = "#668bd7",
    #    border_focus_stack = "#668bd7"
    #    ),
    #layout.Stack(num_stacks=2,margin=8),
    #Try more layouts by unleashing below layouts.
    #layout.Bsp(margin=8),
    #layout.Matrix(),
    layout.MonadTall(
        margin=8,
        border_focus = "#668bd7",
        border_focus_stack = "#668bd7"
        ),
   #layout.MonadWide(),
    #layout.RatioTile(),
    #layout.Tile(),
    #layout.TreeTab(
    #    font = "Hack Nerd Font Mono",
    #    fontsize = 16,
    #    sections = ["WINDOWS"],
    #    section_fontsize = 16,
    #    bg_color = "292d3e",
    #    active_bg = "90C435",
    #    active_fg = "000000",
    #    inactive_bg = "384323",
    #    inactive_fg = "a0a0a0",
    #    padding_y = 5,
    #    section_top = 10,
    #    panel_width = 320
    #),
    #layout.VerticalTile(),
    #layout.Zoomy(),
]

colors = [["#292d3e", "#292d3e"], # panel background
          ["#434758", "#434758"], # background for current screen tab
          ["#ffffff", "#ffffff"], # font color for group names
          ["#ff5555", "#ff5555"], # border line color for current tab
          ["#8d62a9", "#8d62a9"], # border line color for other tab and odd widgets
          ["#668bd7", "#668bd7"], # color for the even widgets
          ["#e1acff", "#e1acff"]] # window name
          
widget_defaults = dict(
    font='Hack Nerd Font Mono',
    fontsize=16,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                #widget.CurrentLayout(
                #    padding = 10,
                #    ),
                widget.GroupBox(
                    padding = 5,
                    margin_y = 3,
                    margin_x = 0,
                    padding_y = 5,
                    padding_x = 3,
                    borderwidth = 3,
                    active = colors[2],
                    inactive = colors[5],
                    rounded = False,
                    highlight_color = colors[1],
                    highlight_method = "line",
                    this_current_screen_border = colors[3],
                    this_screen_border = colors [4],
                    other_current_screen_border = colors[0],
                    other_screen_border = colors[0],
                    foreground = colors[2],
                    background = colors[0]
                    ),
                widget.Sep(
                    linewidth = 0,
                    padding = 2,
                    foreground = colors[2],
                    background = colors[5]
                    ),
                widget.Prompt(
                    padding = 10,
                    foreground = colors[2],
                    background = colors[5]
                    ),
                widget.Sep(
                    linewidth = 0,
                    padding = 2,
                    foreground = colors[2],
                    background = colors[0]
                    ),    
                widget.WindowName(
                    foreground = colors[6],
                    background = colors[0],
                    padding = 0
                    ),
                #widget.Chord(
                #    chords_colors={
                #        'launch': ("#ff0000", "#ffffff"),
                #    },
                #    name_transform=lambda name: name.upper(),
                #),
                #widget.TaskList(),
                widget.Sep(
                    linewidth = 0,
                    padding = 2,
                    foreground = colors[2],
                    background = colors[5]
                    ),
                widget.Net(
                    format = '{down} ↓↑ {up}',
                    foreground = colors[2],
                    background = colors[0],
                    padding = 5
                    ),
                widget.Sep(
                    linewidth = 0,
                    padding = 2,
                    foreground = colors[2],
                    background = colors[5]
                    ),
                widget.TextBox(
                    text = " 🌡",
                    padding = 2,
                    foreground = colors[2],
                    background = colors[0],
                    fontsize = 11
                    ),    
                widget.ThermalSensor(
                    foreground = colors[2],
                    background = colors[0],
                    threshold = 90,
                    padding = 5
                    ),
                widget.Sep(
                    linewidth = 0,
                    padding = 2,
                    foreground = colors[2],
                    background = colors[5]
                    ),
                widget.TextBox(
                    text = " 🖬",
                    foreground = colors[2],
                    background = colors[0],
                    padding = 0,
                    fontsize = 14
                    ),
                widget.Memory(
                    foreground = colors[2],
                    background = colors[0],
                    mouse_callbacks = {'Button1': lambda qtile: qtile.cmd_spawn(alacritty + ' -e htop')},
                    padding = 5
                    ),
                widget.Sep(
                    linewidth = 0,
                    padding = 2,
                    foreground = colors[2],
                    background = colors[5]
                    ),
                widget.Battery(
                    background = colors[0],
                    padding = 5
                    ),
                widget.Sep(
                    linewidth = 0,
                    padding = 2,
                    foreground = colors[2],
                    background = colors[5]
                    ),
                widget.Systray(
                    background = colors[0],
                    padding = 5
                    ),
                widget.Sep(
                    linewidth = 0,
                    padding = 2,
                    foreground = colors[2],
                    background = colors[5]
                    ),
                widget.Clock(
                    format='%Y-%m-%d %a %H:%M',
                    foreground = colors[2],
                    background = colors[0],
                    ),
                widget.Sep(
                    linewidth = 0,
                    padding = 2,
                    foreground = colors[2],
                    background = colors[5]
                    ),
                #widget.QuickExit(),
            ],
            24,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None  # WARNING: this is deprecated and will be removed soon
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
])
auto_fullscreen = True
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
