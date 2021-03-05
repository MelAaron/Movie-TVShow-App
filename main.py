from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton, MDFloatingActionButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
# from content import KV, KC, list_helper
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivymd.uix.list import OneLineAvatarIconListItem, OneLineListItem
from kivy.storage.jsonstore import JsonStore


KV = """
<Content>
    MDTextField:
        hint_text: "Movie"
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
            title: 'Movies'
        ScrollView:
            MDList:
                id: container
"""

check = """
Label:
    id:checkLabel
    text:""
CheckBoxRightWidget:
    id:checkcheck

"""

class Media:
    def __init__(self, id, name, rating):
        self.id = id
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
        self.theme_cls.primary_palette = 'Orange'#(1, 193/255.0, 7/255.0, 1)
        self.mediaList = []
        self.store = JsonStore('store.json')
        screen = Builder.load_string(list_helper)
        btn_flat = MDFloatingActionButton(icon='language-python',
                                          pos_hint={'center_x': 0.8, 'center_y': 0.1},
                                          on_release=self.addDialog)
        self.movieInput = Builder.load_string(KV)
        self.movieRating = Builder.load_string(KC)

        self.movieCount = 0
        screen.add_widget(btn_flat)
        return screen

    def addToMovieList(self, name, rating):
        self.mediaList.append(Media(self.movieCount, name, rating))
        # self.store.put(self.movieCount, id=self.movieCount, name=name, rating=rating)

        item = OneLineListItem(text=name, on_release=self.ratingDialog)
        self.movieCount += 1
        self.root.ids.container.add_widget(item)

        self.selectedMovieListItem = item
        self.colorMovie(rating)


    def on_start(self):
        for key in self.store.keys():
            self.addToMovieList(str(key), str(self.store.get(key)['rating']))

    def on_stop(self):
        for i in self.mediaList:
            self.store.put(i.name, rating=i.rating)

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
        close_btn = MDFlatButton(text='Close', on_release=self.close_dialog)
        add_btn = MDFlatButton(text='Add', on_release=self.addMovie)
        self.dialog = MDDialog(title='Add Movie',
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
                self.store.put(obj.text, rating="")
                self.addToMovieList(obj.text, "")
                self.dialog.dismiss()
        self.dialog.dismiss()

    def rateMovie(self, obj):
        for obj in self.dialog.items:
            if isinstance(obj, ItemConfirm):
                if obj.ids.check.active:
                    self.colorMovie(obj.text)

                    for media in self.mediaList:
                        if media.name == self.selectedMovieListItem.text:
                            media.setRating(obj.text)
                            self.store.put(media.name, rating=media.rating)
                            break
                    # print(obj.text)
        self.dialog.dismiss()

    def deleteMovie(self, obj):
        idz = 0
        for media in self.mediaList:
            if media.name == self.selectedMovieListItem.text:
                #print(media.name + " " + str(media.id))
                break
            idz += 1
        print(idz)
        self.mediaList.pop(idz)
        self.store.delete(self.selectedMovieListItem.text)
        self.movieCount -= 1
        self.root.ids.container.remove_widget(self.selectedMovieListItem)
        self.dialog.dismiss()

    def colorMovie(self, rating):
        if rating == "Good":
            self.selectedMovieListItem.bg_color = (204 / 255.0, 255 / 255.0, 204 / 255.0, 1)
        elif rating == "Normal":
            self.selectedMovieListItem.bg_color = (255 / 255.0, 255 / 255.0, 204 / 255.0, 1)
        elif rating == "Bad":
            self.selectedMovieListItem.bg_color = (255 / 255.0, 153 / 255.0, 153 / 255.0, 1)


DemoApp().run()