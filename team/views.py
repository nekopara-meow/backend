import datetime
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from interact.models import Member_in_Team, PersonalMessage
from team.models import Team
from team.models import Uml
from projects.models import Projectt
import datetime
from users.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


# Create your views here.

@csrf_exempt
def establish(request):
    username = json.loads(request.body)['username']
    team_name = json.loads(request.body)['team_name']
    brief_intro = json.loads(request.body)['brief_intro']
    # success
    new_team = Team()
    new_team.team_name = team_name
    new_team.creator = username
    new_team.create_time = datetime.datetime.now()
    new_team.member_num = 1
    new_team.project_num = 0
    new_team.brief_intro = brief_intro
    new_team.save()

    new_mem_in_team = Member_in_Team()
    new_mem_in_team.username = username
    new_mem_in_team.team_id = new_team.team_id
    new_mem_in_team.priority = 2
    new_mem_in_team.save()
    return JsonResponse({'status_code': 1, 'team_id': new_team.team_id, "priority": new_mem_in_team.priority})


@csrf_exempt
def invite(request):
    inviter_username = json.loads(request.body)['inviter']  # 邀请人
    invitee_username = json.loads(request.body)['invitee']  # 被邀请人
    team_id = json.loads(request.body)['team_id']
    inviter = User.objects.get(username=inviter_username)
    # invitee = User.objects.get(username=invitee_username)
    already_in = Member_in_Team.objects.filter(username=invitee_username, team_id=team_id)
    if already_in:
        return JsonResponse({'status_code': 2, 'msg': "Invitee has been already in the team"})
    if Member_in_Team.objects.get(username=inviter.username, team_id=team_id).priority < 1:
        return JsonResponse({'status_code': 3, 'msg': "Inviter doesn't have the priority"})

    new_message = PersonalMessage()
    new_message.message_type = 1
    new_message.team_id = team_id

    new_message.sender = inviter_username
    new_message.receiver = invitee_username
    new_message.save()
    # new_mem_in_team = Member_in_Team()
    # new_mem_in_team.username = invitee_username
    # new_mem_in_team.team_id = team_id
    # new_mem_in_team.priority = 0
    # new_mem_in_team.save()
    return JsonResponse({'status_code': 1, 'msg': "Invite success"})


@csrf_exempt
def setAdmins(request):
    setter_username = json.loads(request.body)['setter']  # 设置人
    settee_username = json.loads(request.body)['settee']  # 被设置人
    team_id = json.loads(request.body)['team_id']
    setter = Member_in_Team.objects.get(username=setter_username,team_id=team_id)
    settee = Member_in_Team.objects.get(username=settee_username,team_id=team_id)
    already_in = Member_in_Team.objects.filter(username=settee_username, team_id=team_id, priority=1)
    if already_in:
        return JsonResponse({'status_code': 2, 'msg': "Has already been admin"})
    if Member_in_Team.objects.get(username=setter.username, team_id=team_id).priority < 2:
        return JsonResponse({'status_code': 3, 'msg': "Setter doesn't have the priority"})
    settee.priority = 1
    settee.save()
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
    return JsonResponse({'status_code': 1, 'msg': "删除成功!"})


@csrf_exempt
def viewMembersInTeam(request):
    team_id = json.loads(request.body)['team_id']
    member_list = Member_in_Team.objects.filter(team_id=team_id)
    ans_list = []
    for members in member_list:  # 枚举团队中的每个成员
        member = User.objects.get(username=members.username)
        a = {'username': member.username, 'email': member.email,
             'priority': Member_in_Team.objects.get(username=members.username, team_id=team_id).priority,
             'avatar': member.avatar, 'brief_intro': member.brief_intro
             }
        ans_list.append(a)  # 将每个成员信息拼接起来
    return JsonResponse({'status_code': 1, 'ans_list': ans_list})


@csrf_exempt
def viewSomeonesTeams0(request):
    username = json.loads(request.body)['username']
    team_list = Member_in_Team.objects.filter(username=username, priority=0)

    tmp = []
    Team_Info = []
    User_Info = []
    for teams in team_list:
        team = Team.objects.get(team_id=teams.team_id)
        a = {'team_id': team.team_id, 'team_name': team.team_name,
             'creator': team.creator, 'team_avatar': team.avatar,
             'team_brief_intro': team.brief_intro,
             'create_time': team.create_time, 'member_num': team.member_num,
             'project_num': team.project_num
             }
        Team_Info.append(a)
        member_list = Member_in_Team.objects.filter(team_id=team.team_id)

        for members in member_list:
            member = User.objects.get(username=members.username)
            b = {'team_id': team.team_id, 'username': member.username, 'email': member.email,
                 'priority': Member_in_Team.objects.get(username=members.username, team_id=team.team_id).priority,
                 'avatar': member.avatar, 'brief_intro': member.brief_intro
                 }
            User_Info.append(b)
    Dict = {"team_info": Team_Info, "user_info": User_Info}
    return JsonResponse({'status_code': 1, 'Dict': Dict})


@csrf_exempt
def viewSomeonesTeams1(request):
    username = json.loads(request.body)['username']
    team_list = Member_in_Team.objects.filter(username=username, priority=1)

    tmp = []
    Team_Info = []
    User_Info = []
    for teams in team_list:
        team = Team.objects.get(team_id=teams.team_id)
        a = {'team_id': team.team_id, 'team_name': team.team_name,
             'creator': team.creator, 'team_avatar': team.avatar,
             'team_brief_intro': team.brief_intro,
             'create_time': team.create_time, 'member_num': team.member_num,
             'project_num': team.project_num
             }
        Team_Info.append(a)
        member_list = Member_in_Team.objects.filter(team_id=team.team_id)

        for members in member_list:
            member = User.objects.get(username=members.username)
            b = {'team_id': team.team_id, 'username': member.username, 'email': member.email,
                 'priority': Member_in_Team.objects.get(username=members.username, team_id=team.team_id).priority,
                 'avatar': member.avatar, 'brief_intro': member.brief_intro
                 }
            User_Info.append(b)
    Dict = {"team_info": Team_Info, "user_info": User_Info}

    return JsonResponse({'status_code': 1, 'Dict': Dict})


