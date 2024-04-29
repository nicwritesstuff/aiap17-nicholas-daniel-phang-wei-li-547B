from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import precision_score, recall_score

def trainAndPredict(X_train, X_test, Y_train, type="all"):

  accuracy = {}
  prediction = {}
  precision = {}
  recall = {}


  def runRandomForest():
    randomForest = RandomForestClassifier(n_estimators=75)
    randomForest.fit(X_train, Y_train)
    prediction["Random Forests"] = randomForest.predict(X_test)
    accuracy["Random Forests"] = round(randomForest.score(X_train, Y_train) * 100, 2)
    precision["Random Forests"] = round(precision_score(Y_train, randomForest.predict(X_train)) * 100, 2)
    recall["Random Forests"] = round(recall_score(Y_train,  randomForest.predict(X_train)) * 100, 2)
  
  def runDecisionTree():
    tree = DecisionTreeClassifier() 
    tree.fit(X_train, Y_train)
    prediction["Decision Trees"] = tree.predict(X_test)  
    accuracy["Decision Trees"] = round(tree.score(X_train, Y_train) * 100, 2)
    precision["Decision Trees"] = round(precision_score(Y_train, tree.predict(X_train)) * 100, 2)
    recall["Decision Trees"] = round(recall_score(Y_train, tree.predict(X_train)) * 100, 2)

  if type == "rf": runRandomForest()
  if type == "dt": runDecisionTree()

  if type == "all":
    runRandomForest()
    runDecisionTree()

  return accuracy, prediction, precision, recall
