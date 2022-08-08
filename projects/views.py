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
    project_name = json.loads(request.body)['project_name']
    brief_intro = json.loads(request.body)['brief_intro']
    already_in = Member_in_Team.objects.filter(username=username, team_id=team_id)
    if already_in is None:
        return JsonResponse({'status_code': 2, 'msg': "该用户不在团队中，无权操作"})
    else:
        project = Projectt()
        project.team_id = team_id
        project.project_name = project_name
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
    already_in = Member_in_Team.objects.filter(username=username, team_id=project.team_id)
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
    already_in = Member_in_Team.objects.filter(username=username, team_id=project.team_id)
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
    already_in = Member_in_Team.objects.filter(username=username, team_id=project.team_id)
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
    already_in = Member_in_Team.objects.filter(username=username, team_id=project.team_id)
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
    already_in = Member_in_Team.objects.filter(username=username, team_id=project.team_id)
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
    already_in = Member_in_Team.objects.filter(username=username, team_id=project.team_id)
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
    already_in = Member_in_Team.objects.filter(username=username, team_id=project.team_id)
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


@csrf_exempt
def loadXML(request):
    if request.method == 'POST':
        uml_id = json.loads(request.body)['uml_id']
        file = File.objects.get(file_id=uml_id)
        url = file.file_url
        return JsonResponse({'status_code': 1, 'uml_url': url, 'message': '获取成功'})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误'})


@csrf_exempt
def saveXML(request):
    if request.method == 'POST':
        uml_id = json.loads(request.body)['uml_id']
        uml_url = json.loads(request.body)['uml_url']

        file = File.objects.get(file_id=uml_id)
        file.file_url = uml_url
        file.save()
        return JsonResponse({'status_code': 1, 'message': '保存成功'})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误'})


@csrf_exempt
def newXML(request):
    if request.method == 'POST':
        file = File()
        print(json.loads(request.body))
        username = json.loads(request.body)['username']
        project_id = json.loads(request.body)['project_id']
        uml_name = json.loads(request.body)['uml_name']
        file.file_name = uml_name
        file.file_type = 0
        file.project_id = project_id
        file.creator = username
        file.save()
        return JsonResponse({'status_code': 1, 'uml_id': file.file_id, 'message': '新建成功'})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误'})


@csrf_exempt
def loadDOC(request):
    if request.method == 'POST':
        doc_id = json.loads(request.body)['doc_id']
        file = File.objects.get(file_id=doc_id)
        url = file.file_url
        return JsonResponse({'status_code': 1, 'doc_url': url, 'message': '获取成功'})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误'})


@csrf_exempt
def saveDOC(request):
    if request.method == 'POST':
        doc_id = json.loads(request.body)['doc_id']
        doc_url = json.loads(request.body)['doc_url']

        file = File.objects.get(file_id=doc_id)
        file.file_url = doc_url
        file.save()
        return JsonResponse({'status_code': 1, 'message': '保存成功'})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误'})


@csrf_exempt
def newDOC(request):
    if request.method == 'POST':
        file = File()
        username = json.loads(request.body)['username']
        project_id = json.loads(request.body)['project_id']
        doc_name = json.loads(request.body)['doc_name']
        file.file_name = doc_name
        file.file_type = 0
        file.project_id = project_id
        file.creator = username
        file.save()
        return JsonResponse({'status_code': 1, 'doc_id': file.file_id, 'message': '新建成功'})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误'})


@csrf_exempt
def del_file_by_id(request):
    if request.method == 'POST':
        file_id = json.loads(request.body)['file_id']
        file = File.objects.get(file_id=file_id)
        file.delete()
        return JsonResponse({'status_code': 1, 'message': '删除成功!'})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误!'})


@csrf_exempt
def rename_file_by_id(request):
    if request.method == 'POST':
        file_id = json.loads(request.body)['file_id']
        new_name = json.loads(request.bode)['new_file_name']
        file = File.objects.get(file_id=file_id)
        file.file_name = new_name
        file.save()
        return JsonResponse({'status_code': 1, 'message': '重命名成功！'})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误'})
