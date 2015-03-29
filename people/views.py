#-*- coding: utf-8 -*-
from datetime import date, datetime

from django.shortcuts import render_to_response, get_object_or_404, RequestContext, redirect, render
from django.utils.encoding import smart_str, smart_unicode
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.contrib.auth import logout 
from django.template import loader, RequestContext as TemplateRequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from weilink.settings import MESSAGE_EACH_PAGE, FOLLOW_EACH_PAGE, FAN_EACH_PAGE, BACKGROUND_IMG_COUNT
from message.models import Message, Atuser, Comment, Agree, Retweet, Collection
from com.utils import paginate, AjaxData, AjaxWarn, AjaxFail, AjaxSuccess, AjaxJump, AjaxAlert
from models import People, Relationship, Blacklist, WlSettings, Whitelist, PasswordTicket
from relation import Relation
import services


def profile(request, pid):
	request_people = get_object_or_404(People, pk=pid)
	if request.user.is_authenticated():
		people = request.user.people
	else:
		people = None
	user = request_people.user
	if request.user.is_authenticated() and request.user.id == user.id:
		message_list = user.message_set.all()
	else:
		message_list = user.message_set.filter(private=False)
	
	if people and request_people.id != people.id:
		state = services.relation_state(people.user, request_people.user)
	else:
		state = ""
	
	if people and request_people.id != people.id:
		wlset = user.wlsettings
		if wlset.account_mode == 'N':
			show = "HIDDEN"
		elif wlset.account_mode == 'S':
			befollowed = Relationship.objects.filter(wluserid=people.user.id, followerid=user.id)
			onwhitelist = str(people.user.id) in user.whitelist.white_list
			if not(befollowed or onwhitelist):
				show = "HIDDEN"
			else:
				show = ""
		else:
			show = ""
	else:
		show = ""

	query = request.GET.get("query", "")
	tweet_type = request.GET.get("type", "")
	if query:
		message_list = message_list.filter(content__icontains=query)
	if tweet_type:
		if tweet_type == 'ori':
			message_list = message_list.filter(isoriginal=True)
		if tweet_type == 'rte':
			message_list = message_list.filter(isoriginal=False)
		if tweet_type == 'pub':
			message_list = message_list.filter(private=False)
		if tweet_type == 'pri':
			message_list = message_list.filter(private=True)
	
	page = request.GET.get("page", "")
	messages, paginator = paginate(message_list, MESSAGE_EACH_PAGE, page)
	
	message_num = user.message_set.all().count()
	follow_num = Relationship.objects.filter(followerid=user.id).count()
	follower_num = Relationship.objects.filter(wluserid=user.id).count()
	
	
	return render_to_response("people/profile.html", {"people": people, "request_people": request_people, "messages": messages, "paginator": paginator, "message_num": message_num, "follow_num": follow_num, "follower_num": follower_num, "state": state, "show": show}, RequestContext(request))

def get_background(request, pid):
	people = get_object_or_404(People, pk=pid)
	wluser = people.user
	wlsettings = wluser.wlsettings
	bgimg = wlsettings.background
	return AjaxSuccess(str(bgimg))

@login_required(login_url="/login")
def people_logout(request):
	logout(request)
	return HttpResponseRedirect("/login")


@login_required(login_url="/login")
def people_info(request, pid):
	request_people = get_object_or_404(People, pk=pid)
	people = request.user.people
	state = services.relation_state(people.user, request_people.user)
	return render_to_response("people/people_info.html", {"people": people, "request_people": request_people, "state": state}, RequestContext(request))


@login_required(login_url="/login")
def settings(request):
	authuser = request.user
	people = authuser.people
	wlsettings = authuser.wlsettings
	bglist = [ n for n in xrange(1, BACKGROUND_IMG_COUNT+1)]
	return render_to_response("people/settings.html", {"people": people, "bglist": bglist, "wlsettings": wlsettings}, RequestContext(request))


