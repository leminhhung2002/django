from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.db import connection
from .import models
import json
from django.shortcuts import render

# Create your views here.


@csrf_exempt
def index(req):
    routes = [
        {
            "url": "/api/",
            "method": "*",
            "description": "This is the index page."
        },
        {
            "url": "/api/get_user/<wallet_address>",
            "method": "GET",
            "description": "This endpoint returns the user data for the given wallet address."
        },
        {
            "url": "/api/get_buy_history/<wallet_address>",
            "method": "GET",
            "description": "This endpoint returns the buy history for the given wallet address."
        },
        {
            "url": "/api/register_user/",
            "method": "POST",
            "description": "This endpoint registers a new user."
        },
        {
            "url": "/api/save_buy_history/",
            "method": "POST",
            "description": "This endpoint saves a new buy history."
        },
        {
            "url": "/api/show_person_below_introduced/",
            "method": "POST",
            "description": "This endpoint show person below introduced"
        },
        {
            "url": "api/introduce/<wallet_address>",
            "method": "GET",
            "description": "This endpoint insert person below introduced."
        },
        {
            "url": "api/auto_pay_interest/<wallet_address>",
            "method": "POST",
            "description": "This endpoint will auto pay"
        }
    ]

    return JsonResponse({
        "message": "Welcome to the BNB Kingdom API.",
        "routes": routes
    })


@csrf_exempt
def get_user(req, wallet_address):
    if req.method != "GET":
        return JsonResponse({
            "message": "Method not allowed."
        }, status=405)

    try:
        user = models.User.objects.get(wallet_address=wallet_address)
    except models.User.DoesNotExist:
        return JsonResponse({
            "message": "User not found.",
            "error_type": "user_not_found",
        }, status=404)
    response = JsonResponse({
        "message": "User data found.",
        "user": {
            "id": user.user_id,
            "created_at": user.created_at,
            "date_created": user.date_created,
            "wallet_address": user.wallet_address
        }
        })  
    response.set_cookie('wallet_address', wallet_address)  
    return response

@csrf_exempt
def register_user(req):
    if req.method != "POST":
        return JsonResponse({
            "message": "Method not allowed.",
            "error_type": "method_not_allowed"
        }, status=405)

    body = json.loads(req.body.decode("utf-8"))

    if "wallet_address" not in body:
        return JsonResponse({
            "message": "Missing wallet_address.",
            "error_type": "missing_parameter"
        }, status=400)

    wallet_address = body["wallet_address"]

    try:
        user = models.User.objects.get(wallet_address=wallet_address)
        return JsonResponse({
            "message": "User already exists.",
            "error_type": "user_already_exists"
        }, status=400)
    except models.User.DoesNotExist:
        user = models.User(
            wallet_address=wallet_address
        )
        user.save()
        response = JsonResponse({
            "message": "User registered."
        })  
        response.set_cookie('wallet_address', wallet_address)  
        return response 


@csrf_exempt
def save_buy_history(req):
    if req.method != "POST":
        return JsonResponse({
            "message": "Method not allowed.",
            "error_type": "method_not_allowed"
        }, status=405)

    body = json.loads(req.body.decode("utf-8"))

    if "wallet_address" not in body:
        return JsonResponse({
            "message": "Missing wallet_address.",
            "error_type": "missing_parameter"
        }, status=400)

    if "amount_bnb" not in body:
        return JsonResponse({
            "message": "Missing amount_bnb.",
            "error_type": "missing_parameter"
        }, status=400)

    wallet_address = body["wallet_address"]
    amount_bnb = body["amount_bnb"]
    package_selected = body["package_selected"]

    try:
        user = models.User.objects.get(wallet_address=wallet_address)
    except models.User.DoesNotExist:
        return JsonResponse({
            "message": "User not found.",
            "error_type": "user_not_found"
        }, status=404)

    buy_history = models.BuyHistory(
        user=user,
        uid=user.user_id,
        amount_bnb=amount_bnb,
        package_selected=package_selected
    )
    buy_history.save()

    return JsonResponse({
        "message": "Buy history saved."
    })


@csrf_exempt
def get_buy_history(req, wallet_address):
    if req.method != "GET":
        return JsonResponse({
            "message": "Method not allowed."
        }, status=405)

    try:
        history = models.BuyHistory.objects.filter(
            user__wallet_address=wallet_address)
    except models.BuyHistory.DoesNotExist:
        return JsonResponse({
            "message": "Buy history not found.",
            "error_type": "buy_history_not_found"
        }, status=404)

    history_data = []
    for i in history:
        history_data.append({
            "id": i.buy_history_id,
            "user_id": i.user.user_id,
            "wallet_address": i.user.wallet_address,
            "created_at": i.created_at,
            "date_created": i.date_created,
            "date_started": i.get_date_started(),
            "date_finished": i.get_date_finished(),
            "amount_bnb": i.amount_bnb,
            "current_bnb_profit": i.get_current_bnb_profit(),
            "current_bnbk_profit": i.get_current_bnbk_profit(),
            "interest_per_day": i.get_interest_per_day(),
            "is_complete": i.is_complete_task(),
            "program_type": i.get_program_type(),
            "note": i.note
        })

    if len(history_data) == 0:
        return JsonResponse({
            "message": "Buy history not found."
        }, status=404)

    return JsonResponse({
        "message": "Buy history found.",
        "history": history_data
    })

