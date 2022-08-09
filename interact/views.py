import json
import re
from team.models import Team
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pytz import utc
from projects.models import Projectt, File
from interact.models import Member_in_Team
import datetime
from interact.models import PersonalMessage, ProjectMessage, TeamMessage
from users.models import User

# PersonalMessage里type为0是被踢出团队 1是邀请加入团队 2是被设为管理员 3是被取消管理员

# TeamMessage里type为0    1    2    3
# x邀请y加入团队，x把y踢出团队，x把y设为管理，x撤销y的管理，x新建项目

# ProjectMessage里type为0   1   2   3
# x新建了文件y，x删除了文件y，x开放文件y的预览

@csrf_exempt
def getPersonalMessage(request):
    username = json.loads(request.body)['username']
    ans_list = []
    message_list = PersonalMessage.objects.filter(receiver=username).order_by('-send_time')
    for messages in message_list:
        if messages.message_type == 0:
            a = {
                'id': messages.id,
                'msg':
                    '您被移出了' +
                    str(Team.objects.get(team_id=messages.team_id).team_name),
                'sender': messages.sender, 'send_time': messages.send_time,
                'message_type': messages.message_type, 'team_id': messages.team_id,
                'avatar': User.objects.filter(username=messages.sender)
            }
        if messages.message_type == 1:
            a = {
                'id': messages.id,
                'msg':
                    str(messages.sender) + '邀请您加入' +
                    str(Team.objects.get(team_id=messages.team_id).team_name),
                'sender': messages.sender, 'send_time': messages.send_time,
                'message_type': messages.message_type, 'team_id': messages.team_id,
                'avatar': User.objects.filter(username=messages.sender)
            }
        if messages.message_type == 2:
            a = {
                'id': messages.id,
                'msg':
                    '您''被设为了' +
                    str(Team.objects.get(team_id=messages.team_id).team_name) + "的管理员",
                'sender': messages.sender, 'send_time': messages.send_time,
                'message_type': messages.message_type, 'team_id': messages.team_id,
                'avatar': User.objects.filter(username=messages.sender)
            }
        if messages.message_type == 3:
            a = {
                'id': messages.id,
                'msg':
                    '您被移除了' +
                    str(Team.objects.get(team_id=messages.team_id).team_name) + "的管理员职位",
                'sender': messages.sender, 'send_time': messages.send_time,
                'message_type': messages.message_type, 'team_id': messages.team_id,
                'avatar': User.objects.filter(username=messages.sender)
            }
        ans_list.append(a)
    return JsonResponse({'status_code': 1, 'ans_list': ans_list})


# 0是被踢出团队 1是被邀请加入团队 2是被设为管理员 3是被取消管理员


@csrf_exempt
def getTeamMessage(request):
    team_id = json.loads(request.body)['team_id']
    ans_list = []
    message_list = TeamMessage.objects.filter(team_id=team_id).order_by('-send_time')
    for messages in message_list:
        if messages.message_type == 0:
            a = {
                'id': messages.id,
                'msg':
                    str(messages.sender) + '邀请了' +
                    str(messages.receiver) + "加入了团队",
                'sender': messages.sender, 'send_time': messages.send_time,
                'message_type': messages.message_type, 'team_id': messages.team_id,
                'avatar': User.objects.filter(username=messages.sender)
            }

        if messages.message_type == 1:
            a = {
                'id': messages.id,
                'msg':
                    str(messages.sender) + '将' +
                    str(messages.receiver) + "移出了团队",
                'sender': messages.sender, 'send_time': messages.send_time,
                'message_type': messages.message_type, 'team_id': messages.team_id,
                'avatar': User.objects.filter(username=messages.sender)
            }
        if messages.message_type == 2:
            a = {
                'id': messages.id,
                'msg':
                    str(messages.sender) + '将' +
                    str(messages.receiver) + "设为了团队管理",
                'sender': messages.sender, 'send_time': messages.send_time,
                'message_type': messages.message_type, 'team_id': messages.team_id,
                'avatar': User.objects.filter(username=messages.sender)
            }
        if messages.message_type == 3:
            a = {
                'id': messages.id,
                'msg':
                    str(messages.sender) + '撤销了' +
                    str(messages.receiver) + "的团队管理",
                'sender': messages.sender, 'send_time': messages.send_time,
                'message_type': messages.message_type, 'team_id': messages.team_id,
                'avatar': User.objects.filter(username=messages.sender)
            }
        if messages.message_type == 4:
            a = {
                'id': messages.id,
                'msg':
                    str(messages.sender) + '新建了项目' +
                    str(Projectt.objects.get(project_id=messages.project_id).project_name),
                'sender': messages.sender, 'send_time': messages.send_time,
                'message_type': messages.message_type, 'team_id': messages.team_id,
                'avatar': User.objects.filter(username=messages.sender)
            }
        if messages.message_type == 5:
            a = {
                'id': messages.id,
                'msg':
                    str(messages.sender) + '删除了项目' +
                    str(messages.delete_project_name),
                'sender': messages.sender, 'send_time': messages.send_time,
                'message_type': messages.message_type, 'team_id': messages.team_id,
                'avatar': User.objects.filter(username=messages.sender)
            }
        ans_list.append(a)
    return JsonResponse({'status_code': 1, 'ans_list': ans_list})


