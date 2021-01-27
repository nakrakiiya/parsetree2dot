Convert the parse tree to Graphviz's dot file.

# Requirements

On Ubuntu, run the following.

```
sudo apt install graphviz
```

# Run the script

Parse `example.py` and convert the parse tree to a svg graph.

```
python parsetree2dot.py example.py
dot -Tsvg -O example.py.dot
```
