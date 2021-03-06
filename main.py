from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton, MDFloatingActionButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
#from content import KV, KC, list_helper, check
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivymd.uix.list import OneLineAvatarIconListItem, OneLineListItem
from kivy.storage.jsonstore import JsonStore
# from kivy.uix.screenmanager import ScreenManager, Screen

KV = """
<Content>
    MDTextField:
        hint_text: "Here"
        required: True
        helper_text_mode: "on_error"
        helper_text: "Enter text"
"""

KC = """
<ItemConfirm>
    on_release: root.set_icon(check)

    CheckboxRightWidget:
        id: check
        group: "check"
"""

list_helper = """
Screen:
    BoxLayout:
        orientation:'vertical'
        MDToolbar:
            title: 'Movies and TV Shows'
        #ScrollView:
            #MDList:
                #id: container

        MDBottomNavigation:
            MDBottomNavigationItem:
                name:"Movies"
                icon: "movie"
                text: "Movies"
                #on_release: app.toggleScreen()
                #id:

                ScrollView:
                    MDList:
                        id: containerMovies

                MDFloatingActionButton:
                    icon:'language-python'
                    pos_hint:{'center_x': 0.5, 'center_y': 0.1}
                    on_release: app.addDialog(containerMovies)

            MDBottomNavigationItem:
                name:"TV Shows"
                icon: "television-classic"
                text: "TV Shows"

                ScrollView:
                    MDList:
                        id: containerShows

                MDFloatingActionButton:
                    icon:'language-python'
                    pos_hint:{'center_x': 0.5, 'center_y': 0.1}
                    on_release: app.addDialogShow(containerShows)
"""

check = """
Label:
    id:checkLabel
    text:""
CheckBoxRightWidget:
    id:checkcheck

"""

class Media:
    def __init__(self, name, rating, media):
        self.media = media
        self.name = name
        self.rating = rating

    def setRating(self, rating):
        self.rating = rating


class Content(BoxLayout):
    pass


class ItemConfirm(OneLineAvatarIconListItem):
    divider = None

    def set_icon(self, instance_check):
        instance_check.active = True
        check_list = instance_check.get_widgets(instance_check.group)
        for check in check_list:
            if check != instance_check:
                check.active = False


