.PHONY: setup run data

setup:
\tpip install -r requirements.txt

data:
\tpython data_gen.py

run:
\tstreamlit run app.py