# 0    1    2    3        4                                    5
# x邀请y加入团队，x把y踢出团队，x把y设为管理，x撤销y的管理，x新建项目,x删除项目

@csrf_exempt
def getProjectMessage(request):
    project_id = json.loads(request.body)['project_id']
    ans_list = []
    message_list = ProjectMessage.objects.filter(project_id=project_id).order_by('-send_time')
    for messages in message_list:
        if messages.message_type == 0:
            a = {
                'id': messages.id,
                'msg':
                    str(messages.sender) + '新建了文件' +
                    str(File.objects.get(file_id=messages.file_id).file_name),
                'sender': messages.sender, 'send_time': messages.send_time,
                'message_type': messages.message_type, 'team_id': messages.team_id,
                'avatar': User.objects.filter(username=messages.sender)
            }
        if messages.message_type == 1:
            a = {
                'id': messages.id,
                'msg':
                    str(messages.sender) + '删除了文件' +
                    str(messages.delete_file_name),
                'sender': messages.sender, 'send_time': messages.send_time,
                'message_type': messages.message_type, 'team_id': messages.team_id,
                'avatar': User.objects.filter(username=messages.sender)
            }
        if messages.message_type == 2:
            a = {
                'id': messages.id,
                'msg':
                    str(messages.sender) + '开放了原型设计' +
                    str(File.objects.get(file_id=messages.file_id).file_name) + '的预览',
                'sender': messages.sender, 'send_time': messages.send_time,
                'message_type': messages.message_type, 'team_id': messages.team_id,
                'avatar': User.objects.filter(username=messages.sender)
            }

        if messages.message_type == 3:
            a = {
                'id': messages.id,
                'msg':
                    str(messages.sender) + '关闭了原型设计' +
                    str(File.objects.get(file_id=messages.file_id).file_name) + '的预览',
                'sender': messages.sender, 'send_time': messages.send_time,
                'message_type': messages.message_type, 'team_id': messages.team_id,
                'avatar': User.objects.filter(username=messages.sender)
            }
        ans_list.append(a)
    return JsonResponse({'status_code': 1, 'ans_list': ans_list})

# ProjectMessage里type为0   1   2   3
# x新建了文件y，x删除了文件y，x开放文件y的预览   x关闭文件y的预览

@csrf_exempt
def agreeInvitation(request):
    username = json.loads(request.body)['username']
    team_id = json.loads(request.body)['team_id']
    message_list = PersonalMessage.objects.filter(receiver=username, team_id=team_id)
    for messages in message_list:
        new_mem_in_team = Member_in_Team()
        new_mem_in_team.username = messages.receiver
        new_mem_in_team.team_id = team_id
        new_mem_in_team.priority = 0
        new_mem_in_team.save()


@csrf_exempt
def disagreeInvitation(request):
    username = json.loads(request.body)['username']
    team_id = json.loads(request.body)['team_id']
    message_list = PersonalMessage.objects.filter(receiver=username, team_id=team_id)
    for messages in message_list:
        messages.delete()
