#!/usr/bin/env python3
"""
TerminalTunes Music Player – neat-layout & stable thread version
"""
import os
import time
import threading
import urwid
import pygame

# ── optional: accurate lengths with mutagen ───────────────────
try:
    from mutagen.mp3 import MP3
    from mutagen.wave import WAVE
    from mutagen.oggvorbis import OggVorbis
    from mutagen.flac import FLAC
    HAS_MUTAGEN = True
except ImportError:
    HAS_MUTAGEN = False
# ──────────────────────────────────────────────────────────────


# ╭──────────────────────────────────────────────────────────╮
# │                     MUSIC-PLAYER                        │
# ╰──────────────────────────────────────────────────────────╯
class MusicPlayer:
    def __init__(self):
        pygame.mixer.init(frequency=44_100, size=-16, channels=2, buffer=4_096)

        self.playlist: list[str] = []
        self.current_index = 0
        self.is_playing = False
        self.volume = 0.7
        pygame.mixer.music.set_volume(self.volume)

        self.track_lengths: dict[str, float] = {}
        self.current_track_start_time = 0
        self.current_track_paused_position = 0

        self._build_ui()          # sets widgets / palette

    # ──────────────────────────────────────────────────────────
    # UI BUILD
    # ──────────────────────────────────────────────────────────
    def _nice_button(self, label: str, cb):
        """Return a button wrapped with colour focus highlight."""
        return urwid.AttrMap(urwid.Button(label, cb),
                             'button', focus_map='button_focus')

    def _build_ui(self):
        # header
        self.header_text = urwid.Text(
            "TerminalTunes Music Player", align='center')
        header = urwid.AttrMap(self.header_text, 'header')

        # browser (left)
        self.dir_browser = DirectoryBrowser(self.file_selected)
        browser_box = urwid.LineBox(self.dir_browser, title="Music Files")

        # now-playing (left-bottom)
        self.now_playing = urwid.Text("Not playing")
        now_playing_box = urwid.LineBox(urwid.Filler(
            self.now_playing), title="Now Playing")

        # playlist (right-top)
        self.playlist_walker = urwid.SimpleFocusListWalker([])
        self.playlist_listbox = urwid.ListBox(self.playlist_walker)
        playlist_box = urwid.LineBox(self.playlist_listbox, title="Playlist")

        # progress bar
        self.progress = urwid.ProgressBar(
            'progress_normal', 'progress_complete', 0, 1)
        self.progress_text = urwid.Text("0:00 / 0:00")
        progress_box = urwid.LineBox(
            urwid.Columns([('weight', 8, self.progress),
                          ('weight', 2, self.progress_text)]),
            title="Progress")

        # main controls
        self.play_button = self._nice_button("Play",  self.toggle_play)
        self.stop_button = self._nice_button("Stop",  self.stop)
        self.prev_button = self._nice_button("Prev",  self.previous)
        self.next_button = self._nice_button("Next",  self.next)

        vol_down = self._nice_button("─", self.volume_down)
        vol_up = self._nice_button("+", self.volume_up)
        self.vol_text = urwid.Text(f"Volume {int(self.volume*100)}%")
        volume_cols = urwid.Columns([('pack', vol_down), self.vol_text, ('pack', vol_up)],
                                    dividechars=1)

        controls_row = urwid.Columns(
            [('pack', self.play_button), ('pack', self.stop_button),
             ('pack', self.prev_button), ('pack', self.next_button),
             volume_cols],
            dividechars=4)
        controls_box = urwid.LineBox(controls_row, title="Controls")

        # playlist-action buttons
        clr_btn = self._nice_button("Clear",  self.clear_playlist)
        del_btn = self._nice_button("Delete", self.remove_selected_track)
        play_sel = self._nice_button("Play",   self.play_selected_track)

        playlist_actions = urwid.Columns(
            [('pack', clr_btn), ('pack', del_btn), ('pack', play_sel)],
            dividechars=4)
        playlist_actions_box = urwid.LineBox(
            playlist_actions, title="Playlist Actions")

        # footer help line
        footer = urwid.AttrMap(
            urwid.Text(
                "q Quit | Tab switch | Space play/pause | n/p next/prev | +/- volume | d delete"),
            'footer')

        # layout
        left_panel = urwid.Pile(
            [('weight', 7, browser_box), ('weight', 3, now_playing_box)])
        right_panel = urwid.Pile([('weight', 5, playlist_box),
                                  playlist_actions_box,
                                  ('weight', 4,
                                   urwid.Pile([progress_box, controls_box]))])

        self.frame = urwid.Frame(
            body=urwid.Columns([left_panel, right_panel], dividechars=1),
            header=header, footer=footer)

        # palette
        self.palette = [
            ('header',           'white',      'dark blue'),
            ('footer',           'light gray', 'dark blue'),
            ('dir',              'light green', ''),
            ('file',             'light cyan',  ''),
            ('playing',          'black',      'light green'),
            ('selected',         'white',      'dark green'),
            ('progress_normal',  'black',      'dark gray'),
            ('progress_complete', 'white',      'dark green'),
            ('button',           'white',      ''),
            ('button_focus',     'black',      'light gray'),
        ]

    # ──────────────────────────────────────────────────────────
    # main loop
    # ──────────────────────────────────────────────────────────
    def run(self):
        self.loop = urwid.MainLoop(self.frame, self.palette,
                                   unhandled_input=self.handle_input,
                                   screen=urwid.raw_display.Screen())
        self.loop.screen.set_terminal_properties(colors=256)

        # start periodic screen refresh
        self.loop.set_alarm_in(0.1, self._refresh_screen)

        # start progress-bar background thread *after* self.loop exists
        self.update_thread = threading.Thread(
            target=self._progress_loop, daemon=True)
        self.update_thread.start()

        self.loop.run()

    def _refresh_screen(self, loop, _):
        loop.draw_screen()
        loop.set_alarm_in(0.1, self._refresh_screen)

    # ──────────────────────────────────────────────────────────
    # input handlers
    # ──────────────────────────────────────────────────────────
    def handle_input(self, key):
        if key in ('q', 'Q'):
            self.quit()
        elif key == ' ':
            self.toggle_play()
        elif key in ('n', 'N'):
            self.next()
        elif key in ('p', 'P'):
            self.previous()
        elif key in ('+', '='):
            self.volume_up()
        elif key == '-':
            self.volume_down()
        elif key in ('d', 'D', 'delete'):
            self.remove_selected_track()
        elif key == 'tab':
            self._cycle_focus()
        elif key == 'enter':
            self._enter_action()

    def _cycle_focus(self):
        cols = self.frame.body
        if cols.focus_position == 0:          # from browser → playlist
            cols.focus_position = 1
            cols.contents[1][0].focus_position = 0
        else:                                 # cycle inside right panel
            rp = cols.contents[1][0]
            rp.focus_position = (rp.focus_position + 1) % 3
            if rp.focus_position == 0:
                pass
            elif rp.focus_position == 1:
                pass
            else:
                cols.focus_position = 0
        self.header_text.set_text(f"Focused: {self._focus_name()}")
        self.loop.set_alarm_in(
            1.5, lambda *_: self.header_text.set_text("TerminalTunes Music Player"))

    def _focus_name(self):
        if self.frame.body.focus_position == 0:
            return "File Browser"
        idx = self.frame.body.contents[1][0].focus_position
        return ["Playlist", "Playlist Actions", "Controls"][idx]

    def _enter_action(self):
        if self.frame.body.focus_position == 0:
            self.dir_browser.open_selected()
        else:
            if self.frame.body.contents[1][0].focus_position == 0:
                self.play_selected_track()

    # ──────────────────────────────────────────────────────────
    # playback controls
    # ──────────────────────────────────────────────────────────
    def toggle_play(self, *_):
        if not self.playlist:
            return
        if self.is_playing:
            pygame.mixer.music.pause()
            self.current_track_paused_position = time.time() - self.current_track_start_time
            self.play_button.base_widget.set_label("Play")
        else:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.unpause()
                self.current_track_start_time = time.time() - self.current_track_paused_position
            else:
                self._play_current()
            self.play_button.base_widget.set_label("Pause")
        self.is_playing = not self.is_playing

    def _play_current(self):
        if not self.playlist:
            return
        path = self.playlist[self.current_index]
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()
            self.current_track_start_time = time.time()
            self.current_track_paused_position = 0
            self.now_playing.set_text(os.path.basename(path))
            m, s = divmod(int(self._length(path)), 60)
            self.progress_text.set_text(f"0:00 / {m}:{s:02d}")
            self._highlight_playlist()
        except pygame.error as e:
            self.now_playing.set_text(f"Error: {e}")

    def stop(self, *_):
        pygame.mixer.music.stop()
        self.is_playing = False
        self.play_button.base_widget.set_label("Play")
        self.progress.set_completion(0)
        self.progress_text.set_text("0:00 / 0:00")

    def next(self, *_):
        if not self.playlist:
            return
        self.current_index = (self.current_index + 1) % len(self.playlist)
        self.stop()
        self._play_current()
        self.is_playing = True
        self.play_button.base_widget.set_label("Pause")

    def previous(self, *_):
        if not self.playlist:
            return
        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.stop()
        self._play_current()
        self.is_playing = True
        self.play_button.base_widget.set_label("Pause")

    # volume
    def volume_up(self, *_):
        self.volume = min(1, self.volume + 0.05)
        pygame.mixer.music.set_volume(self.volume)
        self.vol_text.set_text(f"Volume {int(self.volume*100)}%")

    def volume_down(self, *_):
        self.volume = max(0, self.volume - 0.05)
        pygame.mixer.music.set_volume(self.volume)
        self.vol_text.set_text(f"Volume {int(self.volume*100)}%")

    # ──────────────────────────────────────────────────────────
    # playlist operations
    # ──────────────────────────────────────────────────────────
    def file_selected(self, path):
        if os.path.isdir(path):
            self.dir_browser.update_from_path(path)
        else:
            if os.path.splitext(path)[1].lower() in ('.mp3', '.wav', '.ogg', '.flac'):
                self._add_to_playlist(path)

    def _add_to_playlist(self, path):
        if not self.playlist:
            self.playlist_walker.clear()
        self.playlist.append(path)
        self.playlist_walker.append(
            urwid.AttrMap(urwid.SelectableIcon("🎵 "+os.path.basename(path)),
                          None, 'selected'))
        self._highlight_playlist()

    def play_selected_track(self, *_):
        if not self.playlist:
            return
        self.current_index = self.playlist_listbox.focus_position
        self.stop()
        self._play_current()
        self.is_playing = True
        self.play_button.base_widget.set_label("Pause")

    def remove_selected_track(self, *_):
        if not self.playlist:
            return
        idx = self.playlist_listbox.focus_position
        del self.playlist[idx]
        del self.playlist_walker[idx]
        if not self.playlist:
            self.stop()
            self.playlist_walker.append(urwid.Text("Playlist empty"))
            self.now_playing.set_text("Not playing")
        else:
            self.current_index = max(
                0, min(self.current_index, len(self.playlist)-1))
        self._highlight_playlist()

    def clear_playlist(self, *_):
        if not self.playlist:
            return
        self.playlist.clear()
        self.playlist_walker.clear()
        self.playlist_walker.append(urwid.Text("Playlist empty"))
        self.stop()
        self.now_playing.set_text("Not playing")

    def _highlight_playlist(self):
        for i, w in enumerate(self.playlist_walker):
            if isinstance(w, urwid.AttrMap):
                w.set_attr_map(
                    {None: 'playing' if i == self.current_index else None})

    # ──────────────────────────────────────────────────────────
    # helpers
    # ──────────────────────────────────────────────────────────
    def _length(self, path):
        if path in self.track_lengths:
            return self.track_lengths[path]
        if HAS_MUTAGEN:
            ext = os.path.splitext(path)[1].lower()
            try:
                length = {'.mp3': MP3, '.wav': WAVE, '.ogg': OggVorbis,
                          '.flac': FLAC}.get(ext, MP3)(path).info.length
                self.track_lengths[path] = length
                return length
            except:
                pass
        self.track_lengths[path] = 180
        return 180

    # background progress updater
    def _progress_loop(self):
        while True:
            if self.is_playing and self.playlist:
                length = self._length(self.playlist[self.current_index])
                elapsed = min(
                    time.time()-self.current_track_start_time, length)
                pct = elapsed/length
                m, s = divmod(int(elapsed), 60)
                tm, ts = divmod(int(length), 60)

                def _ui(_loop, _d):
                    self.progress.set_completion(pct)
                    self.progress_text.set_text(f"{m}:{s:02d} / {tm}:{ts:02d}")
                self.loop.set_alarm_in(0, _ui)

                if elapsed >= length-0.5:
                    self.loop.set_alarm_in(0.1, lambda *_: self.next())
            time.sleep(0.4)

    def quit(self):
        pygame.mixer.quit()
        raise urwid.ExitMainLoop()