@login_required(login_url="/loign")
def fillinfo(request):
	people = request.user.people
	if request.method == 'GET':
		return render_to_response("people/fillinfo.html", {"people": people},  RequestContext(request))
	nickname = request.POST.get("nickname", "").strip()
	introduction = request.POST.get("introduction", "").strip()
	realname = request.POST.get("realname", "").strip()
	prov = request.POST.get("prov", "").strip()
	city = request.POST.get("city", "").strip()
	gender = request.POST.get("gender", "")
	sexual = request.POST.get("sexual", "")
	feeling = request.POST.get("feeling", "")
	birthday = request.POST.get("birthday", "")
	domainurl = request.POST.get("domainurl", "").strip()
	introduction = request.POST.get("introduction", "").strip()
	contact_email = request.POST.get("email", "").strip()
	QQ = request.POST.get("QQ", "").strip()
	wechat = request.POST.get("wechat", "").strip()
	profession = request.POST.get("profession", "").strip()
	label = request.POST.get("label", "").strip()
	
	if nickname:
		people.nickname = nickname
	if realname:
		people.realname = realname
	if introduction:
		people.introduction = introduction
	if prov and city:
		address = prov+'-'+city
		people.address = address
	if gender and gender in 'UFM':
		people.gender = gender
	if sexual and sexual in 'SHBU':
		people.sexual = sexual
	if feeling and feeling in 'SAIEDU':
		people.feeling = feeling
	if birthday:
		date_list = birthday.split('-')
		birthdate = date(int(date_list[0]), int(date_list[1]),int(date_list[2]))
		people.birthday = birthdate
	if domainurl:
		people.domainurl = domainurl
	if introduction:
		people.introduction = introduction
	if contact_email:
		people.contact_email = contact_email
	if QQ:
		people.QQ = QQ
	if wechat:
		people.wechat = wechat
	if profession:
		people.profession = profession
	if label:
		people.label = label 
	people.save()
	return HttpResponseRedirect("/people/newrecommend")
	

@login_required(login_url="/login")
def newuser_recommend_follow(request):
	people = request.user.people
	follows = services.newuser_recommend()
	return render_to_response("people/newuserfollow.html", {"people": people, "follows": follows}, RequestContext(request))


@login_required(login_url="/login")
def home(request):
	user = request.user
	people = user.people 
	message_list, paginator = services.get_recent_messages(request)
	message_num = user.message_set.all().count()
	follow_num = Relationship.objects.filter(followerid=user.id).count()
	follower_num = Relationship.objects.filter(wluserid=user.id).count()
	return render_to_response("people/home.html", {"people": people, "message_list": message_list, "paginator": paginator, "message_num": message_num, "follow_num": follow_num, "follower_num": follower_num}, RequestContext(request))

@login_required(login_url="/login")
def follow_page(request, pid):
	request_people = get_object_or_404(People, pk=pid)
	request_user = request_people.user
	authuser = request.user
	people = authuser.people

	follow_queryset = Relationship.objects.filter(followerid=request_user.id)
	follow_id_list = follow_queryset.values_list("wluserid", flat=True)
	follows = People.objects.filter(user_id__in=follow_id_list)

	page = request.GET.get("page", "")
	follow_list, paginator = paginate(follows, FOLLOW_EACH_PAGE, page)
	if request_people.id == people.id:
		friend_state = services.friend_state
		follow_states = [ friend_state(authuser, follow.user) for follow in follow_list]
	else:
		relation_state = services.relation_state
		follow_states = [ relation_state(authuser, follow.user) for follow in follow_list]
	follow_relations = [ Relation(follow, state) for (follow, state) in zip(follow_list, follow_states)]
	current_page = follow_list.number
	return render_to_response("people/follow.html", {"people": people, "request_people": request_people, "current_page": current_page, "follow_relations": follow_relations, "paginator": paginator})


@login_required(login_url="/login")
def fan_page(request, pid):
	authuser = request.user
	people = authuser.people

	request_people = get_object_or_404(People, pk=pid)
	request_user = request_people.user
	
	fan_id_list = Relationship.objects.filter(wluserid=request_user.id).values_list('followerid', flat=True)
	fans = People.objects.filter(user_id__in=fan_id_list)
	page = request.GET.get("page", "")
	fan_list, paginator = paginate(fans, FAN_EACH_PAGE, page)
	if request_people.id == people.id:
		fan_state = services.fan_state
		fan_states = [ fan_state(authuser, fan.user) for fan in fan_list]
	else:
		relation_state = services.relation_state
		fan_states = [ relation_state(authuser, fan.user) for fan in fan_list]
	fan_relations = [ Relation(fan, state) for (fan, state) in zip(fan_list, fan_states)]
	current_page = fan_list.number
	return render_to_response("people/fan.html", {"people": people, "request_people": request_people, "fan_relations": fan_relations, "paginator": paginator,  "current_page": current_page})


