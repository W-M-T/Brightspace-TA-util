# How to use this script to distribute work by group:

- Enter the names and mail addresses of the TA's to distribute over in ```ta_groupify.py```.
- Patch ```verdeel.sh``` as described below.
- Ensure there are group_[ta_name] files (see below as well)
- Run the bash scripts as you would normally.

# How to patch https://github.com/squell/bb-scripts with this distribution script:

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
# How to obtain the group_[ta_name] files:

If you're in luck you can get the enrollment info for each student using the Export Grades functionality with a field like "Group Enrollment". In this case you only need to parse the csv for this info. This is not the use case that this repo provides however.

This repo assumes that this field does not exist in the grade exporter (for some courses this seems to be the case, weirdly enough?).

To obtain ta group files using this utility, you select ```Enroll Users``` under the desired group category under ```Administration``` -> ```Groups```, set the display size to 200, and download the html pages to the same folder as ```scrapegroups.py```. It's an ugly solution, but it works with a lack of a better way to access this data such as discussed earlier.

Currently it uses the regex ```RE_CUSTOM_GROUP_NAME``` to translate a group to the first name of the ta. You will need to write a new regex if your course uses a different naming scheme. The easiest way to implement this translation is to just write a lookup table.