# ╭──────────────────────────────────────────────────────────╮
# │  DIRECTORY BROWSER                                      │
# ╰──────────────────────────────────────────────────────────╯
class DirectoryBrowser(urwid.ListBox):
    """Simple explorer rooted at ~/Music (change path if desired)."""

    def __init__(self, callback):
        self.callback = callback
        self.current_dir = os.path.expanduser("~/Music")
        super().__init__(urwid.SimpleFocusListWalker(self._items(self.current_dir)))

    # build items list
    def _items(self, path):
        items = [urwid.AttrMap(urwid.SelectableIcon(".. (Parent Directory)"),
                               'dir', 'selected')]
        try:
            for name in sorted(os.listdir(path)):
                full = os.path.join(path, name)
                if os.path.isdir(full):
                    items.append(urwid.AttrMap(
                        urwid.SelectableIcon("📁 "+name), 'dir', 'selected'))
                elif os.path.splitext(name)[1].lower() in ('.mp3', '.wav', '.ogg', '.flac'):
                    items.append(urwid.AttrMap(
                        urwid.SelectableIcon("🎵 "+name), 'file', 'selected'))
        except Exception:
            items.append(urwid.Text("Error loading directory"))
        return items

    def update_from_path(self, path):
        self.current_dir = path
        self.body[:] = self._items(path)

    def open_selected(self):
        w, _ = self.get_focus()
        if not isinstance(w.original_widget, urwid.SelectableIcon):
            return
        label = w.original_widget.text
        if label.startswith(".."):
            new_path = os.path.dirname(self.current_dir)
            self.callback(new_path)
        elif label.startswith("📁 "):
            self.callback(os.path.join(self.current_dir, label[2:]))
        elif label.startswith("🎵 "):
            self.callback(os.path.join(self.current_dir, label[2:]))


# ╭──────────────────────────────────────────────────────────╮
# │  MAIN                                                   │
# ╰──────────────────────────────────────────────────────────╯
if __name__ == "__main__":
    MusicPlayer().run()
