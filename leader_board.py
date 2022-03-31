import pandas as pd
import dataframe_image as dfi
import sys

MAX_SCORE = 35


def convert_scores(scores):
    unique_scores = sorted(set(scores['score']), reverse = True)
    scores['base_score'] = scores['score'].apply(lambda x: MAX_SCORE - unique_scores.index(x))
    scores['bonus_score'] = scores['score'].apply(lambda x: scores.shape[0] - scores[scores['score'] >= x].shape[0])
    scores['adjusted_score'] = scores['base_score'] + scores['bonus_score']

    return scores


def create_dataframe_image(scores, outfile):
    print_scores = pd.DataFrame({'Team': scores['team'], 'Score': scores['adjusted_score']}).set_index('Team')
    dfi.export(print_scores, outfile, table_conversion = 'matplotlib')


def main(infile, outfile):
    latest_scores = pd.read_csv(infile).sort_values(by=['score'], ascending = False)
    adjusted_scores = convert_scores(latest_scores)
    adjusted_scores.to_csv(outfile)


    create_dataframe_image(adjusted_scores, "tables/2020_03_30.png")

if __name__ == '__main__':
    infile = sys.argv[1]
    outfile = 'adjusted-scores/2020_03_30_adjusted.csv'
    main(infile, outfile)
