import pandas as pd
import datetime
import argparse
import sys
import os



# Import other py files
import retrieveDataframe
import cleanupDataframe
import splitTrainingTest
import trainModel


taskTimes = {}
process = "start"


parser = argparse.ArgumentParser(description = "This script runs our database of historical call records to train our ML models on predicting scam calls.", formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('--model', metavar='ML Model', required = False,
                    help='''
                    'all': run both Random Forests and Decision Trees
                    'rf': run Random Forests
                    'dt': run Decision Trees
                    ''')
args = parser.parse_args()


### READ DATA ###
if process == "start":
  print('')
  print('')
  print(" > Retrieving data from database...")
  start_time = datetime.datetime.now()
  directory_str = 'data/calls.db'
#-----------USE THIS IF ALL ELSE FAILS------------------------
#  directory_str = r"../data/calls.db"
  df = retrieveDataframe.connectToDataBase(directory_str)
  taskTimes["Train-Test Split"] = (datetime.datetime.now() - start_time).total_seconds()
  
  
  
  process = "clean"

### CLEAN AND PREPARE DATA ###
if process == "clean":
  print('')
  print('')
  print(" > Commencing data cleaning and preparation...")
  start_time = datetime.datetime.now()
  cleaned_df = cleanupDataframe.commenceCleanup(df)
  taskTimes["Clean Data"] = (datetime.datetime.now() - start_time).total_seconds()
  
  
  process = "split"

### TRAINING TEST SPLIT ###
if process == "split":
  print('')
  print('')
  print(" > Splitting training and test data...")
  start_time = datetime.datetime.now()
  train, test  = splitTrainingTest.splitData(cleaned_df)

  print('')

  taskTimes["Train-Test Split"] = (datetime.datetime.now() - start_time).total_seconds()
  process = "predict"

### TRAIN & PREDICT ### 
if process == "predict":
  print('')
  print('')
  print(" > Commencing training and prediction...")
  start_time = datetime.datetime.now()

  X_train = train
  X_test = test
  

  print(" > Training and test data read")

  Y_train = X_train['Scam Call']
  X_train = X_train.drop('Scam Call', axis=1)
  X_test = X_test.drop('Scam Call', axis=1).copy()
  

  accuracy, prediction, precision, recall = trainModel.trainAndPredict(X_train, X_test, Y_train, "all")
  
  
  acc_results = pd.DataFrame({
    'Model': accuracy.keys(),
    'Accuracy': accuracy.values()
  })

  acc_results = acc_results.sort_values(by="Accuracy", ascending = False)
  acc_results = acc_results.set_index("Accuracy")

  print('')
  print("Accuracy: ")
  print(acc_results)
  print('')

  pred_results = pd.DataFrame({
    'Model': prediction.keys(),
    'Prediction': prediction.values()
  })

  pred_results = pred_results.set_index("Prediction")

  print('')
  print("Prediction: ")
  print(pred_results)
  print('')

  prec_results = pd.DataFrame({
    'Model': precision.keys(),
    'Precision': precision.values()
  })

  prec_results = prec_results.set_index("Precision")

  print('')
  print("Precision: ")
  print(prec_results)
  print('')

  rec_results = pd.DataFrame({
    'Model': recall.keys(),
    'Recall': recall.values()
  })

  rec_results = rec_results.set_index("Recall")

  print('')
  print("Recall: ")
  print(rec_results)
  print('')

  taskTimes["Train and Predict"] = (datetime.datetime.now() - start_time).total_seconds()

totalTime = sum(taskTimes.values())
runTime_df = pd.DataFrame()
runTime_df["Task"] = taskTimes.keys()

if totalTime != 0:
  runTime_df["Percent of Pipeline"] = [ i / totalTime * 100 for i in taskTimes.values()]

  print('')
  print('')
  print("##########")
  print(runTime_df)
  print("##########")
  print('')
  print(' > Complete, great success!')




