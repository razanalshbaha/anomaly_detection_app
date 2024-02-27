template_string= """
You are a data analyst and you are given the columns names for a certain Logs Dataset. Read and understand the dataset columns. \
Do feature selection to determine which columns in the dataset should be used for anomaly detection. \
The Dataset columns are shown below delimited by triple brackets: \
columns: {columns} \
The output format should be ONLY A LIST like this:  ['feature1', 'ferature2', 'feature3']
"""