@csrf_exempt
def viewSomeonesTeams2(request):
    username = json.loads(request.body)['username']
    team_list = Member_in_Team.objects.filter(username=username, priority=2)

    tmp = []
    Team_Info = []
    User_Info = []
    for teams in team_list:
        team = Team.objects.get(team_id=teams.team_id)
        a = {'team_id': team.team_id, 'team_name': team.team_name,
             'creator': team.creator, 'team_avatar': team.avatar,
             'team_brief_intro': team.brief_intro,
             'create_time': team.create_time, 'member_num': team.member_num,
             'project_num': team.project_num
             }
        Team_Info.append(a)
        member_list = Member_in_Team.objects.filter(team_id=team.team_id)

        for members in member_list:
            member = User.objects.get(username=members.username)
            b = {'team_id': team.team_id, 'username': member.username, 'email': member.email,
                 'priority': Member_in_Team.objects.get(username=members.username, team_id=team.team_id).priority,
                 'avatar': member.avatar, 'brief_intro': member.brief_intro
                 }
            User_Info.append(b)
    Dict = {"team_info": Team_Info, "user_info": User_Info}

    return JsonResponse({'status_code': 1, 'Dict': Dict})


@csrf_exempt
def viewTeam(request):
    team_id = json.loads(request.body)['team_id']
    team = Team.objects.get(team_id=team_id)
    return JsonResponse({'status_code': 1, 'avatar': team.avatar,
                         'team_name': team.team_name, 'brief_intro': team.brief_intro,
                         'create_time': team.create_time, 'creator': team.creator
                         })


@csrf_exempt
def viewProjectsInTeam(request):
    team_id = json.loads(request.body)['team_id']
    project_list = Projectt.objects.filter(team_id=team_id)
    ans_list = []
    for projects in project_list:
        a = {'project_id': projects.project_id,
             'project_name': projects.project_name,
             'project_brief_intro': projects.brief_intro,
             'project_create_time': projects.create_time
             }
        ans_list.append(a)
    return JsonResponse({'status_code': 1, 'ans_list': ans_list})


@csrf_exempt
def getCreatorOfTeam(request):
    team_id = json.loads(request.body)['team_id']
    team = Team.objects.get(team_id=team_id)
    if team is None:
        return JsonResponse({'status_code': 2, 'msg': '该团队不存在'})
    else:
        user = User.objects.get(username=team.creator)
        return JsonResponse({
            'status_code': 1, 'creator': team.creator, 'nickname': user.nickname, 'email': user.email,
            'avatar': user.avatar, 'brief_intro': user.brief_intro
        })


@csrf_exempt
def getAdminsOfTeam(request):
    team_id = json.loads(request.body)['team_id']
    team = Team.objects.get(team_id=team_id)
    if team is None:
        return JsonResponse({'status_code': 2, 'msg': '该团队不存在'})
    else:
        ans_list = []
        member_list = Member_in_Team.objects.filter(team_id=team_id, priority=1)
        for members in member_list:
            user = User.objects.get(username=members.username)
            a = ({
                'username': user.username, 'nickname': user.nickname, 'email': user.email,
                'avatar': user.avatar, 'brief_intro': user.brief_intro
            })
            ans_list.append(a)
        return JsonResponse({'status_code': 1, 'ans_list': ans_list})


@csrf_exempt
def getUsersOfTeam(request):
    team_id = json.loads(request.body)['team_id']
    team = Team.objects.get(team_id=team_id)
    if team is None:
        return JsonResponse({'status_code': 2, 'msg': '该团队不存在'})
    else:
        ans_list = []
        member_list = Member_in_Team.objects.filter(team_id=team_id, priority=0)
        for members in member_list:
            user = User.objects.get(username=members.username)
            a = ({
                'username': user.username, 'nickname': user.nickname, 'email': user.email,
                'avatar': user.avatar, 'brief_intro': user.brief_intro
            })
            ans_list.append(a)
        return JsonResponse({'status_code': 1, 'ans_list': ans_list})

# @csrf_exempt
# def save_uml(request):
#     if request.method == 'POST':
#         username = json.loads(request.body)['username']
#         team_id = json.loads(request.body)['team_id']
#         uml_url = json.loads(request.body)['uml_url']
#         new_uml = Uml()
#         new_uml.team_id = team_id
#         new_uml.uml_url = uml_url
#         new_uml.creator = username
#         try:
#             new_uml.save()
#             return JsonResponse({'status_code': 1})
#         except:
#             return JsonResponse({'status_code': 2})
#     else:
#         return JsonResponse({'status_code': -1})
#
#
# @csrf_exempt
# def load_uml(request):
#     if request.method == 'POST':
#         uml_id = json.loads(request.body)['uml_id']
#         try:
#             uml = Uml.objects.get(uml_id=uml_id)
#         except:
#             return JsonResponse({'status_code': 2})
#         uml_url = uml.uml_url
#         return JsonResponse({'status_code': 1, 'uml_url': uml_url})
#     else:
#         return JsonResponse({'status_code': -1})
