from kivy.config import Config
from kivy.effects.scroll import ScrollEffect
from kivy.network.urlrequest import UrlRequest
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.utils import platform
from kivy.animation import Animation, AnimationTransition
from kivy.clock import Clock
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.bottomnavigation import MDBottomNavigationItem, MDBottomNavigation
from kivymd.uix.card import MDCard
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.tab import MDTabsBase, MDTabs
from kivymd.uix.button import MDIconButton, MDFlatButton
from kivymd.uix.dialog import MDDialog

try:
    if platform == 'android':
        from kvdroid import navbar_color, statusbar_color
        from kvdroid import toast as native_toast
        from kvdroid.darkmode import dark_mode
    from logging import info, warning, critical, error, basicConfig, debug, DEBUG
    from json import dumps, loads
    from os.path import getmtime, isfile
    import datetime
    import time
    import webbrowser
    import locale
except (ImportError, NameError) as e:
    raise e
else:
    import_error = None

locale.setlocale(
    category=locale.LC_ALL,
    locale=""
)
__version__ = '0.0.7'
ip = '3.123.232.228'
port = '8000'
REGISTRATION_URL = f"http://{ip}:{port}/api/register"
TIMETABLE_URL = f"http://{ip}:{port}/api/timetable"
CHECK_URL = f'http://{ip}:{port}/test-api/check'


class RegistrationError(Exception):
    pass


class DownloadError(Exception):
    pass


def create_uuid():
    from uuid import uuid4
    user_id = uuid4()
    return user_id


class Tab(MDFloatLayout, MDTabsBase):
    pass


class NewsContent(MDBottomNavigationItem):
    pass


class TimetableContent(MDBottomNavigationItem):
    df = None


class SettingsContent(MDBottomNavigationItem):
    pass


class NavBar(MDBottomNavigation):
    pass


class LessonCard(FloatLayout):
    pass


class LessonCardMDCard(MDCard):
    pass


class NumLes:
    pass


class Time:
    pass


class NameLes:
    pass


class Cabinet:
    pass


class Menu:
    pass


class FullLessonScreen(Screen):
    pass


class MultilineLabel(Label):
    pass


class LessonsScroll(ScrollView):
    effect_cls = ScrollEffect


class WeekdaysTab(MDTabs):
    pass


class NotActualSnackBar(Snackbar):
    pass


class SkipTipsButton(MDFlatButton):
    pass


class BackTipsButton(MDIconButton):
    pass


