from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from . forms import SignUpForm, HospitalSignUpForm
from . models import *
# Create your views here.


def sig_don(request):

    context = {
        'form_user': SignUpForm,
    }
    if request.user.is_authenticated:
        return redirect('users:home')
    if request.method == 'POST':
        form_user = SignUpForm(request.POST)
        if form_user.is_valid():
            form_user.save()
            username = form_user.cleaned_data.get('username')
            raw_pass = form_user.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_pass)
            user.is_donor = True
            user.save()
            login(request, user)
            print(user)
            return redirect('users:crp_don')
        else:
            return render(request, 'users/signup.html', context)
    else:
        return render(request, 'users/signup.html', context)


def crp_don(request):

    if not request.user.is_authenticated:
        return redirect('users:home')
        # return render(request, 'users/crp_don.html')
    if request.method == "POST":
        user = request.user
        new_donor = Donor()
        if int(request.POST["age"]) > 21:
            print(user)
            new_donor.user = user
            new_donor.contact = int(request.POST["contact"])
            new_donor.blood_group = request.POST["blood_group"]
            new_donor.age = int(request.POST["age"])
            new_donor.city = request.POST["city"]
            new_donor.state = request.POST["state"]
            new_donor.pin_code = int(request.POST["pin_code"])
            new_donor.save()
            return redirect('users:home')
        else:
            context = {
                'error_message': "We Respect Your Heroic Attitude , Once You Come Become 22 come Back Again"
            }
            return render(request, 'users/crp_don.html', context)
    else:
        return render(request, 'users/crp_don.html')


def home(request):

    if request.user.is_authenticated and request.user.is_hospital:
        blood_groups = ["O+", "O-", "A-", "A+", "B-", "B+", "AB-", "AB+", ]
        repos = HospitalRepository.objects.filter(hospital_user_id=request.user.id)
        flag = True
        for blood in blood_groups:
            quantity = 0
            for repo in repos:
                if repo.blood_group == blood:
                    quantity = quantity + repo.quantity
            if quantity < 10:
                flag = False
                break

        if not flag:
            context = {
                'error_message': "Some of Repository is seems to be Empty !!! Please Check Out Now"
            }
            return render(request, 'users/home.html', context)
        return render(request, 'users/home.html')

    if request.user.is_authenticated and request.user.is_donor:
        req = Request.objects.filter(donor_id=request.user.id, status=1)
        if req:
            context = {
                'error_message': "You Have some emergency requests !!! Please check in Requests "
            }
            return render(request, 'users/home.html', context)
        else:
            return render(request, 'users/home.html')
    return render(request, 'users/home.html')


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('users:home')
    else:
        return redirect('users:home')


def login_user(request):
    if request.user.is_authenticated:
        return redirect('users:home')
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            try:

                if request.user.is_hospital:
                    x = request.user.hospital
                else:
                    x = request.user.donor

                return redirect('users:home')

            except:

                if request.user.is_donor:
                    context = {
                        'error_message': "Please Complete Your Profile for Others Benefit :)",
                    }
                    return render(request, 'users/crp_don.html', context)
                else:
                    context = {
                        'error_message': "Please Complete Your Profile for Others Benefit :)",
                    }
                    return render(request, 'users/crp_hos.html', context)
        else:
            context = {
                'error_message': "Username or Password is incorrect"
            }
            return render(request, 'users/login.html', context)
    else:
        return render(request, 'users/login.html')


def update(request):
    if not request.user.is_authenticated:
        return redirect('users:home')
    if request.method == "POST":
        try:
            if request.user.is_donor:
                donor = request.user.donor
                donor.contact = int(request.POST["contact"])
                donor.blood_group = request.POST["blood_group"]
                donor.age = int(request.POST["age"])
                donor.city = request.POST["city"]
                donor.state = request.POST["state"]
                donor.pin_code = int(request.POST["pin_code"])
                donor.save()
                return redirect('users:home')
            else:
                hospital = request.user.hospital
                hospital.contact = request.POST["contact"]
                hospital.registration_id = request.POST["registration_id"]
                hospital.city = request.POST["city"]
                hospital.state = request.POST["state"]
                hospital.pin_code = request.POST["pin_code"]
                hospital.save()
                return redirect('users:home')
        except:
            return redirect('users:home')
    else:
        return render(request, 'users/update.html')


