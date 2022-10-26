#!/usr/bin/env python3
from threading import Thread
from time import sleep
from typing import Any
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf, Gdk

class Application():
    def __init__(self) -> None:
        self.builder = Gtk.Builder()
        self.builder.add_from_file("./resources/ui.glade")
        self.builder.connect_signals(self)

        window: Gtk.Window = self.get_object("main")
        window.connect("destroy", Gtk.main_quit)
        window.show_all()

    def open(self, file_chooser: Gtk.FileChooserDialog) -> None:
        file_name = file_chooser.get_filename()

        if file_name is None:
            file_chooser.show()
            return

        Thread(target=self.process_image, daemon=True, args=(file_name,)).start()

        file_chooser.unselect_all()
        file_chooser.hide()

    def process_image(self, file_name: str):
        image: Gtk.Image = self.get_object("image")
        spinner: Gtk.Spinner = self.get_object("spinner")
        status: Gtk.Label = self.get_object("status")

        image.hide()
        spinner.show()
        status.set_text("Loading image...")
        status.show()

        # Some works
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(filename=file_name, width=600, height=400)
        sleep(2)

        image.set_from_pixbuf(pixbuf)
        spinner.hide()
        status.hide()
        image.show()

    def about(self, about: Gtk.AboutDialog) -> None:
        about.show()

    def get_object(self, name: str) -> Any:
        return self.builder.get_object(name)

    def on_hide(self, widget: Gtk.Widget, event: Gdk.Event) -> bool:
        return widget.hide_on_delete()

    def main(self) -> None:
        Gtk.main()

app = Application()
app.main()