class DemoApp(MDApp):

    def build(self):
        self.icon = 'Icon.png'
        self.theme_cls.primary_palette = 'Orange'  # (1, 193/255.0, 7/255.0, 1)
        self.mediaList = []
        self.store = JsonStore('store.json')
        screen = Builder.load_string(list_helper)
        btn_flat = MDFloatingActionButton(icon='language-python',
                                          pos_hint={'center_x': 0.5, 'center_y': 0.1},
                                          on_release=self.addDialog)
        self.movieInput = Builder.load_string(KV)
        self.movieRating = Builder.load_string(KC)

        self.movieCount = 0
        # screen.add_widget(btn_flat)
        return screen

    def addToMovieList(self, name, rating, media):
        if name == "":
            return
        self.mediaList.append(Media(name, rating, media))
        # self.store.put(self.movieCount, id=self.movieCount, name=name, rating=rating)

        item = OneLineListItem(text=name, on_release=self.ratingDialog)
        self.movieCount += 1
        self.root.ids.containerMovies.add_widget(item)

        self.selectedMovieListItem = item
        self.colorMovie(rating)

    def addToShowList(self, name, rating, media):
        self.mediaList.append(Media(name, rating, media))
        # self.store.put(self.movieCount, id=self.movieCount, name=name, rating=rating)

        item = OneLineListItem(text=name, on_release=self.ratingDialog)
        self.movieCount += 1
        self.root.ids.containerShows.add_widget(item)

        self.selectedMovieListItem = item
        self.colorMovie(rating)

    def on_start(self):
        for key in self.store.keys():
            if str(self.store.get(key)['media']) == "movie":
                self.addToMovieList(str(key), str(self.store.get(key)['rating']), str(self.store.get(key)['media']))
            else:
                self.addToShowList(str(key), str(self.store.get(key)['rating']), str(self.store.get(key)['media']))

    def on_stop(self):
        for i in self.mediaList:
            self.store.put(i.name, rating=i.rating, media=i.media)

    def ratingDialog(self, obj):
        self.selectedMovieListItem = obj
        close_btn = MDFlatButton(text='Close', on_release=self.close_dialog)
        rate_btn = MDFlatButton(text='Rate', on_release=self.rateMovie)
        del_btn = MDFlatButton(text='Delete movie', text_color=(1, 0, 0, 1), on_release=self.deleteMovie)
        self.dialog = MDDialog(title='Rate Movie "' + self.selectedMovieListItem.text + "\"",
                               type='confirmation',
                               items=[
                                   ItemConfirm(text="Good"),
                                   ItemConfirm(text="Normal"),
                                   ItemConfirm(text="Bad")
                               ],
                               size_hint=(0.7, 1),
                               buttons=[rate_btn, del_btn, close_btn])
        self.dialog.open()

    def addDialog(self, obj):
        # print(obj.ids.containerMovies == None)

        close_btn = MDFlatButton(text='Close', on_release=self.close_dialog)
        add_btn = MDFlatButton(text='Add', on_release=self.addMovie)
        self.dialog = MDDialog(title='Add Movie',
                               type='custom',
                               content_cls=Content(),
                               size_hint=(0.7, 1),
                               buttons=[add_btn, close_btn])
        self.dialog.open()

    def addDialogShow(self, obj):
        close_btn = MDFlatButton(text='Close', on_release=self.close_dialog)
        add_btn = MDFlatButton(text='Add', on_release=self.addShow)
        self.dialog = MDDialog(title='Add TV Show',
                               type='custom',
                               content_cls=Content(),
                               size_hint=(0.7, 1),
                               buttons=[add_btn, close_btn])
        self.dialog.open()

    def close_dialog(self, obj):
        self.dialog.dismiss()

    def addMovie(self, obj):
        for obj in self.dialog.content_cls.children:
            if isinstance(obj, MDTextField):
                # print(obj.text)
                if obj.text != "":
                    self.store.put(obj.text, rating="", media='movie')
                    self.addToMovieList(obj.text, "", 'movie')
                    self.dialog.dismiss()
        # self.dialog.dismiss()


    def addShow(self, obj):
        for obj in self.dialog.content_cls.children:
            if isinstance(obj, MDTextField):
                # print(obj.text)
                if obj.text != "":
                    self.store.put(obj.text, rating="", media='show')
                    self.addToShowList(obj.text, "", 'show')
                    self.dialog.dismiss()

    def rateMovie(self, obj):
        for obj in self.dialog.items:
            if isinstance(obj, ItemConfirm):
                if obj.ids.check.active:
                    self.colorMovie(obj.text)

                    for media in self.mediaList:
                        if media.name == self.selectedMovieListItem.text:
                            media.setRating(obj.text)
                            self.store.put(media.name, rating=media.rating, media=media.media)
                            break
                    # print(obj.text)
        self.dialog.dismiss()

    def deleteMovie(self, obj):
        idz = 0
        for media in self.mediaList:
            if media.name == self.selectedMovieListItem.text:
                break
            idz += 1
        if self.mediaList[idz].media == "movie":
            self.root.ids.containerMovies.remove_widget(self.selectedMovieListItem)
        else:
            self.root.ids.containerShows.remove_widget(self.selectedMovieListItem)
        self.mediaList.pop(idz)
        self.store.delete(self.selectedMovieListItem.text)
        self.movieCount -= 1

        self.dialog.dismiss()

    def colorMovie(self, rating):
        if rating == "Good":
            self.selectedMovieListItem.bg_color = (204 / 255.0, 255 / 255.0, 204 / 255.0, 1)
        elif rating == "Normal":
            self.selectedMovieListItem.bg_color = (255 / 255.0, 255 / 255.0, 204 / 255.0, 1)
        elif rating == "Bad":
            self.selectedMovieListItem.bg_color = (255 / 255.0, 153 / 255.0, 153 / 255.0, 1)

    # def toggleScreen(self):


DemoApp().run()
