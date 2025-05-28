## LAB 3

### Data loader on C++

#### Meant to download needed data from kaggle using C++ for further work. Used libraries:
1. nlohmann-json - to parse json files, like config for downloading data from kaggle.json
2. CURL - to fetch data from kaggle and prepare it in the type of csv for further work

#### Loading raw data
1. **data_loader.cpp** uses kaggle.json configs and dataset_paths.txt, as credentials and source urls for raw data downloading.
2. data then is saved in the folder **data_raw** before being used after