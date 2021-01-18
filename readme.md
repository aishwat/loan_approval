Loan Approval Model
-----
Installation 
* It uses [libpostal](https://github.com/openvenues/libpostal) which will need seperate installation 
* for mac follow 
```
brew install curl autoconf automake libtool pkg-config
git clone https://github.com/openvenues/libpostal
cd libpostal
./bootstrap.sh
./configure --datadir=[...some dir with a few GB of space...]
make -j4
sudo make install```
```
* [Or] uncomment `# return fuzz.ratio(a1.lower(), a2.lower())` in `utils.py` to skip installing libpostal, also remove `postal` from `requirements.txt`

-----

Directory Structure

* server.py - main file, brings up server at 8000
* models.py - request, response classes
* utils.py - helper functions
* test_server.py - run `pytest` in terminal, functional test
* load.py - hits server with parallel requests given at `future = asyncio.ensure_future(run(2000))`. It has a `run_seq` function to get average response time if hit sequentially. Bottom average_response times are mentioned in comment
* load_test.js - NodeJs load testing. Surprisingly! higher the concurrency, it gave lower average response time
 
* _logging is commented out_