def sig_hos(request):

    context = {
        'form_user': HospitalSignUpForm,
    }
    if request.user.is_authenticated:
        return redirect('users:home')
    if request.method == 'POST':
        form_user = HospitalSignUpForm(request.POST)
        if form_user.is_valid():
            form_user.save()
            username = form_user.cleaned_data.get('username')
            raw_pass = form_user.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_pass)
            user.is_hospital = True
            blood_types = ["O+", "O-", "A-", "A+", "B-", "B+", "AB-", "AB+", ]
            user.save()
            login(request, user)
            for blood in blood_types:
                new_repo = HospitalRepository()
                new_repo.blood_group = blood
                new_repo.hospital_user_id = request.user.id
                new_repo.save()
            return redirect('users:crp_hos')
        else:
            return render(request, 'users/signup.html', context)
    else:
        return render(request, 'users/signup.html', context)


def crp_hos(request):
    if not request.user.is_authenticated:
        return redirect('users:home')
    if request.method == "POST":
        new_hospital = Hospital()
        new_hospital.user = request.user
        new_hospital.contact = request.POST["contact"]
        new_hospital.registration_id = request.POST["registration_id"]
        new_hospital.city = request.POST["city"]
        new_hospital.state = request.POST["state"]
        new_hospital.pin_code = request.POST["pin_code"]
        new_hospital.save()
        return redirect('users:home')
    else:
        return render(request, 'users/crp_hos.html')


def search_donor(request):
    if request.user.is_authenticated:
        if request.user.is_hospital:
            if request.method == "POST":
                blood_group = request.POST["blood_group"]
                city = request.POST["city"]

                all_donors = Donor.objects.filter(blood_group=blood_group, city=city, available=True)
                sent_request_raw = Request.objects.filter(hospital_id=request.user.id)

                sent_request = []
                for req in sent_request_raw:
                    if not req.date_approved:
                        a = req
                        sent_request.append(a)

                donors = []
                for don in all_donors:
                    j = 0
                    for req in sent_request:

                        if req.donor_id == don.id:
                            a = (don, req.status, req.id)
                            j = 1
                            if req.status == 1:
                                donors.append(a)
                            break

                    if j == 0:
                        a = (don, 0)
                        donors.append(a)

                if donors:
                    context = {
                        'donors': donors,
                        'sent_request': sent_request,
                        'blood_group': blood_group,
                        'city': city,
                    }
                    return render(request, 'users/search_donor.html', context)

                context = {
                    'donors': donors,
                    'error_message': "---No Donors are there to be Requested---",
                }
                return render(request, 'users/search_donor.html', context)
            else:
                return render(request, 'users/search_donor.html')
        else:
            return redirect('users:home')
    else:
        return redirect('users:home')


def make_request(request, donor_id, blood_group, city):
    if not request.user.is_authenticated:
        return redirect('users:home')
    if request.user.is_hospital:
        new_request = Request()
        new_request.donor_id = donor_id
        new_request.hospital_id = request.user.id
        new_request.date_requested = timezone.now().date()
        new_request.status = 1
        new_request.save()

        all_donors = Donor.objects.filter(blood_group=blood_group, city=city, available=True)
        sent_request_raw = Request.objects.filter(hospital_id=request.user.id)

        sent_request = []
        for req in sent_request_raw:
            if not req.date_approved:
                sent_request.append(req)

        donors = []

        for don in all_donors:

            j = 0

            for req in sent_request:
                if req.donor_id == don.id:
                    a = (don, req.status, req.id)
                    if req.status == 1:
                        donors.append(a)
                    j = 1
                    break

            if j == 0:
                a = (don, 0)
                donors.append(a)

        context = {
            'donors': donors,
            'blood_group': blood_group,
            'city': city,
        }

        return render(request, 'users/search_donor.html', context)


