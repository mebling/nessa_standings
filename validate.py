from models import Rating, Race, db
from glicko_rating import GlickoRating
import pandas as pd
from app import app
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
from sklearn import metrics


def validate():
    races = db.session.query(Race).order_by(Race.date)
    ratings = db.session.query(Rating).order_by(Rating.date)
    ratings_data = defaultdict(dict)
    for rating in ratings:
        ratings_data[rating.date][rating.school_id] = rating
    results = []
    y_true = []
    probs = []
    for race in races:
        school_rating = ratings_data[race.date][race.school_id]
        opponent_rating = ratings_data[race.date][race.opponent_id]

        if race.school_score > race.opponent_score:
            winner = race.school_id
        elif race.opponent_score > race.school_score:
            winner = race.opponent_id
        else:
            continue

        opponent_glicko_rating = GlickoRating(rating=opponent_rating.rating, rd=opponent_rating.rd)
        school_glicko_rating = GlickoRating(rating=school_rating.rating, rd=school_rating.rd)

        opponent_win_confidence = opponent_glicko_rating._expected_score(school_glicko_rating)
        school_win_confidence = 1. - opponent_win_confidence

        if opponent_win_confidence == school_win_confidence:
            continue

        if school_win_confidence > opponent_win_confidence:
            correct = 1 if winner == race.school_id else 0
        else:
            correct = 1 if winner == race.opponent_id else 0

        if winner == race.school_id:
            y_true.append(1)
            confidence = school_win_confidence
        else:
            y_true.append(0)
            confidence = opponent_win_confidence
        probs.append(confidence)

        results.append({'confidence': confidence, 'date': race.date, 'race_id': race.id })
    dataframe = pd.DataFrame(results)
    dataframe.to_csv("Results.csv")

    num_correct = len([confidence for confidence in probs if confidence > .5])
    print("ACCURACY: {}".format(num_correct/len(probs)))

    fpr, tpr, threshold = metrics.roc_curve(y_true, probs)
    roc_auc = metrics.auc(fpr, tpr)

    plt.title('Receiver Operating Characteristic')
    plt.plot(fpr, tpr, 'b', label = 'AUC = %0.2f' % roc_auc)
    plt.legend(loc = 'lower right')
    plt.plot([0, 1], [0, 1],'r--')
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    plt.show()


if __name__ == '__main__':
    with app.app_context():
        validate()
