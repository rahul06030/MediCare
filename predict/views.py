from django.shortcuts import render,redirect
from django.http import JsonResponse
import pandas as pd
from .models import PredResults
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from pandas import read_csv
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

def homepage(request):
    return render(request, 'home.html')

    
@login_required(login_url='/login/')
def predict(request):
    return render(request, 'predict.html')


@login_required(login_url='/login/')
def train(request):
    # Load dataset
    df = pd.read_csv(r"dataset.csv")
    # Split into training data and test data
    X = df[['Patient_Age','Patient_Gender','Patient_Blood_Pressure','Patient_Heartrate']]
    y = df['Heart_Disease']
    # Create training and testing vars, It’s usually around 80/20 or 70/30.
    X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=0.20, random_state=1)
    # Now we’ll fit the model on the training data
    model = RandomForestClassifier()
    model.fit(X_train, Y_train)
    # Make predictions on validation dataset
    predictions = model.predict(X_test)
    # Pickle model
    pd.to_pickle(model,r'heart.pickle')
    messages.success(request, f"Model Trained")
    return redirect ("/")


def predict_chances(request):

    if request.POST.get('action') == 'post':
        Patient_ID = int(request.POST.get('Patient_ID'))
        Patient_Age = int(request.POST.get('Patient_Age'))
        Patient_Gender = int(request.POST.get('Patient_Gender'))
        Patient_Blood_Pressure = int(request.POST.get('Patient_Blood_Pressure'))
        Patient_Heartrate = int(request.POST.get('Patient_Heartrate'))

        # Unpickle model
        model = pd.read_pickle(r"heart.pickle")
        # Make prediction
        result = model.predict([[ Patient_Age, Patient_Gender, Patient_Blood_Pressure, Patient_Heartrate]])

        Heart_Disease = result[0]

        PredResults.objects.create(Patient_ID=Patient_ID, Patient_Age=Patient_Age, Patient_Gender=Patient_Gender,
                                   Patient_Blood_Pressure=Patient_Blood_Pressure, Patient_Heartrate=Patient_Heartrate, Heart_Disease=Heart_Disease)

        return JsonResponse({'result': Heart_Disease, 'Patient_ID': Patient_ID,
                             'Patient_Age': Patient_Age, 'Patient_Gender': Patient_Gender, 'Patient_Blood_Pressure': Patient_Blood_Pressure, 'Patient_Heartrate': Patient_Heartrate},
                            safe=False)

@login_required(login_url='/login/')

def view_results(request):
    # Submit prediction and show all
    data = {"dataset": PredResults.objects.all()}
    return render(request, "results.html", data)


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            login(request, user)
            return redirect("/")
        else:
            for msg in form.error_messages:
                print(form.error_messages[msg])
            return render(request = request,
                          template_name = "register.html",
                          context={"form":form})

    form = UserCreationForm
    return render(request = request,
                  template_name = "register.html",
                  context={"form":form})


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request = request,
                    template_name = "login.html",
                    context={"form":form})


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("/")