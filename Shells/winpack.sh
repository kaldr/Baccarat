python3  -m PyInstaller --name Baccarat ./app.py
mv  Baccarat.spec Baccarat.old.spec
{ echo 'from kivy.deps import sdl2, glew'; cat Baccarat.old.spec; } > Baccarat.spec