from django.shortcuts import render,HttpResponse,redirect
import re
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from malaysia_app.models import *
from django.utils import timezone
from django.db.models import OuterRef,  Subquery, Sum, F, Count
from django.utils.translation import activate
# from .models import UserProfile
from datetime import date
from malaysia_app.models import UserProfile, zikr_count, Target_count
# Create your views here. 
from django.db import IntegrityError 
from django.http import JsonResponse
from malaysia_app.models import Country, State, City
# from django.utils.dateparse import parse_datetime
from datetime import datetime

# Create your views here.

def index(request):
    context = {
    #    'posts': posts

         'user': User.objects.all(),
        #  'profile': Profile.objects.all()
    }
    return render(request,'index.html',context)

def about(request):
    return render(request,'about.html') 

def contact(request):
    return render(request,'contact.html') 
 



def get_states(request):
    country_id = request.GET.get('country_id')
    states = State.objects.filter(country_id=country_id).values('id', 'name')
    return JsonResponse({'states': list(states)})

def get_cities(request):
    state_id = request.GET.get('state_id')
    cities = City.objects.filter(state_id=state_id).values('id', 'name')
    return JsonResponse({'cities': list(cities)})

# def location_selection(request):
#     countries = Country.objects.all()
#     return render(request, 'dashboard.html', {'countries': countries})


@login_required(login_url="/login/")
def dashboard(request):
    target_count = Target_count.objects.get(id=1)
    # print(target_count.traget_count)
#    main page
    if request.method =="POST":
        data = request.POST
        form_Zikr_count_id = request.POST.get('form_Zikr_count_id')  # Get the value of the hidden input field
        # print(form_Zikr_count_id)
        if form_Zikr_count_id == 'form_Zikr_count':  # Check if the form ID matches
       
            new_zikr_count = data.get('zikr_count')
            # new_zikr_date= models.DateTimeField(default=timezone.now)
            # new_zikr_date= timezone.now()
            # try:
            #     parsed_datetime = parse_datetime(new_zikr_date)
            #     # Now you can use parsed_datetime as a datetime object
            #     formatted_datetime = parsed_datetime.strftime("%Y-%m-%d %H:%M:%S")
            # except ValueError:
            #     # Handle the case where the datetime string is not valid
            #     parsed_datetime = None
            # new_zikr_date = data.get('timezone.now()')
            # rec_image = request.FILES.get('rec_image')
        # print(zikr_count)
    
            user = request.user
            try:
                zikr_count_all=zikr_count.objects.create(user=user, zikr_count = new_zikr_count, zikr_date = timezone.now()) 
                # current_day_zikr = zikr_count.objects.filter(user=request.user).aggregate(Sum('zikr_count'))['zikr_count__sum']
                today  = timezone.now().date()
                current_day_zikr = zikr_count.objects.filter(user=request.user, zikr_date__date=today).aggregate(Sum('zikr_count'))['zikr_count__sum']
                # return JsonResponse({'current_day_zikr': current_day_zikr})
                return JsonResponse({'zikr_count': new_zikr_count})
                
                # return redirect('/dashboard/')
            except IntegrityError as e:
                print("IntegrityError:", e)
    
    # if request.method == "POST":
    #     data = request.POST
    #     new_zikr_count = data.get('zikr_count')
    #     user = request.user
    #     zikr_count.objects.create(user=user, zikr_count=new_zikr_count, zikr_date=timezone.now())
    #     return redirect('dashboard')

    today  = timezone.now().date()
    # today_date = User.objects.get(pk=request.user_id)  # Replace with your actual query 
    # user_zikar_date = User.objects.annotate(zikr_date=F('zikr_count__zikr_date')).filter(pk= request.user.id)
    # print(user_zikar_date)
    # user_zikar_date  = zikr_count.objects.get(pk= request.user.id)   # Replace with your actual query
    # user_zikar_date  = zikr_count.objects.filter(user_id= request.user.id).first()
    current_day_zikr = zikr_count.objects.filter(user=request.user, zikr_date__date=today).aggregate(Sum('zikr_count'))['zikr_count__sum']
    try:
        total_zikr_count = zikr_count.objects.filter(user=request.user).aggregate(Sum('zikr_count'))['zikr_count__sum']
    except:
        total_zikr_count = 0
        
    desired_daily_zikr_count = target_count.target_count  # Set your desired daily zikr count here
    # percent_completed = (total_zikr_count / desired_daily_zikr_count) * 100
    all_users_total_zikr = zikr_count.objects.all().aggregate(Sum('zikr_count'))['zikr_count__sum']
    desired_total_zikr = target_count.target_count 
    # if request.user.is_authenticated:
   
    if total_zikr_count is not None and desired_total_zikr is not None:
        total_percentage_completed = (total_zikr_count / desired_total_zikr) * 100
        overall = round(total_percentage_completed)
    else:
        # Handle the case where one or both variables are None
        overall = 0 
        
    # else:
    #     # Handle the case where one or both variables are None
    #     total_percentage_completed = 0  

    if all_users_total_zikr is not None and desired_total_zikr > 0:
        total_percentage_completed = (all_users_total_zikr / desired_total_zikr) * 100
        rounded_total_percentage_completed = round(total_percentage_completed)
    else:
        rounded_total_percentage_completed = 0
    
    subquery = zikr_count.objects.filter(user=OuterRef('pk')).order_by('-zikr_date').values('zikr_date')[:1]

    # Annotate the User queryset with the total zikr_count and the most recent zikr_date
    users_with_total_counts = User.objects.annotate(total_zikr_count=Sum('zikr_count__zikr_count'), zikr_date=Subquery(subquery))
    # users_with_total_counts = None
    # users_with_total_counts = User.objects.annotate(total_zikr_count=Sum('zikr_count__zikr_count'), zikr_date=F('zikr_count__zikr_date'))    
    queryset = zikr_count.objects.filter(user=request.user)
    zikr_entries = list(queryset) 
   
    
    # data=UserProfile.objects.filter(user=request.user)
    # print_r(request)
    UserProfile_user = User.objects.get(username=request.user) 
    UserProfile_loc = UserProfile.objects.filter(user_id= request.user.id).first()
    
    # try:
    #     UserProfile = UserProfile.objects.get(user=request.user)
    # except UserProfile.DoesNotExist:
    #     UserProfile = UserProfile(user=request.user)

