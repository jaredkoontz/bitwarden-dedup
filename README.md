# Bitwarden Deduplication

This script reads a bitwarden json file. You can look online on how to export a json file from bitwarden. After
reading in the file, this script will:

- Delete duplicate folders
  - Folders that have the same name, the first one will be chosen, and relevant items will be mapped to this folder
- Delete duplicate entries
  - A duplicate entry is needs to have the same *password, username, and uri*
    - the duplicated one is ignored
- Alerts on entries that don't have a pw, username, or url
  - Does not do anything to filter these, just alerts on them
- Alerts on duplicate passwords

After completion, you will have a "_verified".json file that you can then import into bitwarden.

You will need to delete your current bitwarden entries before import, otherwise you will just have more duplicates.
