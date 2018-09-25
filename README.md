# How to patch https://github.com/squell/bb-scripts with this script:

In ```feedback.sh```, replace
```bash
# first read a list of students that are assigned fixed ta's (group_$name); the format of this file
# can be the same as the userlist-file, but only the first column matters
#for ta in "${!email[@]}"
#do
#    listfile="$MYDIR/group_${ta}"
#    test -e "$listfile" || continue
#    echo "Distributing workload to $ta"
#    mkdir -p "$ta"
#    while read stud trailing; do
#	[ -e "$stud" ] && mv "$stud" "$ta"
#    done < "$listfile"
#done
```
with
```
python ./ta_groupify.py
```
and remove
```bash
echo Randomly distributing workload 
"$MYDIR"/hak3.sh "${!email[@]}" 
```
