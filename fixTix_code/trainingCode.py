
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cross_validation import train_test_split
from sklearn import preprocessing
from sklearn.svm import LinearSVC, SVC 
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
import sys
x_train = None
x_test = None
y_train = None
y_test = None
x = None
y = None


def readFile(fileName):
    df = pd.read_csv(fileName, header = 0,sep = ',')
    df[['labels','bookingStatus','status1Day','status2Days','status1Week','status1Month','class_SL','class_3A','Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']]
    global x_train ,  x_test, y_train, y_test, x, y
    y = df.ix[:,0]
    x = df.ix[:,1:]
    x_train ,  x_test,  y_train, y_test = train_test_split(x,y,test_size = 0.2)
    x_train = preprocessing.scale(x_train)
    x_test = preprocessing.scale(x_test)
    
#def linearSVM(accuList,maxiter):
 #   xlinSVM = np.arange(maxiter-1)
  #  for i in range (1,maxiter-1):
   #     svm = LinearSVC(C = i)  
    #    svm.fit(x_train, y_train)
     #   pred = svm.score(x_test, y_test)
      #  accuList.append(pred)
    #return (xlinSVM,accuList)


def linearSVMC(accuList,Slack):
    xlinSVM = np.arange(Slack-1)
    for i in range (1,Slack):
        svm = LinearSVC(C = i)  
        svm.fit(x_train, y_train)
        pred = svm.score(x_test, y_test)
        accuList.append(pred)
        print (i,pred)
    return (xlinSVM,accuList)

def naiveBayes():
    gnb = GaussianNB()
    gnb.fit(x_train, y_train)
    pred = gnb.score(x_test, y_test)
    return (pred) 
    
def randomForest(rfAccuList,numEst):
    xRf = np.arange(numEst-1)
    for i in range (1,numEst):
        rf = RandomForestClassifier(n_estimators=i)
        rf.fit(x_train, y_train)
        pred = rf.score(x_test, y_test)
        rfAccuList.append(pred)
    return(xRf, rfAccuList)


readFile(sys.argv[1])
#iterations =int(sys.argv[2])

slack =int(sys.argv[2])
#estimators = int(sys.argv[3])

a = []
y = linearSVMC(a,slack)

#z = randomForest(b,estimators)
plt.plot(y[0],y[1])
plt.xlabel("Slack Variable")
plt.ylabel("Accuracy")
plt.title("Convergence for Soft to Hard SVM")
#plt.plot(z[0],z[1])
plt.show()
num_iter = 100
linsvm =0 
nvb =0
rndfrst = 0

#print(naiveBayes())
#for i in range (0,num_iter):
#    linsvm += linearSVM()
   # nvb += naiveBayes()
    #rndfrst += randomForest()
    #x_train ,  x_test,  y_train, y_test = train_test_split(x,y,test_size = 0.2)
    #x_train = preprocessing.scale(x_train)
    #x_test = preprocessing.scale(x_test)

print ("Linear SVM : ", linsvm/num_iter)
print ("naive Bayes : ", nvb/num_iter) 
print ("randomForest : ",rndfrst/num_iter)
