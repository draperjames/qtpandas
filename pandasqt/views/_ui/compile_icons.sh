#!
# Compile the icons.qrc file for compatability mode

dir=$(dirname $0)

iconfile=${dir}/icons.qrc
outfile=${dir}/icons_rc.py
tmpfile=${outfile}.tmp

# Make backup copy of the output file if there isn't one
cp -n "${outfile}" "${outfile}.bak"




# Pick the compiler that exists.  FIXME: need more general solution for pyside
# http://stackoverflow.com/questions/592620/check-if-a-program-exists-from-a-bash-script
for com in pyrcc5 pyrcc4 pyrcc pyside-rcc pyside-rcc-3.5 pyside-rcc-2.7
do
    if  command -v ${com} > /dev/null
    then
        ${com} "$iconfile" > "$tmpfile"
        break
    fi
done

# Munge the file to make it universal
# Change strings to bytestrings for python-2.7/3.x compatibility
# Change PySide/PyQt* import to use the compatibility layer
cat "$tmpfile" |\
sed -e 's/= "\\/= b"\\/' \
    -e 's/Py[^ ]* /pandasqt.compat /' > "${outfile}"

