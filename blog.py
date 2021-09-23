from peewee import *
import datetime
from collections import *
import sys
import os

db=SqliteDatabase('blog.db')

class Entry(Model):

    content = TextField()
    date = DateTimeField(default= datetime.datetime.now)
    class Meta:
        database= db
def __init__():
    db.connect()
    db.create_tables([Entry],safe=True)

def add_entry():
    """añade un registro en el blog"""
    print("Introduce tu registro, presiona CTR + S para guardar")
    data =sys.stdin.read().strip()
    if data:
        if input("Guardar entrada? [y/n ]").lower()!= 'n':
            Entry.create(content=data)
            print("Guardado correctamente")
    

def view_entries(search_texto=None):
    """ver los registros"""
    entries= Entry.select().order_by(Entry.date.desc())
    if search_texto :
        entries= entries.where(Entry.content.contains(search_texto))

    for entry in entries:
        date=entry.date.strftime('%A %B %d, %Y %I:%M%p' )
        clear()
        print(date)
        print("+"*len(date))
        print(entry.content)
        print("\n \n "+'+'*len(date)+'\n')
        print("n| siguiente registro")
        print("q| salir al menu")
        print("d| borrar registro")
        print()

        next_action= input("Acción a realizar: [n/q]").lower().strip()
        if next_action=="q":
            break
        if next_action=="d":
            delete_entry(entry)
  
        

  

def search_entries():
    """Busca una registro con cierto texto"""
    view_entries(input('texto a buscar: '))


def delete_entry(entry):
    """elimina una entrada de datos"""
    respone= input("Estás seguro? [y/n]").lower().strip()
    if respone == "y":
        entry.delete_instance()
        print("Registro borrado")


menu_list=OrderedDict([
    ('a',add_entry),
    ('v',view_entries),
    ('d',delete_entry),
    ('s',search_entries)
])
def menu():
    """muestra las opciones"""
    choice=None
    while choice != 'q':
        clear()
        print("presiona q para salir")
        for key, value in menu_list.items():
            print("{}| {}".format(key,value.__doc__))

        choice=input('Elección: ').lower().strip()
        if choice in menu_list:
            clear()
            menu_list[choice]()
    db.close()

def clear():
    os.system('cls' if os.name=="nt" else 'clear')
if __name__ == '__main__':
    __init__()
    menu()
    