@login_required(login_url="/login")
def blacklist_page(request):
	authuser = request.user
	people = authuser.people
	blackerid_list = Blacklist.objects.filter(wluserid=authuser.id).values_list("blackerid", flat=True)
	blacker_list = People.objects.filter(user_id__in=blackerid_list)
	return render_to_response("people/blacklist.html", {"people": people, "request_people": people, "blacker_list": blacker_list})


@login_required(login_url="/login")
@csrf_exempt
def follow_action(request):
	pid = request.POST.get("pid", "")
	if not(pid and pid.isdigit()):
		return AjaxWarn("Fail! Pid empty!")
	pid = int(pid)
	fpeople = get_object_or_404(People, pk=pid)
	fuser = fpeople.user
	authuser = request.user 
	relation_query = Relationship.objects.filter(wluserid=fuser.id, followerid=authuser.id)
	if relation_query:
		relation_query.delete()
		return AjaxSuccess("NOTHING")
	else:
		black_query = Blacklist.objects.filter(wluserid=fuser.id, blackerid=authuser.id)
		if black_query:
			return AjaxWarn("Fail! Sorry you are on the list!")
		
		fwlset = fuser.wlsettings
		fmode = fwlset.account_mode
		if fmode == 'N':
			return AjaxAlert("用户开启自闭模式，您无法关注他/她")
		if fmode == 'S' and str(authuser.id) not in fuser.whitelist.white_list:
			return AjaxAlert("用户开启白名单模式，您不能关注他/她")

		relationship = Relationship(wluserid=fuser.id, followerid=authuser.id)
		relationship.save()
		if Relationship.objects.filter(wluserid=authuser.id, followerid=fuser.id):
			state = "FRIEND"
		else:
			state = "FOLLOW"
		return AjaxSuccess(state)



@login_required(login_url="/login")
@csrf_exempt
def remove_fan(request):
	pid = request.POST.get("pid", "")
	if not(pid and pid.isdigit()):
		return AjaxWarn("pid empty!")
	pid = int(pid)
	bfpeople = get_object_or_404(People, pk=pid)
	bfuser = bfpeople.user
	Relationship.objects.filter(wluserid=request.user.id, followerid=bfuser.id).delete()
	return AjaxSuccess("remote follower success!")


@login_required(login_url="/login")
@csrf_exempt
def add_blacklist(request):
	pid = request.POST.get("pid", "")
	if not(pid and pid.isdigit()):
		return AjaxWarn("pid empty!")
	
	pid = int(pid)
	fpeople = get_object_or_404(People, pk=pid)
	fuser = fpeople.user
	authuser = request.user
	
	Relationship.objects.filter(wluserid=fuser.id, followerid=authuser.id).delete()
	Relationship.objects.filter(wluserid=authuser.id, followerid=fuser.id).delete()

	Atuser.objects.filter(atuserid=fuser.id, useratid=authuser.id).delete()
	Atuser.objects.filter(atuserid=authuser.id, useratid=fuser.id).delete()

	blacklist = Blacklist(wluserid=authuser.id, blackerid=fuser.id)
	blacklist.save()
	
	return AjaxSuccess("add blacklist success!")

@login_required(login_url="/login")
@csrf_exempt
def remove_blacklist(request):
	pid = request.POST.get("pid", "")
	if not(pid and pid.isdigit()):
		return AjaxWarn("pid empty!")
	
	pid = int(pid)
	bpeople = get_object_or_404(People, pk=pid)
	buser = bpeople.user
	
	Blacklist.objects.filter(wluserid=request.user.id, blackerid=buser.id).delete()
	return AjaxSuccess("remove blacklist success!")


