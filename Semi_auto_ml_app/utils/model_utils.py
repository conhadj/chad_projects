from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.svm import SVC, SVR
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, GradientBoostingRegressor
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

def get_models(output_type_after_encoding, is_ordinal):
    models = []
    removed_models = []

    if output_type_after_encoding in ['Numerical Binary', 'Numerical Multiclass']:
        models = [
            ('Logistic Regression', LogisticRegression()),
            ('K-Nearest Neighbors', KNeighborsClassifier()),
            ('Support Vector Machine', SVC()),
            ('Decision Tree', DecisionTreeClassifier()),
            ('Gaussian Naive Bayes', GaussianNB()),
            ('Random Forest', RandomForestClassifier())
        ]
        if output_type_after_encoding == 'Numerical Binary':
            removed_models = [
                ('Linear Discriminant Analysis', 'Not suitable for binary output')
            ]
        else:
            models.append(('Linear Discriminant Analysis', LinearDiscriminantAnalysis()))
    elif output_type_after_encoding == 'Numerical Continuous':
        models = [
            ('Linear Regression', LinearRegression()),
            ('Support Vector Regression', SVR()),
            ('Decision Tree Regression', DecisionTreeRegressor()),
            ('Random Forest Regression', RandomForestRegressor()),
            ('Gradient Boosting Regression', GradientBoostingRegressor()),
            ('K-Nearest Neighbors Regression', KNeighborsRegressor())
        ]
    elif output_type_after_encoding == 'Mixed' and is_ordinal == "Yes":
        models = [
            ('Logistic Regression', LogisticRegression()),
            ('K-Nearest Neighbors', KNeighborsClassifier()),
            ('Support Vector Machine', SVC()),
            ('Decision Tree', DecisionTreeClassifier()),
            ('Gaussian Naive Bayes', GaussianNB()),
            ('Random Forest', RandomForestClassifier()),
            ('Linear Regression', LinearRegression()),
            ('Support Vector Regression', SVR()),
            ('Decision Tree Regression', DecisionTreeRegressor()),
            ('Random Forest Regression', RandomForestRegressor())
        ]
    elif output_type_after_encoding == 'Mixed' and is_ordinal == "No":
        models = [
            ('Logistic Regression', LogisticRegression()),
            ('K-Nearest Neighbors', KNeighborsClassifier()),
            ('Support Vector Machine', SVC()),
            ('Decision Tree', DecisionTreeClassifier()),
            ('Gaussian Naive Bayes', GaussianNB()),
            ('Random Forest', RandomForestClassifier())
        ]

    return models, removed_models