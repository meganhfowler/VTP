import pandas as pd
import numpy as np

# Assign the base score to each team that week
# 35 for winner, 34 second, ...
# In the case of a draw, the two teams get the same base score
# Ex. If second and third place draw,
# 1st will get 35 pts, 2nd 34 pts, 3rd 34 pts, 4th 33 pts, etc

MAX_SCORE = 35

def get_unique_weekly_scores(weekly_scores):
    unique_scores = pd.Series(sorted(set(weekly_scores), reverse = True)).dropna()
    return unique_scores.values

def get_base_scores(weekly_scores):

    # get the unique scores from the week
    unique_scores = get_unique_weekly_scores(weekly_scores)

    # get the correct number of base scores for the week
    n = get_unique_weekly_scores(weekly_scores).shape[0]
    base_scores = np.arange(MAX_SCORE, MAX_SCORE-n, -1)

    # Create dictionary of scores to base score
    scores_dict = dict(zip(unique_scores, base_scores))
    scores_dict.update({0.0: 0})

    weekly_scores = weekly_scores.fillna(0)

    return weekly_scores.apply(lambda x: scores_dict[x])



# Assign the bonus score to each team that week
# Bonus = Number of teams you beat
# In the case of a draw, you did not beat that team

def get_bonus_scores(weekly_scores):
    num_teams = weekly_scores[weekly_scores > 0].count()
    weekly_scores = weekly_scores.apply(lambda x: weekly_scores[weekly_scores < x].count())
    return weekly_scores


# Take a column of weekly scores and convert them
def adjust_weekly_scores(weekly_scores):
    adjusted_scores = get_base_scores(weekly_scores) + get_bonus_scores(weekly_scores)
    return adjusted_scores



# Adjust the scores of all the columns
def adjust_all_scores(scores_df):
    for weekly_score in scores_df:
        weekly_scores = scores_df[weekly_score]
        scores_df[weekly_score] = adjust_weekly_scores(weekly_scores)
    return scores_df


def main():
    scores = pd.read_csv('raw_scores.csv')
    scores = scores.dropna(axis=1, how='all')
    scores = scores.set_index('team')

    scores = adjust_all_scores(scores)
    scores['Total'] = scores.sum(axis = 1)
    scores.sort_values(by='Total', ascending = False, inplace = True)

    scores.to_csv('adjusted_scores.csv')

if __name__ == '__main__':
    main()
