# Web service to convert Finnish bank's account statements to FIN-KTL data

Viiteaineistomuunnin is a Flask-powered web service to convert payment events
from various sources to a FIN-KTL compatible reference payment file for use
with Kilta / Kuksa and other data consumers.

## Compatible source files

* Osuuspankki event CSV file
* Nordea event listing CSV file
* Kilta / Kuksa invoice Excel export converted to CSV

## Installation

* Create a virtual env using Python 3
```virtualenv -p python3 env/
```
* Jump into the virtual env
```source env/bin/activate
```
* Install dependencies:
```pip install -r requirements.txt
```
* Run the dev server:
```python run.py```
