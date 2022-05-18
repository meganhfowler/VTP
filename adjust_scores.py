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


def main(date, infile, outfile):
    scores = pd.read_csv('scores/2022_04_13.csv')
    print(scores)
    latest_scores = pd.read_csv(infile).sort_values(by=['score'], ascending = False)
    adjusted_scores = convert_scores(latest_scores)
    adjusted_scores.to_csv(outfile)


    create_dataframe_image(adjusted_scores, 'tables/' + date + '.png')

if __name__ == '__main__':
    date = str(sys.argv[1])
    infile = 'scores/' + date + '.csv'
    outfile = 'adjusted-scores/' + date + '_adjusted.csv'
    main(date, infile, outfile)
