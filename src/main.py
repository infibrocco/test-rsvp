import json
import os
from datetime import datetime, timedelta
from pathlib import Path

import kivymd.icon_definitions

# from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp, sp
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton  # MDIconButton; , MDFabButton
from kivymd.uix.button import MDButtonIcon, MDButtonText
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.navigationdrawer import (  # MDNavigationLayout,; MDNavigationDrawerItem,; MDNavigationDrawerItemLeadingIcon,; MDNavigationDrawerItemText,; MDNavigationDrawerItemTrailingText,
    MDNavigationDrawer,
    MDNavigationDrawerDivider,
    MDNavigationDrawerLabel,
    MDNavigationDrawerMenu,
)
from kivymd.uix.responsivelayout import MDResponsiveLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.stacklayout import MDStackLayout
from kivymd.uix.textfield import MDTextField  # MDTextFieldTrailingIcon,
from kivymd.uix.textfield import (
    MDTextFieldHelperText,
    MDTextFieldHintText,
    MDTextFieldLeadingIcon,
    MDTextFieldMaxLengthText,
)

# from kivy.uix.button import Button
# from kivy.uix.floatlayout import FloatLayout
# from kivy.uix.textinput import TextInput

SCREEN_TITLE = "RSVP tests"


def hide_widget(wid, dohide=True):
    if hasattr(wid, "saved_attrs"):
        if not dohide:
            wid.height, wid.size_hint_y, wid.opacity, wid.disabled = wid.saved_attrs
            del wid.saved_attrs
    elif dohide:
        wid.saved_attrs = wid.height, wid.size_hint_y, wid.opacity, wid.disabled
        wid.height, wid.size_hint_y, wid.opacity, wid.disabled = 0, None, 0, True


# Window.size = (500, 300)


