from collections import defaultdict
import pandas as pd

from surprise import Reader, Dataset, SVD


def get_top_n(predictions, n=10):
    """Return the top-N recommendation for each user from a set of predictions.

    Args:
        predictions(list of Prediction objects): The list of predictions, as
            returned by the test method of an algorithm.
        n(int): The number of recommendation to output for each user. Default
            is 10.

    Returns:
    A dict where keys are user (raw) ids and values are lists of tuples:
        [(raw item id, rating estimation), ...] of size n.
    """

    # First map the predictions to each user.
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, est))

    # Then sort the predictions for each user and retrieve the k highest ones.
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]

    return top_n


ratings = pd.read_csv("./dataset/ratings.csv", sep=",")
reader = Reader(rating_scale=(0.5, 5.0))

data = Dataset.load_from_df(ratings[["userId", "movieId", "rating"]], reader)
trainset = data.build_full_trainset()

# First train an SVD algorithm on the movielens dataset.
algo = SVD()
algo.fit(trainset)

# Than predict ratings for all pairs (u, i) that are NOT in the training set.
testset = trainset.build_anti_testset()
predictions = algo.test(testset)

top_n = get_top_n(predictions=predictions, n=10)

# Print the recommended items for each user
# for uid, user_ratings in top_n.items():
#     if uid == 1:
#         print(uid, [iid for (iid, _) in user_ratings])

# Predict the rating of the specific user's item
uid = 1
iid = 318
pred = algo.predict(uid, iid)
print(pred)

uid = 1
iid = 2300
pred = algo.predict(uid, iid)
print(pred)

uid = 1
iid = 922
pred = algo.predict(uid, iid)
print(pred)
