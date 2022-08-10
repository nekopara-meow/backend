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

# TeamMessage里type为0    1    2    3   4   5
# x邀请y加入团队，x把y踢出团队，x把y设为管理，x撤销y的管理，x新建项目  x删除项目

# ProjectMessage里type为0   1   2   3
# x新建了文件y，x删除了文件y，x开放文件y的预览  x关闭文件预览

@csrf_exempt
def getPersonalMessage(request):
    username = json.loads(request.body)['username']
    ans_list = []
    message_list = PersonalMessage.objects.filter(receiver=username).order_by('-send_time')
    for messages in message_list:
        if messages.message_type == 0:
            a = {
                'message_id': messages.message_id,
                'msg':
                    '您被移出了' +
                    str(Team.objects.get(team_id=messages.team_id).team_name),
                'sender': messages.sender, 'send_time': messages.send_time.strftime('%b-%m-%y %H:%M:%S'),
                'message_type': messages.message_type, 'team_id': messages.team_id,
                'avatar': User.objects.get(username=messages.sender).avatar
            }
        if messages.message_type == 1:
            a = {
                'message_id': messages.message_id,
                'msg':
                    str(messages.sender) + '邀请您加入' +
                    str(Team.objects.get(team_id=messages.team_id).team_name),
                'sender': messages.sender, 'send_time': messages.send_time.strftime('%b-%m-%y %H:%M:%S'),
                'message_type': messages.message_type, 'team_id': messages.team_id,
                'avatar': User.objects.get(username=messages.sender).avatar
            }
        if messages.message_type == 2:
            a = {
                'message_id': messages.message_id,
                'msg':
                    '您被设为了' +
                    str(Team.objects.get(team_id=messages.team_id).team_name) + "的管理员",
                'sender': messages.sender, 'send_time': messages.send_time.strftime('%b-%m-%y %H:%M:%S'),
                'message_type': messages.message_type, 'team_id': messages.team_id,
                'avatar': User.objects.get(username=messages.sender).avatar
            }
        if messages.message_type == 3:
            a = {
                'message_id': messages.message_id,
                'msg':
                    '您被移除了' +
                    str(Team.objects.get(team_id=messages.team_id).team_name) + "的管理员职位",
                'sender': messages.sender, 'send_time': messages.send_time.strftime('%b-%m-%y %H:%M:%S'),
                'message_type': messages.message_type, 'team_id': messages.team_id,
                'avatar': User.objects.get(username=messages.sender).avatar
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
                'message_id': messages.message_id,
                'msg':
                    '邀请了' +
                    str(messages.receiver) + "加入了团队",
                'sender': messages.sender, 'send_time': messages.send_time.strftime('%b-%m-%y %H:%M:%S'),
                'message_type': messages.message_type, 'team_id': messages.team_id,
                'avatar': User.objects.get(username=messages.sender).avatar
            }

        if messages.message_type == 1:
            a = {
                'message_id': messages.message_id,
                'msg':
                    '将' +
                    str(messages.receiver) + "移出了团队",
                'sender': messages.sender, 'send_time': messages.send_time.strftime('%b-%m-%y %H:%M:%S'),
                'message_type': messages.message_type, 'team_id': messages.team_id,
                'avatar': User.objects.get(username=messages.sender).avatar
            }
        if messages.message_type == 2:
            a = {
                'message_id': messages.message_id,
                'msg':
                    '将' +
                    str(messages.receiver) + "设为了团队管理",
                'sender': messages.sender, 'send_time': messages.send_time.strftime('%b-%m-%y %H:%M:%S'),
                'message_type': messages.message_type, 'team_id': messages.team_id,
                'avatar': User.objects.get(username=messages.sender).avatar
            }
        if messages.message_type == 3:
            a = {
                'message_id': messages.message_id,
                'msg':
                    '撤销了' +
                    str(messages.receiver) + "的团队管理",
                'sender': messages.sender, 'send_time': messages.send_time.strftime('%b-%m-%y %H:%M:%S'),
                'message_type': messages.message_type, 'team_id': messages.team_id,
                'avatar': User.objects.get(username=messages.sender).avatar
            }
        if messages.message_type == 4:
            a = {
                'message_id': messages.message_id,
                'msg':
                    '新建了项目' +
                    str(Projectt.objects.get(project_id=messages.project_id).project_name),
                'sender': messages.sender, 'send_time': messages.send_time.strftime('%b-%m-%y %H:%M:%S'),
                'message_type': messages.message_type, 'team_id': messages.team_id,
                'avatar': User.objects.get(username=messages.sender).avatar
            }
        if messages.message_type == 5:
            a = {
                'message_id': messages.message_id,
                'msg':
                    '删除了项目' +
                    str(messages.delete_project_name),
                'sender': messages.sender, 'send_time': messages.send_time.strftime('%b-%m-%y %H:%M:%S'),
                'message_type': messages.message_type, 'team_id': messages.team_id,
                'avatar': User.objects.get(username=messages.sender).avatar
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
                'message_id': messages.message_id,
                'msg':
                    '新建了文件' +
                    str(File.objects.get(file_id=messages.file_id).file_name),
                'sender': messages.username, 'send_time': messages.send_time.strftime('%b-%m-%y %H:%M:%S'),
                'message_type': messages.message_type, 'team_id': messages.team_id,
                'avatar': User.objects.get(username=messages.username).avatar
            }
        if messages.message_type == 1:
            a = {
                'message_id': messages.message_id,
                'msg':
                    '删除了文件' +
                    str(messages.delete_file_name),
                'sender': messages.username, 'send_time': messages.send_time.strftime('%b-%m-%y %H:%M:%S'),
                'message_type': messages.message_type, 'team_id': messages.team_id,
                'avatar': User.objects.get(username=messages.username).avatar
            }
        if messages.message_type == 2:
            a = {
                'message_id': messages.message_id,
                'msg':
                    '开放了原型设计' +
                    str(File.objects.get(file_id=messages.file_id).file_name) + '的预览',
                'sender': messages.username, 'send_time': messages.send_time.strftime('%b-%m-%y %H:%M:%S'),
                'message_type': messages.message_type, 'team_id': messages.team_id,
                'avatar': User.objects.get(username=messages.username).avatar
            }

        if messages.message_type == 3:
            a = {
                'message_id': messages.message_id,
                'msg':
                    '关闭了原型设计' +
                    str(File.objects.get(file_id=messages.file_id).file_name) + '的预览',
                'sender': messages.username, 'send_time': messages.send_time.strftime('%b-%m-%y %H:%M:%S'),
                'message_type': messages.message_type, 'team_id': messages.team_id,
                'avatar': User.objects.get(username=messages.username).avatar
            }
        ans_list.append(a)
    return JsonResponse({'status_code': 1, 'ans_list': ans_list})


