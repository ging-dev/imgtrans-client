#!/usr/bin/env python3
import os
import tempfile
import gi
import subprocess
from imgtrans import model, draw
from wand.image import Image
from threading import Thread
from typing import Any

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

class Application():
    def __init__(self) -> None:
        self.enable_translation = False
        self.builder = Gtk.Builder()
        self.builder.add_from_file("./resources/ui.glade")
        self.builder.connect_signals(self)

        window: Gtk.Window = self.get_object("main")
        window.connect("destroy", Gtk.main_quit)
        window.show_all()

    def on_choose_btn_file_set(self, choose: Gtk.FileChooserButton) -> None:
        filename = choose.get_filename()
        if filename is None:
            return
        thread = Thread(target=self.process_image, args=(filename,), daemon=True)
        thread.start()

    def state_set(self, _: Gtk.Switch, state: bool) -> None:
        self.enable_translation = state

    def process_image(self, filename: str):
        button: Gtk.FileChooserButton = self.get_object("choose_btn")
        spinner: Gtk.Spinner = self.get_object("spinner")
        status: Gtk.Label = self.get_object("status")

        button.hide()
        spinner.show()
        status.show()

        status.set_text("Đang nhận dạng...")
        tboxes = model.ocr(filename, paragraph=True)

        path = os.path.join(tempfile.gettempdir(), 'result.png')

        status.set_text("Đang dịch...")
        with Image(filename=filename) as image:
            draw.rectangle(image, tboxes, not self.enable_translation)
            if self.enable_translation:
                draw.translate(image, tboxes)
            image.save(filename=path)

        subprocess.Popen(["xdg-open", path])

        spinner.hide()
        status.hide()
        button.unselect_all()
        button.show()

    def about(self, about: Gtk.AboutDialog) -> None:
        about.show()

    def get_object(self, name: str) -> Any:
        return self.builder.get_object(name)

    def on_hide(self, widget: Gtk.Widget, _: Gdk.Event) -> bool:
        return widget.hide_on_delete()

    def main(self) -> None:
        Gtk.main()

if __name__ == "__main__":
    app = Application()
    app.main()
