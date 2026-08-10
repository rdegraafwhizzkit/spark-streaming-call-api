# Prepare
Needs Java JDK 1.8
```
deactivate > /dev/null 2>&1 || :
rm -rf .venv requirements.txt

python3 -m venv .venv
. .venv/bin/activate
pip install --upgrade -r dev-requirements.txt
pip-compile requirements.in
pip install --upgrade -r requirements.txt
```

# Start socket server
Mileage may vary on Windows/WSL here
```
nc -v -k -l 9999
```

# Start Spark Structured Streaming Job
On Windows with Git Bash, set some extra variables
```
export HADOOP_HOME=/c/Users/..FIX-ME../hadoop/
export PATH=${PATH}:${HADOOP_HOME}/bin
```
then
```
python main.py
```
and type url's in the socket server like 
```
https://ip.me
https://ip.me
https://api.ipify.org?format=json
```
and the result will be:
```
:: loading settings :: 
... SNIP ...
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
-------------------------------------------                                     
Batch: 0
-------------------------------------------
+--------+-----+
|response|count|
+--------+-----+
+--------+-----+

-------------------------------------------                                     
Batch: 1
-------------------------------------------
+-------------+-----+
|     response|count|
+-------------+-----+
|11.222.33.444|    1|
+-------------+-----+

-------------------------------------------                                     
Batch: 2
-------------------------------------------
+-------------+-----+
|     response|count|
+-------------+-----+
|11.222.33.444|    2|
+-------------+-----+

-------------------------------------------                                     
Batch: 3
-------------------------------------------
+--------------------+-----+
|            response|count|
+--------------------+-----+
|{"ip":"11.222.33....|    1|
|       11.222.33.444|    2|
+--------------------+-----+
```