# ProjectMessage里type为0   1   2   3
# x新建了文件y，x删除了文件y，x开放文件y的预览   x关闭文件y的预览

@csrf_exempt
def agreeInvitation(request):
    message_id = json.loads(request.body)['message_id']
    message = PersonalMessage.objects.get(message_id=message_id)
    inviter_username = PersonalMessage.objects.get(message_id=message_id).sender
    invitee_username = PersonalMessage.objects.get(message_id=message_id).receiver
    team_id = PersonalMessage.objects.get(message_id=message_id).team_id
    already_in = Member_in_Team.objects.filter(username=invitee_username, team_id=team_id)

    if already_in:
        message.delete()
        return JsonResponse({'status_code': 2, 'msg': "Invitee has been already in the team"})
    if Member_in_Team.objects.get(username=inviter_username, team_id=team_id).priority < 1:
        message.delete()
        return JsonResponse({'status_code': 3, 'msg': "Inviter doesn't have the priority"})

    new_team_message = TeamMessage()
    new_team_message.message_type = 0
    new_team_message.team_id = message.team_id
    new_team_message.sender = message.sender
    new_team_message.receiver = message.receiver
    new_team_message.send_time = datetime.datetime.now().strftime('%b-%m-%y %H:%M:%S')
    new_team_message.save()
    # 发消息

    new_mem_in_team = Member_in_Team()
    new_mem_in_team.username = message.receiver
    new_mem_in_team.team_id = message.team_id
    new_mem_in_team.priority = 0
    new_mem_in_team.save()
    # 加入团队
    message.delete()
    return JsonResponse({'status_code': 1, 'msg': "加入成功"})


@csrf_exempt
def disagreeInvitation(request):
    message_id = json.loads(request.body)['message_id']
    PersonalMessage.objects.get(message_id=message_id).delete()
    # 删除邀请记录
    return JsonResponse({'status_code': 1, 'msg': "拒绝成功"})


@csrf_exempt
def search_all(request):
    if request.method == 'POST':
        username = json.loads(request.body)['username']
        keyword = json.loads(request.body)['keyword']
        team_ids = []
        project_ids = []
        if 'team_ids' in json.loads(request.body):
            team_ids = json.loads(request.body)['team_ids']
        else:
            teams = Member_in_Team.objects.filter(username=username).order_by('team_id')
            for team in teams:
                team_ids.append(team.team_id)
        project_infos = []
        projects = Projectt.objects.filter(team_id__in=team_ids).order_by('team_id')
        for project in projects:
            project_ids.append(project.project_id)
            if keyword in project.project_name:
                project_info = {'project_name': project.project_name, 'brief_intro': project.brief_intro,
                                'create_time': project.create_time, 'team_name': project.team_name,
                                'team_id': project.team_id , 'project_id': project.project_id
                                }
                project_infos.append(project_info)
        files = File.objects.filter(project_id__in=project_ids, file_name__contains=keyword).order_by('file_id')
        file_infos = []
        for file in files:
            file_info = {'file_id': file.file_id, 'update_time': file.update_time,
                         'file_type': file.file_type, 'creator': file.creator,
                         'file_name': file.file_name, 'file_content': file.file_url,
                         'name_url': file.name_url, 'project_id': file.project_id}
            file_infos.append(file_info)
        users = User.objects.filter(username__contains=keyword)
        user_infos = []
        for user in users:
            user_info = {'username': user.username, 'nickname': user.nickname,
                         'email': user.email, 'brief_intro': user.brief_intro,
                         'avatar':user.avatar}
            user_infos.append(user_info)
        return JsonResponse({'status_code': 1, 'project_infos': project_infos, 'file_infos': file_infos,
                             'user_infos': user_infos})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误!'})