def undo_request(request, blood_group, city, request_id):
    if not request.user.is_authenticated:
        return redirect('users:home')
    undo_req = Request.objects.get(id=request_id)
    undo_req.delete()

    all_donors = Donor.objects.filter(blood_group=blood_group, city=city, available=True)
    sent_request_raw = Request.objects.filter(hospital_id=request.user.id)

    sent_request = []
    for req in sent_request_raw:
        if not req.date_approved:
            sent_request.append(req)

    donors = []

    for don in all_donors:
        j = 0
        for req in sent_request:
            if req.donor_id == don.id:
                a = (don, req.status, req.id)
                if req.status == 1:
                    donors.append(a)
                j = 1
                break
        if j == 0:
            a = (don, 0)
            donors.append(a)
    context = {
        'donors': donors,
        'blood_group': blood_group,
        'city': city,
        'request_id': request_id
    }
    return render(request, 'users/search_donor.html', context)


def request_view_donor(request):
    if request.user.is_authenticated and request.user.is_donor:
        blood_requests_raw = Request.objects.filter(donor_id=request.user.id)
        blood_requests = []

        for req in blood_requests_raw:
            if not req.date_approved:
                blood_requests.append(req)

        view_request = []
        for reqs in blood_requests:
            if reqs.status == 1:
                user_id = reqs.hospital_id
                hospital_user = CustomUser.objects.filter(id=user_id)
                for user in hospital_user:
                    name = user.first_name
                    contact = user.hospital.contact
                    city = user.hospital.city

                new_view_reqs = (reqs, name, contact, city)
                view_request.append(new_view_reqs)

        if view_request:
            context = {
                'blood_request': view_request,
            }
        else:
            context = {
                'error_message': " No Requests Pending . You are All Done "
            }
        return render(request, 'users/requests_view_donor.html', context)
    return redirect('users:home')


def accept_request(request, request_id):

    if request.user.is_authenticated and request.user.is_donor:
        curr_req = Request.objects.get(id=request_id)
        curr_req.status = 2
        curr_req.save()
        return redirect('users:request_view_donor')

    else:
        return redirect('users:home')


def reject_request(request, request_id):

    print("5")
    if request.user.is_authenticated and request.user.is_donor:
        curr_req = Request.objects.get(id=request_id)
        curr_req.status = 3
        curr_req.date_rejected = timezone.now().date()
        curr_req.save()
        # return redirect('users:request_view_donor')
        if request.method == "POST":
            res = Reason()
            res.decline_reason = request.POST["reasons"]
            res.request = curr_req
            res.save()
            return redirect('users:request_view_donor')
    else:
        return redirect('users:home')


def view_repo(request):
    user = request.user
    if user.is_authenticated and user.is_hospital:
        if request.method == "POST":
            blood_group = request.POST["blood_group"]

            repo = HospitalRepository.objects.filter(hospital_user_id=user.id, blood_group=blood_group)
            context = {
                'repo': repo,
            }
            print(repo)
            return render(request, 'users/view_repo.html', context)
        else:
            repos = HospitalRepository.objects.filter(hospital_user_id=user.id)
            repos_sorted = []
            blood_types = ["O+", "O-", "A-", "A+", "B-", "B+", "AB-", "AB+", ]
            for blood in blood_types:
                for repo in repos:
                    if repo.blood_group == blood:
                        a = (blood, repo.plasma_count, repo.quantity)
                        print(a)
                        if repo.quantity == 0:
                            if repo.plasma_count != 10:
                                continue
                        repos_sorted.append(a)

            context = {
                'repos_sorted': repos_sorted,
            }
            # print(repos_sorted)
            return render(request, 'users/view_repo.html', context)
    else:
        return redirect('users:home')


def add_blood(request):

    user = request.user
    if user.is_authenticated and user.is_hospital:
        # print("yo")
        if request.method == "POST":

            blood_group = request.POST["blood_group"]
            plasma_count = request.POST["plasma_count"]
            quantity = request.POST["quantity"]
            # print(blood_group)
            try:

                repo = HospitalRepository.objects.get(blood_group=blood_group, plasma_count=plasma_count,
                                                      hospital_user_id=user.id)
                repo.quantity = repo.quantity + int(quantity)
                repo.save()

            except:

                # print(1)
                new_repo = HospitalRepository()
                new_repo.blood_group = blood_group
                new_repo.plasma_count = plasma_count
                new_repo.quantity = int(quantity)
                new_repo.hospital_user_id = user.id
                new_repo.save()
                # print(new_repo.blood_group)
                # print(new_repo.quantity)
            return redirect('users:view_repo')


