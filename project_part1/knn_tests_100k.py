import pandas as pd
from surprise import prediction_algorithms as pa
from surprise import Dataset, Reader, GridSearch
from surprise import evaluate, print_perf
import datetime

data = pd.read_csv('./ml-100k/data.csv')
df = pd.DataFrame(data)
df.drop('timestamp', axis=1, inplace=True)

reader = Reader(rating_scale=(1, 5))
dataset = Dataset.load_from_df(df[['userId', 'movieId', 'rating']], reader)
dataset.split(n_folds=5)


similarities = ['cosine', 'msd', 'pearson', 'pearson_baseline']
user_based = [True, False]

start_time = ('Timestamp: {:%Y-%b-%d %H:%M:%S}'.format(datetime.datetime.now()))
sim_options = {'name': similarities, 'user_based': user_based}
param_grid = {'k': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100], 'min_k': [5], 'sim_options': sim_options}
grid_search = GridSearch(pa.KNNBaseline, param_grid=param_grid, measures=['MAE', 'RMSE', 'FCP'])
grid_search.evaluate(dataset)
results_df = pd.DataFrame.from_dict(grid_search.cv_results)
results_df.to_csv("100k_KNNBaseline_Results.csv")
end_time = ('Timestamp: {:%Y-%b-%d %H:%M:%S}'.format(datetime.datetime.now()))
print "Start Time: ", start_time
print "End Time: ", end_time