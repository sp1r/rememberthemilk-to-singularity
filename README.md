# Remember the Milk to Singularity Converter

This script converts Tasks exported in JSON format from Remember The Milk app to Singularity importable CSV file.

WARNING: Conversion is lossy! (See below)

### Notes
1. All data is imported in a new Project "Remember the Milk".
2. Remember The Milk "List" is converted to Singularity "Project".
3. Completed Tasks are ignored by default, this can be changed by commandline argument `--preserve-completed`.
4. Deleted tasks are ignored.
5. Notes (Task comments) are preserved in Task description.
6. Task repeat configuration is lost (unfortunately). String with repeat info is added to task description.
7. Sub-tasks is imported as nested Tasks.
8. Tags are imported as additional description info.
9. (sorry) I was lazy and didn't preserve priorities.
10. Double quotes in names and descriptions are replaced with single quotes (to ensure correct multi-line parsing of CSV)
11. Smart Lists are lost.


### Links
1. Remember the Milk: https://www.rememberthemilk.com/
2. Singularity: https://singularity-app.com/
3. How to export data from Remember the Milk: https://www.rememberthemilk.com/help/answer/accounts-backup
4. Import format for Singularity: https://singularity-app.com/wiki/import-iz-csv/
