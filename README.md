# decision-tree-algorithms
Implementation of some decision tree algorithms in Python.

## Requirements:

Python 3+

All dependencies defined in requirements.txt.
Dependencies can be installed by:

```
pip install -r requirements.txt
```

## ID3 Algorithm:

ID3 (Iterative Dichotomiser 3) is a classification algorithm, proposed by Ross Quinlan in 1986, that follows a greedy approach of building a decision tree 
by selecting the best attribute that yields the maximum Information Gain. Only symbolic variables are processed, 
numerical ones must be discretized to be considered. 

Run the ID3/main.py file with the following arguments:

```
python ID3/main.py [data file] [target variable] [instance to classify (optional)]
```