@login_required(login_url="/loing")
def set_info(request):
	people = request.user.people
	if request.method == "GET":
		if people.address and '-' in people.address:
			prov, city = people.address.split('-')
		elif people.address:
			prov, city = people.address, ''
		else:
			prov, city = '', ''
		if people.birthday:
			birthday = people.birthday.strftime("%Y-%m-%d")
		else:
			birthday = ''
		return render_to_response("people/setinfo.html", {"people": people, "prov": prov, "city": city, "birthday": birthday}, RequestContext(request))

	nickname = request.POST.get("nickname", "").strip()
	introduction = request.POST.get("introduction", "").strip()
	realname = request.POST.get("realname", "").strip()
	prov = request.POST.get("prov", "").strip()
	city = request.POST.get("city", "").strip()
	gender = request.POST.get("gender", "")
	sexual = request.POST.get("sexual", "")
	feeling = request.POST.get("feeling", "")
	birthday = request.POST.get("birthday", "")
	domainurl = request.POST.get("domainurl", "").strip()
	introduction = request.POST.get("introduction", "").strip()
	contact_email = request.POST.get("email", "").strip()
	QQ = request.POST.get("QQ", "").strip()
	wechat = request.POST.get("wechat", "").strip()
	profession = request.POST.get("profession", "").strip()
	label = request.POST.get("label", "").strip()
	
	people.nickname = nickname
	people.introduction = introduction
	people.realname = realname
	if prov and city:
		address = prov+'-'+city
	else:
		address = prov+city
	people.address = address
	people.gender = gender
	people.sexual = sexual
	people.feeling = feeling
	if birthday:
		date_list = birthday.split('-')
		birthdate = date(int(date_list[0]), int(date_list[1]),int(date_list[2]))
		people.birthday = birthdate
	else:
		people.birthday = ''
	if domainurl:
		people.domainurl = domainurl
	people.introduction = introduction
	people.contact_email = contact_email
	people.QQ = QQ
	people.wechat = wechat
	people.profession = profession
	people.label = label 
	people.save()
	return HttpResponseRedirect("/people/home")



@login_required(login_url="/login")
@csrf_exempt
def get_relation_info(request):
	#rpid: request people id
	rpid= request.POST.get("rpid", "")
	#apid: auth people id
	apid = request.POST.get("apid", "")
	if not(rpid and apid and rpid.isdigit() and apid.isdigit()):
		return AjaxWarn("Params error!")
	rpid = int(rpid)
	apid = int(apid)
	rpeople = get_object_or_404(People, pk=rpid)
	apeople = get_object_or_404(People, pk=apid)
	ruser = rpeople.user
	auser = apeople.user
	if rpid == apid:
		follow_num = Relationship.objects.filter(followerid=auser.id).count()
		fan_num = Relationship.objects.filter(wluserid=auser.id).count()
		black_num = Blacklist.objects.filter(wluserid=auser.id).count()
		followids = Relationship.objects.filter(followerid=auser.id).values_list('wluserid', flat=True)
		#fanids = Relationship.objects.filter(wluserid=apid).values_list('followerid', flat=True)

		friend_num = Relationship.objects.filter(wluserid=auser.id, followerid__in=followids).count()
		template = loader.get_template("people/relation_info.html")
		context = TemplateRequestContext(request, {"home":True, "follow_num": follow_num, "fan_num": fan_num, "black_num": black_num, "friend_num": friend_num, "request_people": rpeople})
		return HttpResponse(template.render(context))
	else:
		follow_num = Relationship.objects.filter(followerid=ruser.id).count()
		fan_num = Relationship.objects.filter(wluserid=ruser.id).count()
		aufollowids = Relationship.objects.filter(followerid=auser.id).values_list('wluserid', flat=True)
		aufanids = Relationship.objects.filter(wluserid=auser.id).values_list('followerid', flat=True)
		common_follow_count = Relationship.objects.filter(followerid=ruser.id, wluserid__in=aufollowids).count()
		common_fan_count =  Relationship.objects.filter(wluserid=ruser.id, followerid__in=aufanids).count()
		template = loader.get_template("people/relation_info.html")
		context = TemplateRequestContext(request, {"home":False, "follow_num": follow_num, "fan_num": fan_num, "common_follow_count": common_follow_count, "common_fan_count": common_fan_count, "request_people": rpeople})
		return HttpResponse(template.render(context))


@login_required(login_url="/login")
def get_follow(request):
	authuser = request.user
	followid_list = Relationship.objects.filter(followerid=authuser.id).values_list("wluserid", flat=True)
	follow_list = People.objects.filter(user_id__in=followid_list)
	template = loader.get_template("people/follow_cut.html")
	context = TemplateRequestContext(request, {"follow_list": follow_list})
	return HttpResponse(template.render(context))