class MainApp(MDApp):
    def build(self):
        self.DEFAULT_FONT_SIZE = 10
        self.DEFAULT_LINE_HEIGHT = 10
        self.SKIP = 5
        self.WPM = 500
        self.BH = 100
        self.RTIME = 60 / self.WPM  # / 60
        self.LABEL_SHOW_W = 700
        self.chap_root = Path("rssg/")

        self.load_consts()

        self.title = SCREEN_TITLE
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Green"
        self.screen = MDScreen()
        self.blayout = MDBoxLayout(
            orientation="horizontal",
            size_hint=(1, 0.1),
            pos_hint={"right": 1, "top": 1},
        )
        self.b2layout = MDBoxLayout(
            orientation="horizontal",
            size_hint=(1, 0.1),
            pos_hint={"right": 1, "top": 0.899},
        )
        self.b3layout = MDStackLayout(
            orientation="lr-tb",
            size_hint=(1, 0.4),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            # rows=2,
            # cols=3,
            # padding=dp(200),
            spacing=dp(80),
            # row_default_height=20,
        )

        self.layout = MDFloatLayout()
        self.screen.add_widget(self.b3layout)
        self.screen.add_widget(self.blayout)
        self.screen.add_widget(self.b2layout)
        self.screen.add_widget(self.layout)
        self.reading_text = ""
        self.all_text = [""]
        self.word_index = 0 if not hasattr(self, "word_index") else self.word_index
        self.read_paused = False
        # self.chap_num = "777"
        self.load_chap()

        self.mtext = MDLabel(
            text=self.reading_text,
            line_height=self.DEFAULT_LINE_HEIGHT,
            halign="center",
            theme_font_size="Custom",
            font_size=sp(self.DEFAULT_FONT_SIZE * 4),
            # adaptive_size=True,
            # font_style="Display",
            # role="large",
            allow_selection=True,
            allow_copy=True,
            text_color="green",
            underline=True,
            # foreground_color=(0, 1, 0, 1),
            # background_color=(0, 0, 0, 0),
            # readonly=True,
            size_hint=(0.4, 0.2),
            pos_hint={"center_x": 0.5, "center_y": 0.65},
        )
        self.btext = MDLabel(
            text=" ".join(
                self.all_text[
                    self.word_index
                    + 2 : min(self.word_index + self.BH, len(self.all_text))
                ]
            ),
            line_height=self.DEFAULT_LINE_HEIGHT,
            halign="center",
            theme_height="Custom",
            theme_font_size="Custom",
            font_size=sp(self.DEFAULT_FONT_SIZE * 2),
            # justify=True,
            allow_selection=True,
            allow_copy=True,
            # foreground_color=(1, 1, 1, 1),
            # background_color=(0, 0, 0, 0),
            # readonly=True,
            size_hint=(1, None),
            height=dp(200),
            pos_hint={"center_x": 0.5, "top": 0},
        )
        self.side_text1 = MDLabel(
            text=self.all_text[self.word_index - 1],
            line_height=self.DEFAULT_LINE_HEIGHT,
            halign="center",
            theme_font_size="Custom",
            font_size=sp(self.DEFAULT_FONT_SIZE * 3),
            adaptive_size=True,
            allow_selection=True,
            allow_copy=True,
            # foreground_color=(1, 1, 1, 1),
            # background_color=(0, 0, 0, 0),
            # readonly=True,
            size_hint=(0.3, 0.2),
            pos_hint={"left": 1, "center_y": 0.65},
        )
        self.side_text2 = MDLabel(
            text=self.all_text[min(self.word_index + 1, len(self.all_text) - 1)],
            line_height=self.DEFAULT_LINE_HEIGHT,
            halign="center",
            theme_font_size="Custom",
            font_size=sp(self.DEFAULT_FONT_SIZE * 3),
            adaptive_size=True,
            allow_selection=True,
            allow_copy=True,
            # foreground_color=(1, 1, 1, 1),
            # background_color=(0, 0, 0, 0),
            # readonly=True,
            size_hint=(0.3, 0.2),
            pos_hint={"right": 1, "center_y": 0.65},
        )
        self.ibutton = MDButton(
            MDButtonIcon(icon="pause"),
            MDButtonText(text="Pause") if Window.width > self.LABEL_SHOW_W else None,
            theme_height="Custom",
            theme_width="Custom",
            theme_font_size="Custom",
            radius=[
                0,
            ],
            # font_size="12sp",
            # style="elevated",
            # size_hint=(0.135, 1),
            pos_hint={"x": 0.115, "top": 0.95},
            on_press=self.on_pause_press,
        )
        # self.ibutton = MDButton(
        #     MDButtonText(text="Pause"),
        #     size_hint=(0.1, 0.16),
        #     pos_hint={"x": 0.1, "top": 1},
        #     on_press=self.on_pause_press,
        # )
        self.bbutton = MDButton(
            MDButtonIcon(icon="step-backward"),
            MDButtonText(text="Back") if Window.width > self.LABEL_SHOW_W else None,
            theme_height="Custom",
            theme_width="Custom",
            theme_font_size="Custom",
            radius=[
                0,
            ],
            # size_hint=(0.115, 1),
            pos_hint={"x": 0, "top": 0.95},
            on_press=self.on_button_back,
        )
        self.fbutton = MDButton(
            MDButtonIcon(icon="step-forward"),
            MDButtonText(text="Forward") if Window.width > self.LABEL_SHOW_W else None,
            theme_height="Custom",
            theme_width="Custom",
            theme_font_size="Custom",
            radius=[
                0,
            ],
            # size_hint=(0.135, 1),
            pos_hint={"x": 0.25, "top": 0.95},
            on_press=self.on_button_forward,
        )
        self.est = MDLabel(
            text=str(
                (
                    datetime(1, 1, 1)
                    + timedelta(
                        minutes=((len(self.all_text) - self.word_index) / self.WPM)
                    )
                )
                .strftime("%M min %S sec")
                .lstrip("0")
            ),
            line_height=self.DEFAULT_LINE_HEIGHT,
            halign="center",
            theme_font_size="Custom",
            font_size=self.DEFAULT_FONT_SIZE * 2,
            adaptive_size=True,
            allow_selection=True,
            allow_copy=True,
            text_color="green",
            # foreground_color=(0, 1, 0, 1),
            # background_color=(0, 0, 0, 0),
            # readonly=True,
            size_hint=(0.4, 0.2),
            pos_hint={"x": 0, "top": 0.95},
        )
        self.nbutton = MDButton(
            MDButtonIcon(icon="skip-forward"),
            MDButtonText(text="Next") if Window.width > self.LABEL_SHOW_W else None,
            theme_height="Custom",
            theme_width="Custom",
            theme_font_size="Custom",
            radius=[
                0,
            ],
            # size_hint=(0.1, 1),
            pos_hint={"x": 0.9, "top": 0.95},
            on_press=self.on_chap_next,
        )

        self.chap = MDTextField(
            MDTextFieldLeadingIcon(
                icon="book-settings-outline",
            ),
            MDTextFieldHintText(
                text="Chapter num",
            ),
            # MDTextFieldHelperText(
            #     text="Enter the chapter number you want to read",
            #     mode="persistent",
            # ),
            MDTextFieldMaxLengthText(
                max_text_length=15,
            ),
            text="Chapter " + str(self.chap_num),
            mode="outlined",
            size_hint_x=1.4,
            theme_height="Custom",
            # height=1,
            pos_hint={"x": 0.715, "top": 0.9},
        )

        # self.chap = MDLabel(
        #     text=f"Chapter {self.chap_num}",
        #     line_height=self.DEFAULT_LINE_HEIGHT,
        #     halign="center",
        #     theme_font_size="Custom",
        #     font_size=self.DEFAULT_FONT_SIZE * 2,
        #     adaptive_size=True,
        #     allow_selection=True,
        #     allow_copy=True,
        #     # foreground_color=(1, 1, 1, 1),
        #     # background_color=(0, 0, 0, 0),
        #     # readonly=False,
        #     # multiline=False,
        #     size_hint=(0.2, 0.2),
        #     pos_hint={"x": 0.7, "top": 1.0},
        # )

        self.chap.bind(on_text_validate=self.text_valid)
        self.pbutton = MDButton(
            MDButtonIcon(icon="skip-backward"),
            MDButtonText(text="Previous") if Window.width > self.LABEL_SHOW_W else None,
            theme_height="Custom",
            theme_width="Custom",
            theme_font_size="Custom",
            radius=[
                0,
            ],
            # size_hint=(0.2, 1),
            # size_hint_x=1/7,
            pos_hint={"x": 0.575, "top": 0.95},
            on_press=self.on_chap_prev,
        )
        # self.wpm_text = MDLabel(
        #     text=f"WPM {self.WPM}",
        #     line_height=self.DEFAULT_LINE_HEIGHT,
        #     halign="center",
        #     theme_font_size="Custom",
        #     font_size=self.DEFAULT_FONT_SIZE * 2,
        #     adaptive_size=True,
        #     allow_selection=True,
        #     allow_copy=True,
        #     # foreground_color=(1, 1, 1, 1),
        #     # background_color=(0, 0, 0, 0),
        #     # readonly=False,
        #     # multiline=False,
        #     size_hint=(0.2, 0.2),
        #     pos_hint={"center_x": 0.5, "top": 1},
        # )

        self.wpm_text = MDTextField(
            MDTextFieldLeadingIcon(
                icon="car-speed-limiter",
            ),
            MDTextFieldHintText(
                text="Speed",
            ),
            MDTextFieldHelperText(
                text="(in WPM)",
                mode="persistent",
            ),
            MDTextFieldMaxLengthText(
                max_text_length=4,
            ),
            text=str(self.WPM),
            mode="outlined",
            # size_hint_x=1/7,
            theme_height="Custom",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            # height=0.1,
            # pos_hint={"x": 0.385, "top": 0.9},
        )

        self.wpm_text.bind(on_text_validate=self.wpm_valid)
        # self.debug_text = TextInput(
        #     text=f"debug {self.word_index}-{len(self.all_text)}",
        #     line_height=self.DEFAULT_LINE_HEIGHT,
        #     halign="center",
        #     font_size=self.DEFAULT_FONT_SIZE * 2,
        #     foreground_color=(1, 1, 1, 1),
        #     background_color=(0, 0, 0, 0),
        #     readonly=False,
        #     multiline=False,
        #     size_hint=(0.2, 0.2),
        #     pos_hint={"center_x": 0.5, "top": 0.65},
        # )

        self.btext_afield = MDTextField(
            MDTextFieldLeadingIcon(
                icon="text",
            ),
            MDTextFieldHintText(
                text="Shown text",
            ),
            MDTextFieldHelperText(
                text="amount of text (in words)",
                mode="persistent",
            ),
            MDTextFieldMaxLengthText(
                max_text_length=4,
            ),
            text=str(self.BH),
            mode="outlined",
            # size_hint_x=1/7,
            theme_height="Custom",
            # pos_hint={"center_x": .5, "center_y": .5}
            # height=0.1,
            # pos_hint={"x": 0.385, "top": 0.9},
        )
        self.btext_afield.bind(on_text_validate=self.bh_valid)

        self.chap_root_t = MDTextField(
            MDTextFieldLeadingIcon(
                icon="folder-settings-outline",
            ),
            MDTextFieldHintText(
                text="Chapter root",
            ),
            MDTextFieldHelperText(
                text="the main folder where chapters are stored",
                mode="persistent",
            ),
            MDTextFieldMaxLengthText(
                max_text_length=15,
            ),
            text=str(self.chap_root),
            mode="outlined",
            # size_hint_x=1.4,
            theme_height="Custom",
            # height=1,
            # pos_hint={"x": 0.715, "top": 0.9},
        )
        self.chap_root_t.bind(
            on_text_validate=lambda *_: setattr(
                self, "chap_root", Path(str(self.chap_root_t.text))
            )
        )

        # navdiv = MDNavigationDrawerDivider(spacing=10, padding=[20,40,20,40])

        self.nav_draw = MDNavigationDrawer(
            MDNavigationDrawerMenu(
                # navdiv,
                MDNavigationDrawerLabel(
                    text="Config",
                ),
                self.wpm_text,
                self.chap,
                self.btext_afield,
                self.chap_root_t,
                # MDNavigationDrawerDivider(),
                spacing=dp(30),
            ),
            id="nav_drawer",
            # radius=(0, dp(16), dp(16), 0),
            theme_elevation_level="Custom",
            # elevation_level=5,
            # drawer_type="standard",
            # on_open=self.on_pause_press,
            # padding=[dp(200), dp(200), dp(200), dp(200)],
        )
        self.nav_draw.on_open = lambda *_: self.on_pause_press(read_paused=False)
        self.nav_draw.on_close = lambda *_: self.on_pause_press(read_paused=True)

        # hide_widget(navdiv)

        self.nav_btn = MDButton(
            MDButtonIcon(icon="menu"),
            theme_height="Custom",
            theme_width="Custom",
            theme_font_size="Custom",
            radius=[
                0,
            ],
            style="elevated",
            # pos_hint={"left": 0, "top": .895},
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=(None, None),
            width=dp(55),
            height=dp(55),
            # size_hint=(.07, .1),
            on_press=lambda _: (self.nav_draw.set_state("toggle"), ...),
        )

        self.b3layout.add_widget(self.side_text1)
        self.b3layout.add_widget(self.mtext)
        self.b3layout.add_widget(self.side_text2)
        self.b3layout.add_widget(self.btext, index=0)
        self.layout.add_widget(self.est)
        self.blayout.add_widget(self.bbutton)
        self.blayout.add_widget(self.ibutton)
        self.blayout.add_widget(self.fbutton)
        # self.blayout.add_widget(self.wpm_text)
        # self.blayout.add_widget(self.chap)
        self.blayout.add_widget(self.pbutton)
        self.blayout.add_widget(self.nbutton)
        self.layout.add_widget(self.nav_draw)
        self.b2layout.add_widget(self.nav_btn)
        # layout.add_widget(self.debug_text)
        self.read_event = Clock.schedule_interval(self.on_read_update, self.RTIME)

        return self.screen

    def on_pause_press(self, *_args, read_paused=None):
        self.read_paused = read_paused if read_paused is not None else self.read_paused
        if not self.read_paused:
            self.read_paused = True
            self.read_event.cancel()
        else:
            self.read_paused = False
            self.read_event = Clock.schedule_interval(self.on_read_update, self.RTIME)

        self.update_all_text()
        self.blayout.remove_widget(self.ibutton)
        # self.screen.remove_widget(self.layout)
        self.ibutton = (
            MDButton(
                MDButtonIcon(icon="pause"),
                (
                    MDButtonText(text="Pause")
                    if Window.width > self.LABEL_SHOW_W
                    else None
                ),
                theme_height="Custom",
                theme_width="Custom",
                theme_font_size="Custom",
                radius=[
                    0,
                ],
                # size_hint=(0.135, 1),
                pos_hint={"x": 0.115, "top": 0.95},
                on_press=self.on_pause_press,
            )
            if not self.read_paused
            else MDButton(
                MDButtonIcon(icon="play"),
                (
                    MDButtonText(text="Resume")
                    if Window.width > self.LABEL_SHOW_W
                    else None
                ),
                theme_height="Custom",
                theme_width="Custom",
                theme_font_size="Custom",
                radius=[
                    0,
                ],
                # size_hint=(0.135, 1),
                pos_hint={"x": 0.115, "top": 0.95},
                on_press=self.on_pause_press,
            )
        )
        self.blayout.add_widget(self.ibutton, index=-1)
        # self.screen.add_widget(self.layout)

    def text_valid(self, *_args):
        self.chap_num = self.chap.text.lstrip("Chapter ")

        self.load_chap()

    def wpm_valid(self, *_args):
        self.WPM = min(int(self.wpm_text.text.lstrip("WPM ")), 9000)
        self.RTIME = 60 / self.WPM
        self.on_pause_press()
        self.on_pause_press()
        self.load_chap()
        self.update_all_text()

    def bh_valid(self, *_args):
        self.BH = min(max(int(self.btext_afield.text.strip()), 5), 900)

    def on_chap_prev(self, *_args):
        self.chap_num = str(int(self.chap_num) - 1)
        self.load_chap()
        self.update_all_text()

    def on_chap_next(self, *_args):
        self.chap_num = str(int(self.chap_num) + 1)
        self.load_chap()
        self.update_all_text()

    def on_button_back(self, *_args):
        self.word_index -= self.SKIP
        self.update_all_text()

    def on_button_forward(self, *_args):
        self.word_index += self.SKIP
        self.update_all_text()

    def on_read_update(self, _dt):
        self.word_index += 1
        self.update_all_text()
        # self.debug_text.text = f"debug {self.word_index}-{len(self.all_text)}"

        if self.word_index >= len(self.all_text) - 3:
            self.on_pause_press()
            self.word_index = 0
            self.chap_num = str(int(self.chap_num) + 1)
            self.load_chap()
            self.update_all_text()
            self.on_pause_press()

        if self.word_index >= 10:
            self.write_consts()
        #     self.read_event.cancel()

    def load_chap(self):
        self.chapters = [
            x.rstrip(".txt").strip()
            for x in os.listdir(self.chap_root)
            if "all" not in x
        ]
        chapf = str(self.chap_num).zfill(len(self.chapters[1]))
        with open(self.chap_root / f"{chapf}.txt") as f:
            self.all_text = f.read().split()
            self.reading_text = self.all_text[self.word_index]

        self.word_index = 0
        if hasattr(self, "chap"):
            self.chap.text = f"Chapter {self.chap_num}"

        self.write_consts()

    def load_consts(self):
        with open(Path("consts.json"), "r") as f:
            j = json.loads(f.read())
            self.DEFAULT_FONT_SIZE = j["DEFAULT_FONT_SIZE"]
            self.DEFAULT_LINE_HEIGHT = j["DEFAULT_LINE_HEIGHT"]
            self.WPM = j["WPM"]
            self.RTIME = 60 / self.WPM
            self.SKIP = j["SKIP"]
            self.BH = j["BH"]
            self.chap_num = j["CHAP"]
            self.word_index = j["INDEX"]

    def write_consts(self):
        with open(Path("consts.json"), "w") as f:
            j = json.dumps(
                {
                    "DEFAULT_FONT_SIZE": self.DEFAULT_FONT_SIZE,
                    "DEFAULT_LINE_HEIGHT": self.DEFAULT_LINE_HEIGHT,
                    "WPM": self.WPM,
                    "RTIME": self.RTIME,
                    "SKIP": self.SKIP,
                    "BH": self.BH,
                    "CHAP": self.chap_num,
                    "INDEX": self.word_index,
                }
            )
            f.write(j)

    def update_all_text(self):
        self.mtext.text = self.all_text[min(self.word_index, len(self.all_text) - 1)]
        self.btext.text = " ".join(
            self.all_text[
                self.word_index + 2 : min(self.word_index + self.BH, len(self.all_text))
            ]
        )
        self.side_text1.text = self.all_text[self.word_index - 1]
        self.side_text2.text = self.all_text[
            min(self.word_index + 1, len(self.all_text) - 1)
        ]
        self.est.text = f"""{(
            datetime(1,1,1)+
            timedelta(
                minutes=((len(self.all_text)-self.word_index)/self.WPM)))
                .strftime("%M min %S sec")
                .lstrip("0")}"""
        # self.chap.text =f"Chapter {self.chap_num}"
        # self.wpm_text.text =f"WPM {WPM}"


if __name__ == "__main__":
    app = MainApp()
    app.run()
