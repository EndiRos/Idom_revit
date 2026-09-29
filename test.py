from pythonnet import load

load("netfx")

import clr

WPF = r"C:\Windows\Microsoft.NET\Framework64\v4.0.30319\WPF"

clr.AddReference(WPF + r"\WindowsBase.dll")
clr.AddReference(WPF + r"\PresentationCore.dll")
clr.AddReference(WPF + r"\PresentationFramework.dll")

from System.Threading import Thread, ThreadStart, ApartmentState
from System.Windows import Application
from System.Windows.Markup import XamlReader
from System.IO import File


def run_wpf():
    stream = File.OpenRead(
        r"Idom.extension\sheets.tab\Sheets.panel\Sheet Generator.pushbutton\form.xaml"
    )

    window = XamlReader.Load(stream)

    btn = window.FindName("btnOK")
    txt = window.FindName("txtName")

    def on_click(sender, args):
        print(txt.Text)
        window.Close()

    btn.Click += on_click

    app = Application()
    app.Run(window)


t = Thread(ThreadStart(run_wpf))
t.SetApartmentState(ApartmentState.STA)
t.Start()
t.Join()