# location
    countries = Country.objects.all()
  
# group statistics
    # Assuming you have fields like 'country', 'state', and 'city' in UserProfile model
    result = zikr_count.objects.values('user__userprofile__country', 'user__userprofile__state', 'user__userprofile__city').annotate(total_count=Count('zikr_count'))

# Printing the results
    # group_by_country = [item['user__userprofile__country'] for item in result]
    # group_by_state = [item['user__userprofile__state'] for item in result]
    # group_by_city = [item['user__userprofile__city'] for item in result]
    total_count_world = [item['total_count'] for item in result]

    country_each = zikr_count.objects.values('user__userprofile__country').annotate(total_count=Sum('zikr_count'))
    country_total_counts = {}
    country_percentage={}
    for result in country_each:
        country = result['user__userprofile__country']
        total_count = result['total_count']
        country_total_counts[country] = total_count
         # Calculate the percentage for the current country
        percentage =round((total_count / desired_total_zikr) * 100)

        # Store the percentage in the country_percentage dictionary
        country_percentage[country] = percentage

    state_each = zikr_count.objects.values('user__userprofile__state').annotate(total_count=Sum('zikr_count'))
    state_total_counts = {}
    for result in state_each:
        country = result['user__userprofile__state']
        total_count = result['total_count']
        state_total_counts[country] = total_count
    
    city_each = zikr_count.objects.values('user__userprofile__city').annotate(total_count=Sum('zikr_count'))
    city_total_counts = {}
    for result in city_each:
        country = result['user__userprofile__city']
        total_count = result['total_count']
        city_total_counts[country] = total_count

      #----- search funtion
    all_search = {}
    # if request.method == 'POST':
        # form_search_id = request.POST.get('form_search_id')  # Get the value of the hidden input field
        # if form_search_id == 'form_search':  # Check if the form ID matches
          
    if request.GET.get('search_rec'):
        search_term = request.GET.get('search_rec')
    
    # Perform your filtering logic here
    # search_results = YourModel.objects.filter(your_field__icontains=search_term)
        # filtered_group_data = UserProfile.objects.filter(username__icontains=search_term)

        # Filter the dictionaries based on the search term
        filtered_country_counts = {country: count for country, count in country_total_counts.items() if search_term.lower() in country.lower()}
        filtered_state_counts = {state: count for state, count in state_total_counts.items() if search_term.lower() in state.lower()}
        filtered_city_counts = {city: count for city, count in city_total_counts.items() if search_term.lower() in city.lower()}
        filtered_usernames = {user.username: user.total_zikr_count for user in users_with_total_counts if search_term.lower() in user.username.lower()}
        print (filtered_usernames)
        # Create a dictionary to store filtered search results
        all_search = {
            'Country': filtered_country_counts,
            'State': filtered_state_counts,
            'City': filtered_city_counts,
            'Group / Individual':filtered_usernames
        }

    # Pass the combined filtered dictionaries to the template
    # context = {
    #     'search_results': all_search
    # }
 
    context = {'zikr_count_get':zikr_entries, 
               'total_zikr_count': total_zikr_count, 
               'current_day_zikr' :current_day_zikr,
            #    'percent_completed':percent_completed,
                'all_users_total_zikr':all_users_total_zikr,
                'rounded_total_percentage_completed': rounded_total_percentage_completed,
                'users_with_total_counts' : users_with_total_counts,
                'countries': countries,
                'overall':overall,
                # 'cities': list(cities),
                # 'states': list(states),
                'UserProfile_user' : UserProfile_user,
                'UserProfile_loc':UserProfile_loc, 
                # 'group_by_country' : group_by_country,
                # 'group_by_state' : group_by_state,
                # 'group_by_city' : group_by_city,
                'total_count_world' : total_count_world,
                'country_total_counts': country_total_counts,
                'state_total_counts': state_total_counts,
                'city_total_counts': city_total_counts,
                'search_results': all_search,
                # 'today_date':today_date,
                # 'user_zikar_date':user_zikar_date,
                }

    # return JsonResponse(all_search)
    return render(request, 'dashboard.html', context)
    




