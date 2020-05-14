from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . models import Subscribers
from programminghunts.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
import math, random
from django.contrib.gis.geoip2 import GeoIP2
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages

def generate_token():
	digits = '0123456789abcdefghijklmnopqrstuvwxyz.-_'
	otp = ''
	for i in range(45):
		otp += digits[math.floor(random.random() * 39)]
	return otp

def subscribe(request):
	if request.method == "POST":
		data = request.POST
		print("request.POST request.POST ", request.POST)
		first_name = data.get("f_name")
		last_name = data.get("l_name")
		email = data.get("email")
		try:
			is_subscribed = Subscribers.objects.get(email=email)
			if is_subscribed.is_verified == False:
				messages.error(request, "You are already subscribed, please check inbox and verify your email")
				return redirect(request.get_full_path())
			else:
				messages.error(request, "You are already subscribed for our Newsletter")
				return redirect(request.get_full_path())
		except:
			token_available = True
			while token_available:
				otp = generate_token()
				token = Subscribers.objects.filter(otp=otp).exists()
				if token:
					token_available = True
				else:
					token_available = False

			ip = request.META.get('REMOTE_ADDR', None)
			g = GeoIP2()
			city = g.city('2409:4056:18a:6b0b:2cfd:ea8d:8a3b:16ac')
			subscriber = Subscribers.objects.create(first_name=first_name, last_name=last_name,
				email=email, ip=ip, city=city['city'], country=city['country_name'], otp=otp)
			msg_html = render_to_string('subscriber/verification_template.html', {'first_name': first_name, 'action_url':settings.BASE_URL+'/activate/'+otp})
			if subscriber:
				send_mail('ProgrammingHunts - Email Verification',
				"", EMAIL_HOST_USER, [email, ], html_message=msg_html, fail_silently = True)
				messages.success(request, "Verification link sent to your email")
				return redirect(request.get_full_path())
			else:
				messages.error(request, "Unable to make subscribe request")
				return redirect(request.get_full_path())
	return redirect('/')

def verify_email(request, token):
	try:
		subscriber = Subscribers.objects.get(otp=token)
		if subscriber.is_verified == True:
			messages.error(request, "Your email is already verified")
			return redirect(settings.BASE_URL)
		subscriber.is_verified = True
		subscriber.save()
		messages.success(request, "Email verified successfully")
		return redirect(settings.BASE_URL)
	except:
		messages.error(request, "Email verification failed")
		return redirect(settings.BASE_URL)

