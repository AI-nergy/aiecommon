# FileSystem module - file abstraction layer

The FileSystem module provides an abstraction layer for accesing data files, runtime files, and files downloaded from Google Drive or other services.

## Quick examples

### Load data files

```python
from aiecommon.FileSystem import LocalDataFiles

# load JSON from "modules/aiesolar/optimizer/data/TechnicalData.json" in root of the currently running project
technical_data = LocalDataFiles.load_json("modules/aiesolar/optimizer/data/TechnicalData.json")
print(technical_data)
```

```python
from aiecommon.FileSystem import LocalDataFiles

# load JSON from "data/translations.json" in aiecommon package
translations = LocalDataFiles.load_json("data/translations.json", "aiecommon")
print(translations)
```

### Working with runtime files

```python
from aiecommon.FileSystem import LocalRuntimeFiles

# Cached files
# save JSON to "runtimedata/cache/local_runtime_files/temp_results.json" in root of the currently running project
results = {"exampledata1": "Example value 1"}
LocalRuntimeFiles.save_json("temp_results1.json", results)

# Cached files
# load JSON from "runtimedata/cache/local_runtime_files/temp_results.json" in root of the currently running project
loadedResults = LocalRuntimeFiles.load_json("temp_results1.json")
print(loadedResults)
```

```python
import json
from aiecommon.FileSystem import LocalRuntimeFiles

results = {"exampledata2": "Example value 2"}

# Permanent storage
# open "runtimedata/storage/local_runtime_files/temp_results2.json" for writing in root of the currently running project
file = LocalRuntimeFiles.open_file("temp_results2.json", "w", usePermanentStorage = True)
json.dump(results, file)
file.close()

# Permanent storage
# open "runtimedata/storage/local_runtime_files/temp_results2.json" for reding in root of the currently running project
file = LocalRuntimeFiles.open_file("temp_results2.json", "r", usePermanentStorage = True)
loadedResults = json.load(file)
print(loadedResults)
file.close()
```
### Open file from Google drive

```python
from aiecommon.FileSystem import GoogleDrive

# Cached files
# download file with id "1CWapGOUri7uwvmyARDaVEUo1MEEoarcj" from "GoogleDrive,
# save it to "runtimefiles/cache/google_drive/1CWapGOUri7uwvmyARDaVEUo1MEEoarcj"
file = GoogleDrive.open_file("1CWapGOUri7uwvmyARDaVEUo1MEEoarcj")
file.close()

# Permanent storage
# download file with id "1CWapGOUri7uwvmyARDaVEUo1MEEoarcj" from "GoogleDrive,
# save it to "runtimefiles/storgae/google_drive/1CWapGOUri7uwvmyARDaVEUo1MEEoarcj"
file = GoogleDrive.open_file("1CWapGOUri7uwvmyARDaVEUo1MEEoarcj", usePermanentStorage = True)
file.close()
```


## Functions

## FileSystems

## FUll examples


