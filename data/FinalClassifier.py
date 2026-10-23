# import libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import accuracy_score, mean_absolute_error, mean_squared_error, r2_score, confusion_matrix
import joblib

from views import preprocess


def create_model():

    # load dataframe
    df = pd.read_csv('restaurants.csv')
    df.head()
    msg=""
    acc=0
    if(preprocess()=="valid"):
        # remove null value rows
        df = df.dropna()

        # drop features that inhibit model building
        df = df.drop('Restaurant ID', axis=1)
        df = df.drop('Restaurant Name', axis=1)
        df = df.drop('Country Code', axis=1)
        df = df.drop('City', axis=1)
        df = df.drop('Address', axis=1)
        df = df.drop('Locality', axis=1)
        df = df.drop('Locality Verbose', axis=1)
        df = df.drop('Longitude', axis=1)
        df = df.drop('Latitude', axis=1)
        df = df.drop('Cuisines', axis=1)
        df = df.drop('Currency', axis=1)
        #df.to_csv('../PreProcessed.csv', index=False)
        # encode the yes-no labels of categorical features into binary (1 for yes and 0 for no)
        from sklearn.preprocessing import LabelEncoder
        le = LabelEncoder()
        df['Has Table booking'] = le.fit_transform(df['Has Table booking'])
        df['Has Online delivery'] = le.fit_transform(df['Has Online delivery'])
        df['Is delivering now'] = le.fit_transform(df['Is delivering now'])
        df['Switch to order menu'] = le.fit_transform(df['Switch to order menu'])
        df['Rating color'] = le.fit_transform(df['Rating color'])
        df['Rating text'] = le.fit_transform(df['Rating text'])

        #df.to_csv('../Processed.csv', index=False)
        x = df.drop('Aggregate rating', axis=1)
        y = df['Aggregate rating']
        #x.to_csv('../XTrain.csv', index=False)
        # data splitting
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=250)
        x_train.head()
        y_train.head()
        #x_test.to_csv('../XTest.csv', index=False)
        # training by decision tree regressor algorithm
        dtree = DecisionTreeRegressor()
        dtree.fit(x_train, y_train)
        dtree_pred = dtree.predict(x_test)
        dtree_fullpred=dtree.predict(x_train)


        dt_xtest = pd.DataFrame(x_test)
        dt_ypred = pd.DataFrame(dtree_pred,columns=['predicted Rating'])

        final_merge=dt_xtest.merge(dt_ypred, left_index=True, right_index=True)
        final_merge.to_csv('final_predictions.csv', index=False)
        # evaluating performance metrics of decision tree


        dtree_mae = mean_absolute_error(y_test, dtree_pred)
        dtree_mse = mean_squared_error(y_test, dtree_pred)
        dtree_r2 = r2_score(y_test, dtree_pred)
        print(f"MAE of the decision tree model is: {dtree_mae:.2f}")
        print(f"MSE of the decision tree model is: {dtree_mse:.2f}")
        print(f"R2 score of the decision tree model is: {dtree_r2:.2f}")
        acc=dtree_r2*100
        joblib.dump(dtree, 'Restaurant_DT.pkl')
        msg = "Model created successfully"
    else:
        msg="Model could not be created as dataset got corrupted. Please reload the dataset"
        acc=0

    return msg, acc

#create_model()
