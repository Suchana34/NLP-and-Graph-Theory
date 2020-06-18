import pandas as pd
from sklearn import metrics
data  = pd.read_csv('abc.csv')

quitmatrix = np.matrix([vectorfun.generate_vector(v) for k,v in data.column_name.iterkv()])
dmat = metrics.pairwise_distances(quitmatrix, metric = 'cosine')


