#!/usr/bin/env python
# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.modalview import ModalView
from kivy.config import Config
import threading
import serial
import sys
import time


class TesterKivyApp(App):

    def __init__(self):
        super(TesterKivyApp, self).__init__()
        self.stop_event = threading.Event()
        self.stop_event.clear()
        self.recv_thread = threading.Thread(target=self.recv_main)
        self.seri = None
        self.seri_close_flag = False

    def thread_start(self):
        self.recv_thread.start()

    def open_serial(self, port="/dev/ttyUSB0", baud=115200):
        while (self.seri is None) and (not self.seri_close_flag):
            try:
                self.seri = serial.Serial(port=port, baudrate=baud, timeout=0.01)
            except:
                sys.stderr.write("serial open error\n")
                if hasattr(self, "textbox_log"):
                    self.textbox_log.text += "serial open error. please check connection to %s\n" % port
                time.sleep(0.1)


    def build(self):
        root = BoxLayout(orientation=('vertical'), padding=20)
        Window.bind(on_resize=self.resize_font)
        scrollview1 = ScrollView(size_hint_y=0.5,
                                 spacing=20, padding=20)
        boxlayout1 = BoxLayout(size_hint_y=0.15, spacing=20, padding=10)#, padding=20)
        boxlayout2 = BoxLayout(size_hint_y=0.35, spacing=20,
                               orientation=('vertical'))
                               #padding=20)
        root.add_widget(scrollview1)
        root.add_widget(boxlayout1)
        root.add_widget(boxlayout2)
        self.font_name_ja = './fonts/fonts-japanese-gothic.ttf'
        font_name_digi = './fonts/DS-DIGI.TTF'

        self.buttons = []
        for (txt, i) in zip([u'赤城', u'森永', u'ロッテ', u'明治'],
                            ['akagi', 'morinaga', 'lotte', 'meiji']):
            self.buttons.append(Button(text=txt,
                                       font_name=self.font_name_ja, id=i))
            self.buttons[-1].bind(on_press=self.show_modalview)
            boxlayout1.add_widget(self.buttons[-1])
            
        gridlayout1 = GridLayout(spacing=20,
                                 col_force_default=False,
                                 cols=5, rows=4)
                                 #padding=20)
        scrollview1.add_widget(gridlayout1)
        # もし左詰めが見にくければ、
        # *LayoutとLabelを使って背景色とalignを実現する
        self.textboxes = []
        for i in range(20):
            self.textboxes.append(
                TextInput(readonly=True, font_name=font_name_digi,
                          text=str(16000+i), font_size=20,
                          background_color=[0.2, 0.7, 0.6, 1],
                          multiline=False,
                          border=[6, 6, 6, 6]))
            gridlayout1.add_widget(self.textboxes[-1])
        
        self.textbox_msg = TextInput(size_hint_y=0.2,
                                     font_name=self.font_name_ja,
                                     multiline=False, readonly=True,
                                     foreground_color=[0,0,0,1],
                                     background_color=[0.9, 0.9, 0.9, 1],
                                     font_size=12)
        boxlayout2.add_widget(self.textbox_msg)
        
        self.textbox_log = TextInput(size_hint_y=0.8,
                                     font_name=self.font_name_ja,
                                     readonly=True,
                                     font_size=12)
        boxlayout2.add_widget(self.textbox_log)

        return root


    def show_modalview(self, src):
        self.textbox_log.text += u"pressed %s button\n" % src.text
        confirmation_text = u"""この設定を送信しても
良いですか？

Is it really OK
to send message
with this configuration?"""
        self.modalview = ModalView(size_hint = (0.5, 0.5), auto_dismiss=False)
        boxlayout = BoxLayout(orientation='vertical',padding=20, spacing=10)
        boxlayout.add_widget(Label(size_hint_y=0.6,text=confirmation_text,
                                   font_name=self.font_name_ja,
                                   halign='center', valign='middle'))
        button_ok = Button(size_hint_y = 0.2, text="OK", padding=[20, 20])
        button_ok.id = src.id
        button_no = Button(size_hint_y = 0.2, text="NO", id="no",
                           padding=[20, 20])
        boxlayout.add_widget(button_ok)
        boxlayout.add_widget(button_no)
        
        self.modalview.add_widget(boxlayout)
        button_ok.bind(on_press=self.dismiss_modalview)
        button_no.bind(on_press=self.dismiss_modalview)
        self.modalview.open()


    def dismiss_modalview(self, src):
        self.modalview.dismiss()
        if src.id == "no":
            return
        self.transmit_message(src.id)
        self.clear_indicators()


    def transmit_message(self, company):
        if company == "akagi":
            #ここに送信するmessageを記載する
            pass
        elif company == "morinaga":
            pass
        elif company == "lotte":
            pass
        elif company == "meiji":
            pass
        else:
            pass


    def clear_indicators(self):
        initial_value = 0
        for tb in self.textboxes:
            tb.text = str(initial_value)


    def resize_font(self,src1, src2, src3):
        #print "height %s" % self.root.height
        #print "width %s" % self.root.width
        if self.root.height > 590:
            if self.root.width > 650:
                #print "font_size=43"
                for tb in self.textboxes:
                    tb.font_size=43
            elif self.root.width > 610:
                #print "font_size=38"
                for tb in self.textboxes:
                    tb.font_size=38
            elif self.root.width > 560:
                #print "font_size=32"
                for tb in self.textboxes:
                    tb.font_size=32
            else:
                #print "font_size=30"
                for tb in self.textboxes:
                    tb.font_size=30

        elif self.root.height > 580:
            if self.root.width > 650:
                #print "font_size=40"
                for tb in self.textboxes:
                    tb.font_size=40
            elif self.root.width > 610:
                #print "font_size=38"
                for tb in self.textboxes:
                    tb.font_size=38
            elif self.root.width > 560:
                #print "font_size=32"
                for tb in self.textboxes:
                    tb.font_size=32
            else:
                #print "font_size=30"
                for tb in self.textboxes:
                    tb.font_size=30

        elif self.root.height > 555:
            if self.root.width > 560:
                #print "font_size=32"
                for tb in self.textboxes:
                    tb.font_size=32
            else:
                #print "font_size=30"
                for tb in self.textboxes:
                    tb.font_size=30

        elif self.root.height > 540:
            #print "font_size=28"
            for tb in self.textboxes:
                tb.font_size=28

        elif self.root.height > 530:
            #print "font_size=26"
            for tb in self.textboxes:
                tb.font_size=26
        elif self.root.height > 520:
            #print "font_size=24"
            for tb in self.textboxes:
                tb.font_size=24
        elif self.root.height > 500:
            #print "font_size=22"
            for tb in self.textboxes:
                tb.font_size=22
        elif self.root.height > 450:
            #print "font_size=20"
            for tb in self.textboxes:
                tb.font_size=20
        elif self.root.height > 400:
            #print "font_size=18"
            for tb in self.textboxes:
                tb.font_size=18
        elif self.root.height > 350:
            #print "font_size=16"
            for tb in self.textboxes:
                tb.font_size=16


    def update_indicators(self, data):
        if len(data) != len(self.textboxes):
            sys.stderr.write("data length is not same with num. of indicators\n")
            return
        for (tb, d) in zip(self.textboxes, data):
            tb.text = str(d)


    def recv_main(self):
        self.open_serial(port="/dev/ttyUSB0", baud=115200)
        # for test
        data_indicators = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
                           10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
        while not self.stop_event.is_set():
            time.sleep(0.01)
            if self.seri is None:
                continue
            try:
                recv = self.seri.read()
            except serial.serialutil.SerialException:
                pass
            # このあたりで解析処理を記載する
            self.update_indicators(data_indicators)
            

    def recv_stop(self):
        self.stop_event.set()
        if not self.seri is None:
            print "close serialport %s" % self.seri.port
            self.seri.close()
        self.recv_thread.join()


if __name__ == '__main__':
    tkapp = TesterKivyApp()
    Window.size = (770,420)
    tkapp.thread_start()
    try:
        tkapp.run()
    except KeyboardInterrupt:
        pass
    tkapp.seri_close_flag = True
    tkapp.recv_stop()