def login_page(request):
    if request.method == "POST": 
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not User.objects.filter(username=username).exists():
            messages.error(request, "Username invalid ! Please try some other username.")
            return redirect('/login/')
        user = authenticate(username = username, password = password)
        
        if user is None:
            messages.error(request, "password invalid ! Please try some other username.")
            return redirect('/login/')
        
        else:
            login(request, user)
            messages.error(request, "User logged in .")
            return redirect('/dashboard/')

    return render(request, 'login.html')

def register(request):
    if request.method == "POST":     
      
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('/register/')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('/register/')
        
        if len(username)>20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('/register/')
        
        password = request.POST.get('password')

        # Define regular expressions for character, number, and special character requirements
        character_pattern = re.compile(r'[A-Za-z]')
        number_pattern = re.compile(r'[0-9]')
        special_character_pattern = re.compile(r'[!@#$%^&*()_+{}\[\]:;<>,.?~\\-]')

        # Check if the password meets the requirements
        if not (character_pattern.search(password) and
                number_pattern.search(password) and
                special_character_pattern.search(password)) and len(password) < 8:
                messages.error(request, "Password must contain at least one character, one number, and one special character.")
                return redirect('/register/')
        # if len(password) < 8:
        #     messages.error(request, "Password must be at least 8 characters long.")
        #     return redirect('/register/')
       
        # myuser = User.objects.create_user(username, email, password)
        # myuser.first_name = fname
        # myuser.last_name = lname
        # myuser.is_active = False
        user = User.objects.create(
            email = email,
            username = username,
        )
        user.set_password(password)
        user.save()
        # myuser.is_active = False
        # myuser.save()
        messages.success(request, "Your Account has been created succesfully!!.")
        
        
        return redirect('/login/')
     
    return render(request, 'register.html')



@login_required(login_url="login")
def edit_profile(request):
    # try:
    #     user_profile = UserProfile.objects.get(user=request.user)
    # except UserProfile.DoesNotExist:
    #     user_profile = UserProfile(user=request.user)
    #     user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form_edit_id = request.POST.get('form_edit_id')  # Get the value of the hidden input field
        if form_edit_id == 'form_edit':  # Check if the form ID matches
            global country
            global user_profile
            # country = request.POST.get('country')
            # state = request.POST.get('state')
            # city = request.POST.get('city')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            group_section = request.POST.get('group_section')
        
            # Update the attributes of the User instance
            user = request.user
            if email:  # Only update if email is provided
                user.email = email
                user.save()

            user_profile, created = UserProfile.objects.get_or_create(user=request.user)
            # Update the attributes of the user_profile instance
            if not request.POST.get('country').isnumeric():
                pass
            else:
                country = request.POST.get('country')
                country_name = Country.objects.filter(id=country).first()
                user_profile.country = country_name.name
            
             
            if not request.POST.get('state').isnumeric():
                pass
            else:
                state = request.POST.get('state')
                state_name = State.objects.filter(id=state).first()
                user_profile.state = state_name.name

            if not request.POST.get('city').isnumeric():
                pass
            else:
                city = request.POST.get('city')
                city_name = City.objects.filter(id=city).first()
                user_profile.city = city_name.name
            
            # user_profile.country = country_name.name
            # user_profile.state = state_name.name
            # user_profile.city = city_name.name
                user_profile.phone = phone
                user_profile.email = email
                user_profile.group_section = group_section
                user_profile.save()


            # Update user email if provided
            if email and email != request.user.email:
                request.user.email = email
                request.user.save()
            #  return redirect('/dashboard/')
            # response_data = {'user_profile': user_profile}
            # return JsonResponse(response_data)
            return redirect('/dashboard/')
        all_users=UserProfile.objects.all()
        context = {
            'user_profile': user_profile,
            'all_users':all_users,
            
        }
    # user_profile = user_profile.objects.get(user=user_profile)
    return render(request, 'dashboard.html', context)


def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('/login/')