@login_required(login_url="/login")
@csrf_exempt
def match_nickname(request):
	authuser = request.user
	people = authuser.people

	nickname = request.POST.get("nickname", "")
	if not nickname:
		return AjaxWarn("Nick emtpy!")

	people_query = People.objects.filter(nickname=nickname)
	if people_query and people_query[0].id != people.id:
		return AjaxAlert("Nickname taken!")

	return AjaxSuccess("Nickname accessable!")


@login_required(login_url="/login")
@csrf_exempt
def match_domainurl(request):
	authuser = request.user
	people = authuser.people

	domainurl = request.POST.get("domainurl", "").strip()
	if not domainurl:
		return AjaxSuccess("Empty allow!")

	people_query = People.objects.filter(domainurl=domainurl)
	if people_query and people_query[0].id != people.id:
		return AjaxAlert("Domainurl taken!")

	return AjaxSuccess("Domainurl accessable!")


@login_required(login_url="/login")
@csrf_exempt
def match_password(request):
	authuser = request.user
	password = request.POST.get("password", "").strip()
	if not password:
		return AjaxAlert("Empty password!")

	if authuser.check_password(password):
		return AjaxSuccess("Password correct!")
	return AjaxFail('密码不正确!')


@login_required(login_url="/login")
def update_password(request):
	authuser = request.user
	oldpassword = request.POST.get("oldpassword", "").strip()
	newpassword1 = request.POST.get("newpassword1", "").strip()
	newpassword2 = request.POST.get("newpassword2", "").strip()

	if not authuser.check_password(oldpassword):
		return AjaxFail("密码不正确!")

	if not ( newpassword1 and newpassword2 and newpassword1 == newpassword2):
		return AjaxAlert("输入两次密码不一致!")

	authuser.set_password(newpassword1)
	authuser.save()
	return AjaxSuccess("密码修改成功!")

@login_required(login_url="/login")
def update_background(request):
	authuser = request.user
	bgimg = request.POST.get("bgimg", "")

	if not(bgimg and bgimg.isdigit()):
		return AjaxAlert("bgimg should be integer!")

	bgimg = int(bgimg)
	if bgimg < 0 or bgimg > BACKGROUND_IMG_COUNT:
		return AjaxAlert("bgimg out or range!")
	
	wlsettings = authuser.wlsettings
	wlsettings.background= bgimg
	wlsettings.save()
	return AjaxSuccess("设置成功!")


@login_required(login_url="/login")
def update_mode(request):
	authuser = request.user
	mode = request.POST.get("mode", "").strip()

	if not mode:
		return AjaxAlert("Mode empty!")

	if mode not in ("A", "S", "N"):
		return AjaxAlet("Params invalid!")

	wlsettings = authuser.wlsettings
	wlsettings.account_mode = mode
	wlsettings.save()
	if mode == 'N':
		Relationship.objects.filter(wluserid=authuser.id).delete()
		wlsettings.account_visible = False 
		wlsettings.retweet_visible = False
		wlsettings.save()
	elif mode == 'S':
		whitelist_query = Whitelist.objects.filter(wluser=authuser)
		if not whitelist_query:
			whitelist = Whitelist()
			whitelist.wluser = authuser
			whitelist.save()
		wlsettings.account_visible = False
		wlsettings.retweet_visible = False
		wlsettings.save()

	return AjaxSuccess("设置成功!")


@login_required(login_url="/login")
def private_schema(request):
	authuser = request.user
	account_visible = request.POST.get("avisible", "")
	tweet_visible = request.POST.get("tvisible", "")

	if not( account_visible and tweet_visible):
		return AjaxAlert("Params empty!")

	wlsettings = authuser.wlsettings
	if account_visible == 'no':
		wlsettings.account_visible = False
	else:
		wlsettings.account_visible = True

	if tweet_visible == 'no':
		wlsettings.tweet_visible = False
	else:
		wlsettings.tweet_visible = True
	
	wlsettings.save()
	return AjaxSuccess("设置隐私机制成功!")

@login_required(login_url="/login")
def remind_schema(request):
	authuser = request.user
	message_remind = request.POST.get("mrnd", "")

	if not message_remind:
		return AjaxAlert("Params empty!")

	wlsettings = authuser.wlsettings
	if message_remind == 'no':
		wlsettings.message_remind = False
	else:
		wlsettings.message_remind = True
	wlsettings.save()
	return AjaxSuccess("消息提醒设置成功!")


	









