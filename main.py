# -*- coding: utf-8 -*-
# @Author: E-NoR
# @Date:   2022-10-09 05:43:11
# @Last Modified by:   E-NoR
# @Last Modified time: 2022-10-10 22:29:10
import kivy

kivy.require('1.9.1')
import wcwidth
from threading import Thread

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.uix.pickers import MDDatePicker
from checkresult import main as result


class Calendar(BoxLayout):
    date, res = None, None
    money = (f'單程票價: {i}' for i in map(str, range(20, 61, 5)))
    holiday = (f'自訂休假天數: {i}' for i in map(str, range(0, 11)))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.date_dialog = self.createDatePicker(MDApp())
        self.ids.ti.readonly = True

    def createDatePicker(self, *args):
        date_dialog = MDDatePicker()
        date_dialog.min_year = date_dialog.sel_year
        date_dialog.max_year = date_dialog.sel_year + 3
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        return date_dialog

    def on_save(self, instance, value, date_range):
        self.date = str(value).replace('-', '')
        self.ids.startDate.text = f'起始日：{value}'

    def on_cancel(self, instance, value):
        '''Events called when the "CANCEL" dialog box button is clicked.'''

    def show_calendar(self):
        self.date_dialog.open()

    def calc(self):
        fixDate = lambda x: ''.join(v if i == 0 else v.zfill(2)
                                    for i, v in enumerate(x.split('/')))
        app = self.ids
        date = str(fixDate(app.startDate.text[4:]).replace('-', ''))
        money = int(
            self.ids.money.text[6:]) if self.ids.money.text[6:] != '' else None

        inputFail = sum(1 if i != '日' else 2 for i in (date, money)
                        if not i or i == '日')

        if inputFail:
            errorMsg = {1: '票價', 2: '日期', 3: '票價與日期'}
            app.ti.text = f'{errorMsg[inputFail]}為必填項目，請選擇後再執行。'
            return

        for i in app:
            if i == 'ti': continue
            app[i].disabled = True

        def th_job():
            holiday = int(self.ids.holiday.text[8:]
                          ) if self.ids.holiday.text != '自訂休假天數' else 0
            self.res = result(date, money, holiday)
            for i in app:
                if i == 'ti': continue
                app[i].disabled = False

        s = Thread(target=th_job)
        s.start()
        s.join()
        app.ti.text = str(self.res)


class mrt1280compare(App):

    def build(self):
        return Calendar()
        # return LoginScreen()


if __name__ == '__main__':
    mrt1280compare().run()