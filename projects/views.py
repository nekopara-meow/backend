import json
import re
from team.models import Team
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pytz import utc
from projects.models import Projectt, File
from interact.models import Member_in_Team
import datetime
# Create your views here.

@csrf_exempt
def clear(request):
    pros = Projectt.objects.all()
    for projects in pros:
        projects.delete()

@csrf_exempt
def establish(request):
    username = json.loads(request.body)['username']
    team_id = json.loads(request.body)['team_id']
    brief_intro = json.loads(request.body)['brief_intro']
    already_in = Member_in_Team.objects.get(username=username, team_id=team_id)
    if already_in is None:
        return JsonResponse({'status_code': 2, 'msg': "该用户不在团队中，无权操作"})
    else:
        project = Projectt()
        project.team_id = team_id
        project.creator = username
        project.create_time = datetime.datetime.now()
        project.brief_intro = brief_intro
        project.save()
        return JsonResponse({'status_code': 1, 'msg': "新建项目成功"})

@csrf_exempt
def delete(request):
    username = json.loads(request.body)['username']
    project_id = json.loads(request.body)['project_id']
    project = Projectt.objects.get(project_id=project_id)
    already_in = Member_in_Team.objects.get(username=username, team_id=project.team_id)
    if already_in is None:
        return JsonResponse({'status_code': 2, 'msg': "该用户不在团队中，无权操作"})
    else:
        project.delete()
        return JsonResponse({'status_code': 1, 'msg': "删除成功"})

@csrf_exempt
def rename(request):
    username = json.loads(request.body)['username']
    project_id = json.loads(request.body)['project_id']
    new_name = json.loads(request.body)['new_name']
    project = Projectt.objects.get(project_id=project_id)
    already_in = Member_in_Team.objects.get(username=username, team_id=project.team_id)
    if already_in is None:
        return JsonResponse({'status_code': 2, 'msg': "该用户不在团队中，无权操作"})
    else:
        project.project_name = new_name
        return JsonResponse({'status_code': 1, 'msg': "重命名成功"})

@csrf_exempt
def uploadFile(request):
    username = json.loads(request.body)['username']
    file_name = json.loads(request.body)['file_name']
    project_id = json.loads(request.body)['project_id']
    file_type = json.loads(request.body)['file_type']
    file_content = json.loads(request.body)['file_content']
    project = Projectt.objects.get(project_id=project_id)
    already_in = Member_in_Team.objects.get(username=username, team_id=project.team_id)
    if already_in is None:
        return JsonResponse({'status_code': 2, 'msg': "该用户不在团队中，无权操作"})
    else:
        file = File()
        file.file_name = file_name
        file.file_type = file_type
        file.file_content = file_content
        file.project_id = project_id
        file.creator = username
        file.save()
        return JsonResponse({'status_code': 1, 'msg': "上传文件成功"})

@csrf_exempt
def viewFilesInProject(request):
    username = json.loads(request.body)['username']
    project_id = json.loads(request.body)['project_id']
    project = Projectt.objects.get(project_id=project_id)
    already_in = Member_in_Team.objects.get(username=username, team_id=project.team_id)
    if already_in is None:
        return JsonResponse({'status_code': 2, 'msg': "该用户不在团队中，无权操作"})
    else:
        ans_list = []
        file_list = File.objects.filter(project_id=project_id)
        for files in file_list:
            a = {
                'project_id': files.project_id, 'creator': files.creator,
                'file_id': files.file_id, 'file_type': files.file_type,
                'file_content': files.file_content
            }
            ans_list.append(a)
        return JsonResponse({'status_code': 1, 'ans_list': ans_list})

@csrf_exempt
def viewUMLsInProject(request):
    username = json.loads(request.body)['username']
    project_id = json.loads(request.body)['project_id']
    project = Projectt.objects.get(project_id=project_id)
    already_in = Member_in_Team.objects.get(username=username, team_id=project.team_id)
    if already_in is None:
        return JsonResponse({'status_code': 2, 'msg': "该用户不在团队中，无权操作"})
    else:
        ans_list = []
        file_list = File.objects.filter(project_id=project_id, file_type=0)
        for files in file_list:
            a = {
                'project_id': files.project_id, 'creator': files.creator,
                'file_id': files.file_id, 'file_type': files.file_type,
                'file_content': files.file_content
            }
            ans_list.append(a)
        return JsonResponse({'status_code': 1, 'ans_list': ans_list})

@csrf_exempt
def viewDesignsInProject(request):
    username = json.loads(request.body)['username']
    project_id = json.loads(request.body)['project_id']
    project = Projectt.objects.get(project_id=project_id)
    already_in = Member_in_Team.objects.get(username=username, team_id=project.team_id)
    if already_in is None:
        return JsonResponse({'status_code': 2, 'msg': "该用户不在团队中，无权操作"})
    else:
        ans_list = []
        file_list = File.objects.filter(project_id=project_id, file_type=1)
        for files in file_list:
            a = {
                'project_id': files.project_id, 'creator': files.creator,
                'file_id': files.file_id, 'file_type': files.file_type,
                'file_content': files.file_content
            }
            ans_list.append(a)
        return JsonResponse({'status_code': 1, 'ans_list': ans_list})

@csrf_exempt
def viewTextsInProject(request):
    username = json.loads(request.body)['username']
    project_id = json.loads(request.body)['project_id']
    project = Projectt.objects.get(project_id=project_id)
    already_in = Member_in_Team.objects.get(username=username, team_id=project.team_id)
    if already_in is None:
        return JsonResponse({'status_code': 2, 'msg': "该用户不在团队中，无权操作"})
    else:
        ans_list = []
        file_list = File.objects.filter(project_id=project_id, file_type=2)
        for files in file_list:
            a = {
                'project_id': files.project_id, 'creator': files.creator,
                'file_id': files.file_id, 'file_type': files.file_type,
                'file_content': files.file_content
            }
            ans_list.append(a)
        return JsonResponse({'status_code': 1, 'ans_list': ans_list})