class KRSTCApp(MDApp):
    dialog = None
    window_icon: str
    version = __version__
    tab_template = LessonsScroll()
    tab_template.add_widget(MDGridLayout(adaptive_height=True, cols=1))
    rus_days = {1: 'пн', 2: 'вт', 3: 'ср', 4: 'чт', 5: 'пт'}
    rus_weekdays = {'пн': 1, 'вт': 2, 'ср': 3, 'чт': 4, 'пт': 5}
    weekday = datetime.datetime.now().isoweekday()
    college_group = '12ИС-20К'
    if weekday > 5:
        weekday = 1
    selected_day = rus_days[weekday]
    touched_navtabs = {'timetable': False,
                       'news': False,
                       'settings': False}
    current_event = None

    @staticmethod
    def open_link(link):
        webbrowser.open(link)

    @staticmethod
    def show_toast(text):
        if platform == 'android':
            native_toast(text)
        else:
            toast(text)

    @staticmethod
    def itsint(pos_int: str):
        try:
            int(pos_int)
        except ValueError:
            double = pos_int.find('/')
            if double != -1:
                return True
            return False
        else:
            return True

    @staticmethod
    def fixtime(lesson_time):
        lesson_time: str
        new_time = lesson_time.replace('\n', '')
        return new_time

    @staticmethod
    def parse_rgb(r, g, b, a):
        value = [r / 255, g / 255, b / 255, a]
        return value

    @staticmethod
    def get_file_time():
        file_path = 'dfs.json'
        raw_time = getmtime(file_path)
        normal_time = time.strftime("%d %B %H:%M", time.gmtime(raw_time))
        return normal_time

    @staticmethod
    def empty_dfs():
        with open('dfs.json') as f:
            data = f.read()
            if data == '""':
                return True
            else:
                return False

    def get_uuid(self):
        uuid = self.config.get('general', 'id')
        return uuid

    def change_theme(self, theme):
        self.theme_cls.theme_style = theme
        self.config.set('interface', 'theme', theme)
        self.config.write()
        wt = self.root.ids['timetable'].ids['wt']
        wt.text_color_normal = [0.8,0.8,0.8,1]

    def switch_fpsshow(self):
        pre_value = self.config.getint('app', 'fps')
        self.config.set('app', 'fps', int(not pre_value))
        self.config.write()

    def change_nav_tips_button(self, screens):
        sm = screens[0].manager
        buttons = self.root.ids['tips_buttons']
        first_button = buttons.children[0]
        second_button = buttons.children[1]
        if isinstance(second_button, SkipTipsButton):
            buttons.remove_widget(second_button)
            test = sm.previous()
            test3 = sm.get_screen(test)
            test2 = BackTipsButton(on_press=lambda x: sm.switch_to(test3))
            buttons.add_widget(test2)
        elif isinstance(first_button, MDIconButton):
            buttons.remove_widget(first_button)
            test2 = SkipTipsButton(on_realise=lambda x: sm.switch_to('tips1'))
            buttons.add_widget(test2)

    def dismiss_dialog(self, *args):
        if self.dialog:
            self.dialog.dismiss()

    def close_app(self, *args):
        self.stop()

    # def prevent_switch(self, *args):
    #     if len(args) < 3:
    #         self.touched_navtabs[args[0].name] = True
    #         event = Clock.schedule_once(lambda dt: args[0].parent_widget.switch_tab(args[0].name))
    #         self.current_event = event
    #     else:
    #         self.current_event.cancel()

    def build(self):
        if platform != 'android' and platform != 'ios':
            self.icon = 'assets/rounded_icon.png'
            self.window_icon = 'assets/rounded_icon.png'
            self.title = 'Мой колледж'
        if platform == 'android':
            import jnius
            statusbar_color("#1668D6", 'white')
            navbar_color("#D8D8D8")

    def build_config(self, config):
        config.adddefaultsection('general')
        config.setdefault('general', 'id', create_uuid())
        config.adddefaultsection('interface')
        config.setdefault('interface', 'theme', 'Light')  # TODO: Если темная тема включена, то вкладки неправильно работают
        config.adddefaultsection('app')
        config.setdefault('app', 'fps', 0)

    # def on_start(self):
    #     Clock.schedule_once(lambda dt: self.welcome_text_animation(), 3)

    def on_start(self):
        config = self.config
        theme = config.get('interface', 'theme')
        fps = config.getint('app', 'fps')
        if theme == 'light' or theme == 'dark':
            theme = theme.capitalize()
            config.set('interface', 'theme', theme)
            config.write()
        self.theme_cls.theme_style = theme
        if fps:
            self.fps_monitor_start()

        from kivy.base import EventLoop
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)

        wt = self.root.ids['timetable'].ids['wt']
        wt.switch_tab(self.rus_days[self.weekday])
        self.change_data(None, None, None, self.rus_days[self.weekday])  # Тестовая функция
        sm = self.root.ids['settings'].ids['settings_sm']
        sm.current = 'main'

    def on_pause(self):
        self.config.write()
        return True

    def on_resume(self):
        self.change_data(None, None, None, self.selected_day)

    def hook_keyboard(self, window, key, *largs):
        if key == 27:
            self.dialog = MDDialog(
                text='Выйти из приложения?',
                buttons=[
                    MDFlatButton(
                        text='Нет',
                        text_color=self.theme_cls.primary_color,
                        font_size='18dp',
                        on_press=lambda x:self.dismiss_dialog()
                    ),
                    MDFlatButton(
                        text='Да!',
                        text_color=self.theme_cls.primary_color,
                        font_size='18dp',
                        on_press=lambda x:self.close_app()
                    )
                ]
            )
            current_nav_item = self.root.previous_tab
            if current_nav_item.name == 'settings':
                settings_sm = self.root.ids['settings'].ids['settings_sm']
                current_settings_item = settings_sm.current
                if current_settings_item == 'main':
                    self.dialog.open()
                else:
                    self.back_to_start()
            else:
                self.dialog.open()
            return True

    def welcome_text_animation(self):
        text = self.root.ids['welcome_screen'].ids['welcome_text']
        anim = Animation(y=dp(1000), t='in_out_back', duration=2)
        anim &= Animation(font_size=dp(36), duration=.2)
        anim.start(text)
        Clock.schedule_once(lambda dt: self.test_df(), 1.2)

    def test_df(self):
        sm = self.root
        sm.current = 'tips'

    def registration(self):
        uuid = self.get_uuid()
        body = {'id': uuid, 'group': self.college_group, 'app_ver': __version__}
        UrlRequest(url=REGISTRATION_URL,
                   req_headers={'Content-type': 'application/json'},
                   req_body=dumps(body),
                   method='POST',
                   on_success=print,
                   on_redirect=print,
                   on_failure=print,
                   on_error=print)

    def change_data(self, tabs, tab, tab_label, str_label):
        self.selected_day = str_label
        timetable = self.root.ids['timetable']
        if timetable.df is None:
            try:
                self.check_request()
            except Exception as e:
                snackbar = NotActualSnackBar(text="Возникла критическая ошибка", bg_color=(1, 0, 0, 1))
                critical(f'ошибка {e}')
                snackbar.open()
        else:
            try:
                self.show_timetable()
            except Exception as e:
                snackbar = NotActualSnackBar(text="Возникла критическая ошибка", bg_color=(1, 0, 0, 1))
                critical(f'ошибка {e}')
                snackbar.open()

    def check_request(self):
        if not isfile('dfs.json'):
            self.get_dataframe()
            return
        uuid = self.get_uuid()
        mod_time = getmtime('dfs.json')
        data = {'id': str(uuid), 'time': mod_time}
        body = dumps(data)
        wt = self.root.ids['timetable'].ids['wt']
        wt.switch_tab(self.rus_days[self.weekday])
        current_tab = self.root.ids['timetable'].ids[self.selected_day]
        if len(current_tab.children) != 0:
            if not isinstance(current_tab.children[0], FloatLayout):
                return  # тестовая функция
        current_tab = self.root.ids['timetable'].ids[self.selected_day]
        spiner = FloatLayout()
        spiner.add_widget(MDSpinner(pos_hint={'center_x': 0.5, 'center_y': 0.5}, size_hint=[None, None]))
        current_tab.add_widget(spiner)
        UrlRequest(url=CHECK_URL,
                   method='GET',
                   req_headers={'Content-type': 'application/json'},
                   req_body=body,
                   on_success=self.actuality_check,
                   on_redirect=self.load_and_show,
                   on_error=self.load_and_show,
                   on_failure=self.actuality_check)

    def actuality_check(self, req, res):
        if res != {}:
            actual = res['result']
        else:
            actual = False
        empty = self.empty_dfs()
        if not actual or empty:
            self.get_dataframe()
        else:
            try:
                self.load_and_show(req, res, actual=True)
            except Exception as e:
                snackbar = NotActualSnackBar(text="Возникла критическая ошибка", bg_color=(1, 0, 0, 1))
                critical(f'ошибка {e}')
                snackbar.open()

    def get_dataframe(self):
        uuid = self.get_uuid()
        data = {'id': str(uuid)}
        body = dumps(data)
        UrlRequest(url=TIMETABLE_URL,
                   method='GET',
                   verify=False,
                   req_body=body,
                   req_headers={'Content-type': 'application/json'},
                   on_error=self.load_and_show,
                   on_failure=self.load_and_show,
                   on_redirect=self.load_and_show,
                   on_success=self.save_and_show)

    def load_and_show(self, req, res, actual=False, *args):
        if not actual:
            snackbar = NotActualSnackBar(text=f"Загружено расписание от {self.get_file_time()}",
                                         bg_color=(0.4, 0.4, 0.4, 1))
            snackbar.open()
        # else:
        #     snackbar = NotActualSnackBar(text=f"Расписание актуально, скачивание не нужно",
        #                                  bg_color=self.parse_rgb(80, 200, 120, 1))
        #     snackbar.open()
        if not isfile('dfs.json'):
            return
        with open('dfs.json', 'r') as jsn:
            jsn_text = jsn.read()
            self.save_in_var(loads(jsn_text))

    def save_and_show(self, req, res, *args):
        jsn_text = dumps(res)
        if req.resp_status == 200:
            with open('dfs.json', 'w') as jsn:
                jsn.write(jsn_text)
                jsn.close()
            self.save_in_var(loads(jsn_text))
        elif req.resp_status == 204:
            self.registration()
            current_tab = self.root.ids['timetable'].ids[self.selected_day]
            if len(current_tab.children) != 0:
                if isinstance(current_tab.children[0], FloatLayout):
                    current_tab.remove_widget(current_tab.children[0])
            self.change_data(None, None, None, self.selected_day)
        else:
            snackbar = NotActualSnackBar(text="Возникла ошибка при сохранении расписания", bg_color=(1, 0, 0, 1))
            critical(f'HTTP код: {req.resp_status}')
            snackbar.open()

    def save_in_var(self, jsn):
        timetable = self.root.ids['timetable']
        timetable.df = loads(jsn)
        self.show_timetable()

    def show_timetable(self):
        current_tab = self.root.ids['timetable'].ids[self.selected_day]
        timetable = self.root.ids['timetable']
        if len(current_tab.children) != 0:
            if not isinstance(current_tab.children[0], FloatLayout):
                return
        tab_data = LessonsScroll()
        tab_data.add_widget(MDGridLayout(adaptive_height=True, cols=1))
        df = timetable.df
        day_timetable = df[self.selected_day]
        empty_lessons = 0
        for score, lesson in enumerate(day_timetable.values()):
            if lesson['lessons'] is None:
                empty_lessons += 1
                if empty_lessons == len(day_timetable):
                    lesson_widget = LessonCard()
                    lesson_widget.id = f'lesson{1}'
                    lesson_widget.count = '0'
                    lesson_widget.time = '--:-- - --:--'
                    lesson_widget.name_les = 'Нет уроков!'
                    lesson_widget.cabinet = ''
                    tab_data.children[0].add_widget(lesson_widget)
                    if len(current_tab.children) != 0:
                        current_tab.remove_widget(current_tab.children[0])
                    current_tab.add_widget(tab_data)
                continue

            count_of_lesson = score + 1
            lesson_widget = LessonCard()
            lesson_widget.id = f'lesson{count_of_lesson}'
            lesson_widget.count = count_of_lesson
            lesson_widget.time = lesson['time']
            if not lesson['lessons']:
                lesson_widget.name_les = 'null'
                snackbar = NotActualSnackBar(text="Возникла критическая ошибка", bg_color=(1, 0, 0, 1))
                snackbar.open()
            else:
                lesson_widget.name_les = lesson['lessons']
            if isinstance(lesson['cabinets'], float):
                lesson_widget.cabinet = str(int(lesson['cabinets']))
            elif lesson['cabinets'] is None:
                lesson_widget.cabinet = ''
            else:
                lesson_widget.cabinet = lesson['cabinets']

            tab_data.children[0].add_widget(lesson_widget)
        if len(current_tab.children) != 0:
            current_tab.remove_widget(current_tab.children[0])
        current_tab.add_widget(tab_data)

    def add_backbutton(self, *args):
        settings_tb = self.root.ids['settings'].ids['settings_tb']
        settings_tb.left_action_items = [['arrow-left', self.back_to_start]]

    def back_to_start(self, *args):
        settings_sm = self.root.ids['settings'].ids['settings_sm']
        settings_tb = self.root.ids['settings'].ids['settings_tb']
        settings_sm.current = 'main'
        settings_tb.title = 'Настройки'
        settings_tb.left_action_items = []


if __name__ == '__main__':
    Config.set('graphics', 'minimum_width', 350)
    Config.set('graphics', 'minimum_height', 300)
    Config.set('graphics', 'max_fps', 300)
    app = KRSTCApp()
    app.run()