@csrf_exempt
def show_person_below_introduced(req):
    
    if req.method != 'POST':
        return JsonResponse({
            "message": "Method not allowed.",
            "error_type": "method_not_allowed"
        }, status=405)
    body = json.loads(req.body.decode("utf-8"))
    introduction_F = models.Introduction.objects.filter(user_id = body['user_id']).values()
    print(list(introduction_F))
    return JsonResponse({
        "message": 'success query'
    })


@csrf_exempt
def introduce(req, wallet_address, wallet_address_introduced):
    # INPUT 
    # wallet 1 => parent
    # wallet 2 => child
    if req.method != 'GET':
        return JsonResponse({
            "message": "Method not allowed.",
            "error_type": "method_not_allowed"
        }, status=405)
    wallet_address_introduction_by_children = models.Introduction.objects.filter(wallet_address_introduced = wallet_address)
    if wallet_address_introduction_by_children.count() == 0:
        index_f = 0
        introduction_F = models.Introduction(
            wallet_address = wallet_address,
            wallet_address_introduced = wallet_address_introduced,
            F_ratings = 'F{}'.format(index_f + 1)
        )
        introduction_F.save()
        return JsonResponse({'success':'action 1'})
    else:
        index_f = 1
        all_data_introduction = models.Introduction.objects.all().values()
        for data in all_data_introduction:
            if(data['wallet_address_introduced'] == wallet_address):
                print('F', data['F_ratings'])
                print('yes')
                introduction_F = models.Introduction(
                        wallet_address = data['wallet_address'],
                        wallet_address_introduced = wallet_address_introduced,
                        F_ratings = 'F{}'.format(convert_F_to_number(data['F_ratings']) + 1))
                dk_insert = models.Introduction.objects.filter(wallet_address_introduced = wallet_address_introduced)
                if not dk_insert:
                    introduction_F.save()
                    return JsonResponse({'success':'action 2'})
            
        # calc_index = models.Introduction.objects.filter(wallet_address_introduced = wallet_address_introduction_by_children.values()[0]['wallet_address_introduced'])
        # for i in range (0,100,1): 
        #     if calc_index.count() == 1:
        #         calc_index = models.Introduction.objects.filter(wallet_address_introduced = calc_index.values()[0]['wallet_address_introduced']) 
            
        #     else:
        #         print('hel')
        # check_wallet = models.Introduction.objects.filter(wallet_address_introduced = wallet_address).values()
        # total_introduction_F = models.Introduction.objects.filter(wallet_address = check_wallet.values()[0]['wallet_address']).count()
        # introduction_F = models.Introduction(
        #         wallet_address = check_wallet[0]['wallet_address'],
        #         wallet_address_introduced = wallet_address_introduced,
        #         F_ratings = 'F{}'.format(total_introduction_F + 1)
        #     )
        # dk_insert = models.Introduction.objects.filter(wallet_address_introduced = wallet_address_introduced)
        # if not dk_insert:
        #     introduction_F.save()
        #     return JsonResponse({'success':'action 2'})
        return JsonResponse({'error':'not insert DB'})
       
@csrf_exempt
def auto_pay_interest(req, wallet_address ):
    if req.method != 'POST':
        return JsonResponse({
            "message": "Method not allowed.",
            "error_type": "method_not_allowed"
        }, status=405)
    if(wallet_address == 'xxx123'):
        all_data_introduction = models.Introduction.objects.all()
        all_data_history = models.BuyHistory.objects.all()
        for introduction in all_data_introduction:
            F_rating = calc_percent_introduced(introduction.F_ratings)
            wallet = introduction.wallet_address
            for history in all_data_history:
                if(history.user.wallet_address == introduction.wallet_address_introduced):
                    print('yes')
                    print(introduction.wallet_address_introduced)
                    package_by = history.package_selected
                    amount = history.amount_bnb        
                    interest_introduced = amount * F_rating
                    interest_package =  amount *  calc_day(package_by)
                    pay = models.PayInterest(wallet_address = wallet,
                    interest_introduced = interest_introduced,
                    interest_package = interest_package)
                    pay.save()
                else:
                    print('no')
                    print(introduction.wallet_address_introduced)
            
        return JsonResponse(
            {
            "message": 'auto action done'
            })
    else:
        return JsonResponse(
            {
            "message": 'auth fail',
            })

def calc_percent_introduced(F):
    if F == 'F1':
        return 0.08
    if F == 'F2':
        return 0.03
    if F == 'F3':
        return 0.01
    if F == 'F4':
        return 0.01
    if F == 'F5':
        return 0.05
    if F == 'F6':
        return 0.005
    if F == 'F7':
        return 0.005
    if F == 'F8':
        return 0.005
    if F == 'F9':
        return 0.005
    if F == 'F10':
        return 0.005
def calc_day(day):
    if day == 90:
        return 0.21
    if day == 150:
        return 0.4
    if day == 180:
        return 0.54
    if day == 240:
        return 0.8
    if day == 300:
        return 1.1
    if day == 360:
        return 1.44
    

def convert_F_to_number(F):
    if F == 'F1':
        return 1
    if F == 'F2':
        return 2
    if F == 'F3':
        return 3
    if F == 'F4':
        return 4
    if F == 'F5':
        return 5
    if F == 'F6':
        return 6
    if F == 'F7':
        return 7
    if F == 'F8':
        return 8
    if F == 'F9':
        return 9
    if F == 'F10':
        return 10
    

def handler404(req, *args, **argv):
    return JsonResponse({
        "message": "Page not found."
    }, status=404)


def auto_pay(req):
    return render (req,'auto.html')
