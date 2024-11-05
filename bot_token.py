import os

if os.name == "nt":
    cur_dir = os.path.dirname(__file__)
    new_dir = os.path.relpath(f'..\\data\\token.txt', cur_dir)
    txt = open(new_dir)
    token = txt.read()
elif os.name == "posix":
    cur_dir = os.path.dirname(__file__)
    new_dir = os.path.relpath(f'../data/token.txt', cur_dir)
    txt = open(new_dir)
    token = txt.read()