from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from .auth import authentication
import pandas as pd
import pickle
from .models import *
import csv
# Create your views here.

# Create your views here.

def index(request):
    return render(request, 'index.html')


# def registration(request):
#     return render(request,'registration.html')


def registration(request):
    if request.method == "POST":
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        repassword = request.POST['repassword']
        # print(first_name, contact_no, ussername)
        verify = authentication(first_name, last_name, password, repassword)
        if verify == "success":
            user = User.objects.create_user(email, password, repassword)  #
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            messages.success(request, "Your Account has been Created.")
            return redirect("log_in")

        else:
            messages.error(request, verify)
            return redirect("registration")
            # return HttpResponse("This is Home page")
    return render(request, "registration.html")


def log_in(request):
    if request.method == "POST":
        # return HttpResponse("This is Home page")
        u_name = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=u_name, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Log In Successful...!")
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid User...!")
            return redirect("log_in")
    return render(request, "log_in.html")


login_required(login_url="log_in")


@login_required(login_url="log_in")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def dashboard(request):
    # if request.method == "POST":
    #     district = request.POST('district')
    #     market = request.POST('market')
    #     commodity = request.POST('commodity')
    #     variety = request.POST('variety')
    #     grade = request.POST('grade')
    #     date = request.POST('price_date')
    #     dataa = Datas(district =district, market = market , commodity = commodity, variety = variety, grade = grade, date = date )
    #     dataa.save()
    #     messages.success(request, "Data saved successfully.")  # Optional: Provide feedback to the user
    #     return redirect("predict")  # Redirect to the dashboard to prevent form resubmission
    # Open the CSV file
    # Open the CSV file
    
    return render(request, 'dashboard.html')


login_required(login_url="log_in")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
# def view(request):
#     return render(request, 'view.html')


@login_required(login_url="log_in")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def log_out(request):
    logout(request)
    messages.success(request, "Log out Successfuly...!")
    return redirect("/")



def pre(request):
    # selected_data = Datas.objects.all()  # Retrieve all data from the database
    # context = {'selected_data': selected_data}
    context={}
    if request.method == 'POST':
        district = request.POST.get('district')
        market = request.POST.get('market')
        commodity = request.POST.get('commodity')
        variety = request.POST.get('variety')
        grade = request.POST.get('grade')
        price_date = request.POST.get('price_date')

        # Load the input data for prediction
        input_row = {
            'District_Name': district,
            'Market_Name': market,
            'Commodity': commodity,
            'Variety': variety,
            'Grade': grade,
            'Price_Date': price_date
        }

        # Load the saved model
        with open('dataset/minprice.pkl', 'rb') as file:
            modelmin = pickle.load(file)

        with open('dataset/maxprice.pkl', 'rb') as file:
            modelmax = pickle.load(file)

        with open('dataset/modalprice.pkl', 'rb') as file:
            modelp = pickle.load(file)

        # Create a DataFrame with the input row
        input_df = pd.DataFrame([input_row])
        # Feature engineering: Extract month and year from Price_Date
        input_df['Month'] = pd.to_datetime(input_df['Price_Date']).dt.month
        input_df['Year'] = pd.to_datetime(input_df['Price_Date']).dt.year
        

        # Make prediction using the loaded models
        predictionmin = int(modelmin.predict(input_df)[0])
        predictionmax = int(modelmax.predict(input_df)[0])
        predictionp = int(modelp.predict(input_df)[0])

        s=Datas(district=district,market=market,commodity=commodity,variety=variety,grade=grade,date=price_date)
        s.save()
        
        # Send the predictions to the
        
        context = {
            'district': district,
            'market': market,
            'commodity': commodity,
            'variety': variety,
            'grade': grade,
            'price_date': price_date,
            'prediction_min': predictionmin,
            'prediction_max': predictionmax,
            'prediction_p': predictionp,
        }
        return render(request, 'predict.html', context)

    return render(request, 'predict.html', context)
  # Render the form template if the request method is not POST

@login_required(login_url="log_in")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def predict(request):
    return render(request, 'predict.html')
