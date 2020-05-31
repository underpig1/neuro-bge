NAME=$(basename "$1" ".sh")
mkdir -p "$NAME.app/Contents/MacOS"
mv "$1" "$NAME.app/Contents/MacOS/$NAME"
chmod +x "$NAME.app/Contents/MacOS/$NAME"

mkdir -p "$NAME.app/Contents/Resources"
cp "$2" "$NAME.app/Contents/Resources/build.blend"
cp "$3" "$NAME.app/Contents/Resources/build.py"
