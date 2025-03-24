# Bitwarden Deduplication

This script reads a bitwarden json file. You can look online on how to export a json file from bitwarden.

This script:
- Deletes duplicate folders
  - Folders that have the same name, the first one will be chosen, and relevant items will be mapped to this folder
- Deletes duplicate entries
  - If an entry has the same password, username, and uri as another entry, the duplicated one is ignored
- Alerts on entries that don't have a pw, username, or url
  - Does not do anything to filter these, just alerts on them
- Alerts on duplicate passwords

This will output a "_verified".json file that you can then import into bitwarden. You will need to delete your current
bitwarden entries before import, otherwise you will just have more duplicates.
