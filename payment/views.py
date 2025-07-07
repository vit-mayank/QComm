from django.shortcuts import render,redirect
import razorpay
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import razorpay.errors
from checkout.models import Checkout
# Create your views here.
@csrf_exempt
def create_order_id(request):
    if request.method == "POST":
        try:
            amount = int(request.POST.get('amount')) * 100
        except (TypeError, ValueError):
            return JsonResponse({"error": "Invalid amount"}, status=400)
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        order_data = {
            'amount': amount,
            "currency" : "INR",
            "payment_capture" : 1
        }

        order = client.order.create(order_data)
        return JsonResponse(order)
    return redirect("main")

@csrf_exempt
def verify_payment(request):
    if request.method == "POST":
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        data= request.POST
        params={
            "razorpay_order_id" : data.get('razorpay_order_id'),
            "razorpay_payment_id" : data.get("razorpay_payment_id"),
            "razorpay_signature" : data.get("razorpay_signature")
        }
        checkout_id = data.get('checkout_id')
        try:
            client.utility.verify_payment_signature(params)
            if checkout_id:
                try:
                    checkout = Checkout.objects.get(id=checkout_id)
                    checkout.payment_status = 'paid'
                    checkout.save()
                except Checkout.DoesNotExist:
                    return JsonResponse({"status":"Payment Successful, but checkout not found"})
            return JsonResponse({"status":"Payment Successful"})
        except razorpay.errors.SignatureVerificationError:
            return JsonResponse({"status":"Payment Failed"})
    return JsonResponse({"status":"Invalid Request"})