def remove_blood(request):
    user = request.user
    if user.is_authenticated and user.is_hospital:
        if request.method == "POST":

            blood_group = request.POST["blood_group"]
            plasma_count = request.POST["plasma_count"]
            quantity = request.POST["quantity"]
            repo = HospitalRepository.objects.get(blood_group=blood_group, plasma_count=plasma_count
                                                  , hospital_user_id=user.id)
            repo.quantity = repo.quantity - int(quantity)
            repo.save()
            return redirect('users:view_repo')


def active_reqs(request):

    user = request.user
    if user.is_authenticated and user.is_hospital:

        if request.method == "POST":
            blood_group = request.POST["blood_group"]
            blood_request_raw = Request.objects.filter(hospital_id=user.id, blood_group=blood_group)
        else:
            blood_request_raw = Request.objects.filter(hospital_id=user.id)

        blood_request = []
        for req in blood_request_raw:
            if req.status != 4 and req.status != 5:

                donor_user = CustomUser.objects.get(id=req.donor_id)
                a = (donor_user, req)
                blood_request.append(a)

        if blood_request:
            context = {
                'blood_request': blood_request
            }
        else:
            context = {
                'error_message': "You does not having any ACTIVE requests"
            }

        return render(request, 'users/active_requests.html', context)


def approve(request, request_id):
    user = request.user
    if user.is_authenticated and user.is_hospital:
        if request.method == "POST":

            req = Request.objects.get(id=request_id)

            if req.status == 2:
                req.status = 4
                req.date_approved = timezone.now().date()
                req.save()
                rew_donor = Reward()
                rew_donor.req = req
                rew_donor.amount = request.POST["reward"]
                rew_donor.date_rewarded = timezone.now().date()
                rew_donor.save()
                return redirect('users:active_reqs')

            elif req.status == 3:
                req.status = 5
                req.date_approved = timezone.now().date()
                req.save()
                # print(1)
            return redirect('users:active_reqs')

    return redirect('users:home')


def view_history(request):
    user = request.user
    if user.is_authenticated:
        if user.is_hospital:
            if request.method == "POST":
                bg = request.POST["blood_group"]
                blood_request_raw = Request.objects.filter(hospital_id=user.id, blood_group=bg)
                print(blood_request_raw)
            else:
                blood_request_raw = Request.objects.filter(hospital_id=user.id)
            blood_request = []
            for req in blood_request_raw:
                if req.status == 4 or req.status == 5:
                    user_donor = CustomUser.objects.get(id=req.donor_id)
                    a = (user_donor, req)
                    blood_request.append(a)

            if blood_request:
                context = {
                    'blood_request': blood_request
                }
            else:
                context = {
                    'error_message': "History to be Created !!! :)"
                }
            return render(request, 'users/history.html', context)
        else:
            if request.method == "POST":
                bg = request.POST["blood_group"]
                blood_request_raw = Request.objects.filter(hospital_id=user.id, blood_group=bg)
                print(blood_request_raw)
                print(bg)

            else:
                blood_request_raw = Request.objects.filter(donor_id=user.id)
            blood_request = []
            for req in blood_request_raw:
                if req.status == 4 or req.status == 5:
                    user_hospital = CustomUser.objects.get(id=req.hospital_id)
                    a = (user_hospital, req)
                    blood_request.append(a)

            if blood_request:
                context = {
                    'blood_request': blood_request
                }
            else:
                context = {
                    'error_message': "History to be Created !!! :)"
                }
            return render(request, 'users/history.html', context)

    return redirect('users:home')


def change(request):
    user = request.user
    if user.is_authenticated and user.is_donor:

        user.donor.available = not user.donor.available
        user.donor.save()

        return redirect( request.POST["url"] )
    else:
        return redirect('users:home')