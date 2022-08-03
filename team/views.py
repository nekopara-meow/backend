import json
import re
from team.models import Team
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pytz import utc
from interact.models import Member_in_Team
from users.models import User
from utils.email import *
from interact import *
from utils.token import create_token
from utils.token import check_token


# Create your views here.

@csrf_exempt
def establish(request):
    username = json.loads(request.body)['username']
    team_name = json.loads(request.body)['team_name']

    # success
    new_team = Team()
    new_team.team_name = team_name
    new_team.creator = username
    new_team.save()

    new_mem_in_team = Member_in_Team()
    new_mem_in_team.username = username
    new_mem_in_team.team_id = new_team.team_id
    new_mem_in_team.priority = 2
    new_mem_in_team.save()
    return JsonResponse({'status_code': 1, 'team_id': new_team.team_id})


@csrf_exempt
def invite(request):
    inviter_username = json.loads(request.body)['inviter']  # 邀请人
    invitee_username = json.loads(request.body)['invitee']  # 被邀请人
    team_id = json.loads(request.body)['team_id']
    inviter = User.objects.get(username=inviter_username)
    invitee = User.objects.get(username=invitee_username)
    already_in = Member_in_Team.objects.get(username=invitee_username, team_id=team_id)
    if already_in is None:
        return JsonResponse({'status_code': 2, 'msg': "Invitee has been already in the team"})
    if Member_in_Team.objects.get(usernam=inviter.username, team_id=team_id).priority < 1:
        return JsonResponse({'status_code': 3, 'msg': "Inviter doesn't have the priority"})
    new_mem_in_team = Member_in_Team()
    new_mem_in_team.username = invitee_username
    new_mem_in_team.team_id = team_id
    new_mem_in_team.priority = 0
    new_mem_in_team.save()
    return JsonResponse({'status_code': 1, 'msg': "Invite success"})


@csrf_exempt
def setAdmins(request):
    setter_username = json.loads(request.body)['setter']  # 设置人
    settee_username = json.loads(request.body)['settee']  # 被设置人
    team_id = json.loads(request.body)['team_id']
    setter = User.objects.get(username=setter_username)
    settee = User.objects.get(username=settee_username)
    already_in = Member_in_Team.objects.get(username=settee_username, team_id=team_id, priority=1)
    if already_in is None:
        return JsonResponse({'status_code': 2, 'msg': "Has already been admin"})
    if Member_in_Team.objects.get(usernam=setter.username, team_id=team_id).priority < 2:
        return JsonResponse({'status_code': 3, 'msg': "Setter doesn't have the priority"})
    settee.priority = 1
    return JsonResponse({'status_code': 1, 'msg': "Set success"})


@csrf_exempt
def deleteMem(request):
    deleter_username = json.loads(request.body)['deleter_username']  # 删除人
    deletee_username = json.loads(request.body)['deletee_username']  # 被删除人
    team_id = json.loads(request.body)['team_id']
    deleter = Member_in_Team.objects.get(username=deleter_username, team_id=team_id)
    deletee = Member_in_Team.objects.get(username=deletee_username, team_id=team_id)
    if deleter.priority < deletee.priority:
        return JsonResponse({'status_code': 2, 'msg': "Deleter doesn't have the priority"})

    # delete successfully
    Member_in_Team.objects.get(username=deletee_username, team_id=team_id).delete()


@csrf_exempt
def view(request):
    team_id = json.loads(request.body)['team_id']
    member_list = Member_in_Team.objects.filter(team_id=team_id)
    ans_list = []
    for members in member_list:  # 枚举团队中的每个成员
        a = {'username': members.username, 'email': members.email,
             'priority': Member_in_Team.objects.get(username=members.username, team_id=team_id).priority
             }
        ans_list.append(a)  # 将每个成员信息拼接起来
    return JsonResponse({'status_code': 1, 'ans_list': ans_list})


@csrf_exempt
def viewSomeonesTeams(request):
    username = json.loads(request.body)['username']
    team_list = Member_in_Team.objects.filter(username=username)
    ans_list = []
    for teams in team_list:
        a = {'team_name': teams.team_name, 'establisher': teams.establisher,
             'establish_time': teams.establish_time, 'member_num': teams.member_num,
             'project_num': teams.project_num
             }
        ans_list.append(a)
    return JsonResponse({'status_code': 1, 'ans_list': ans_list})


@csrf_exempt
def join(request):
    username = json.loads(request.body)['username']
    team_id = json.loads(request.body)['team_id']
