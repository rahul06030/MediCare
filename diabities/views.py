from django.shortcuts import render,redirect
from django.http import JsonResponse
import pandas as pd
from .models import Diabitic
from django.contrib import messages
from django.contrib.auth.decorators import login_required

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

def homepage(request):
    return render(request, 'diabities/home.html')


@login_required(login_url='/login/')
def trainD(request):
    # Load dataset
    df=pd.read_csv(r'diabetes.csv')
    # Split into training data and test data
    X=df.drop(columns=['Outcome','DiabetesPedigreeFunction'])
    y=df['Outcome']
    train_X,test_X,train_y,test_y=train_test_split(X,y,test_size=0.2)

    model = KNeighborsClassifier(n_neighbors = 2)
    model.fit(train_X, train_y)

    # predictions = model.predict(X_test)

    pd.to_pickle(model,r'diabities.pickle')
    messages.success(request, f"Model Trained ")
    return redirect ("/")

@login_required(login_url='/login/')
def predictD(request):
    data={}
    if request.method == 'POST':
        try:
            Patient_ID = int(request.POST.get('Patient_ID'))
            Age = int(request.POST.get('Age'))
            Gender = int(request.POST.get('Gender'))
            Blood_Pressure = int(request.POST.get('Blood_Pressure'))
            Pregnancies = int(request.POST.get('Pregnancies'))
            Glucose =int( request.POST.get('Glucose'))
            Insulin = int(request.POST.get('Insulin'))
            BMI = float(request.POST.get('BMI'))
            SkinThickness = int(request.POST.get('SkinThickness'))
            model = pd.read_pickle(r"diabities.pickle")
            result = model.predict([[  Pregnancies  ,Glucose,   Blood_Pressure, SkinThickness, Insulin, BMI, Age]])
            result = result[0]

            pa=Diabitic(Patient_ID=Patient_ID, Age=Age, Gender=Gender,Glucose=Glucose, SkinThickness=SkinThickness ,
                                    Insulin=Insulin , BMI=BMI, Blood_Pressure=Blood_Pressure, Pregnancies=Pregnancies , Result=result)
            pa.save()
            if(result==0):
                messages.success(request, f"You are not Diabetic ")
            else:
                messages.error(request, f"You are Diabetic ")
            data={'Patient_ID':Patient_ID, 'Age':Age, 'Gender':Gender,'Glucose':Glucose, 'SkinThickness':SkinThickness ,'Insulin':Insulin , 'BMI':BMI,
                                       'Blood_Pressure':Blood_Pressure, 'Pregnancies':Pregnancies , 'Result':result}
            return render(request, 'diabities/result.html', {"data":data})
        except Exception as e:
            print(e)
            messages.error(request, f"Invalid Entry")
            return render(request, 'diabities/predict.html')
    return render(request, 'diabities/predict.html')

@login_required(login_url='/login/')
def view_results(request):
    # Submit prediction and show all
    data = {"dataset": Diabitic.objects.all()}
    return render(request, "diabities/database.html", data)



