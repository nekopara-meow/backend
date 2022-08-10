import json
import re
from team.models import Team
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pytz import utc
from projects.models import Projectt, File, FileBin, ProjectBin
from interact.models import Member_in_Team
import datetime
from interact.models import TeamMessage, ProjectMessage
# Create your views here.

XML = 0
DOC = 1
DSN = 2


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
    team_name = Team.objects.get(team_id=team_id).team_name
    already_in = Member_in_Team.objects.filter(username=username, team_id=team_id)
    if already_in is None:
        return JsonResponse({'status_code': 2, 'msg': "该用户不在团队中，无权操作"})
    else:
        project = Projectt()
        project.team_id = team_id
        project.project_name = project_name
        project.creator = username
        project.create_time = datetime.datetime.now()
        project.update_time = datetime.datetime.now()
        project.brief_intro = brief_intro
        project.team_name = team_name
        project.save()

        new_team_message = TeamMessage()
        new_team_message.message_type = 4
        new_team_message.team_id = team_id
        new_team_message.sender = username
        new_team_message.project_id = project.project_id
        new_team_message.send_time = datetime.datetime.now()
        new_team_message.save()
        # team message


        return JsonResponse({'status_code': 1, 'project_id':project.project_id, 'msg': "新建项目成功"})


@csrf_exempt
def delete(request):
    username = json.loads(request.body)['username']
    project_id = json.loads(request.body)['project_id']
    project = Projectt.objects.get(project_id=project_id)
    already_in = Member_in_Team.objects.filter(username=username, team_id=project.team_id)
    if already_in is None:
        return JsonResponse({'status_code': 2, 'msg': "该用户不在团队中，无权操作"})
    else:
        project.deleted = True
        projectbin = ProjectBin()
        projectbin.project_id = project_id
        projectbin.team_id = project.team_id
        projectbin.delete_time = datetime.datetime.now()
        projectbin.save()
        project.save()

        new_team_message = TeamMessage()
        new_team_message.message_type = 5
        new_team_message.team_id = Projectt.objects.get(project_id=project_id).team_id
        new_team_message.sender = username
        new_team_message.project_id = project_id
        new_team_message.send_time = datetime.datetime.now()
        new_team_message.delete_project_name = project.project_name
        new_team_message.save()
        # team message
        return JsonResponse({'status_code': 1, 'msg': "删除成功,已放入回收站"})





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
        project.update_time = datetime.datetime.now()
        project.save()
        return JsonResponse({'status_code': 1, 'msg': "重命名成功"})


@csrf_exempt
def uploadFile(request):
    username = json.loads(request.body)['username']
    file_name = json.loads(request.body)['file_name']
    project_id = json.loads(request.body)['project_id']
    file_type = json.loads(request.body)['file_type']
    project = Projectt.objects.get(project_id=project_id)
    already_in = Member_in_Team.objects.filter(username=username, team_id=project.team_id)
    if already_in is None:
        return JsonResponse({'status_code': 2, 'msg': "该用户不在团队中，无权操作"})
    else:
        file = File()
        file.file_name = file_name
        file.file_type = file_type
        file.project_id = project_id
        file.creator = username
        file.update_time = datetime.datetime.now()
        file.save()
        project.update_time = datetime.datetime.now()

        return JsonResponse({'status_code': 1, 'msg': "上传文件成功"})


@csrf_exempt
def viewFilesInProject(request):
    username = json.loads(request.body)['username']
    project_id = json.loads(request.body)['project_id']
    if 'deleted' in json.loads(request.body):
        deleted = True
    else:
        deleted = False
    project = Projectt.objects.get(project_id=project_id)
    already_in = Member_in_Team.objects.filter(username=username, team_id=project.team_id)
    if already_in is None:
        return JsonResponse({'status_code': 2, 'msg': "该用户不在团队中，无权操作"})
    else:
        ans_list = []
        file_list = File.objects.filter(project_id=project_id, deleted=deleted)
        for files in file_list:
            a = {
                'project_id': files.project_id, 'creator': files.creator,
                'file_id': files.file_id, 'file_type': files.file_type,
                'file_name': files.file_name, 'file_content': files.file_url,
                'update_time': files.update_time.strftime('%b-%m-%y %H:%M:%S'),
            }
            ans_list.append(a)
        return JsonResponse({'status_code': 1, 'ans_list': ans_list})


@csrf_exempt
def viewUMLsInProject(request):
    username = json.loads(request.body)['username']
    project_id = json.loads(request.body)['project_id']
    if 'deleted' in json.loads(request.body):
        deleted = True
    else:
        deleted = False
    project = Projectt.objects.get(project_id=project_id)
    already_in = Member_in_Team.objects.filter(username=username, team_id=project.team_id)
    if already_in is None:
        return JsonResponse({'status_code': 2, 'msg': "该用户不在团队中，无权操作"})
    else:
        ans_list = []
        file_list = File.objects.filter(project_id=project_id, file_type=XML, deleted=deleted)
        for files in file_list:
            a = {
                'project_id': files.project_id, 'creator': files.creator,
                'file_id': files.file_id, 'file_type': files.file_type,
                'file_name': files.file_name, 'file_content': files.file_url,
                'update_time': files.update_time.strftime('%b-%m-%y %H:%M:%S'),
            }
            ans_list.append(a)
        return JsonResponse({'status_code': 1, 'ans_list': ans_list})


@csrf_exempt
def viewDesignsInProject(request):
    username = json.loads(request.body)['username']
    project_id = json.loads(request.body)['project_id']
    if 'deleted' in json.loads(request.body):
        deleted = True
    else:
        deleted = False
    project = Projectt.objects.get(project_id=project_id)
    already_in = Member_in_Team.objects.filter(username=username, team_id=project.team_id)
    if already_in is None:
        return JsonResponse({'status_code': 2, 'msg': "该用户不在团队中，无权操作"})
    else:
        ans_list = []
        file_list = File.objects.filter(project_id=project_id, file_type=DSN, deleted=deleted)
        for files in file_list:
            a = {
                'project_id': files.project_id, 'creator': files.creator,
                'file_id': files.file_id, 'file_type': files.file_type,
                'file_name': files.file_name, 'file_content': files.file_url,
                'update_time': files.update_time.strftime('%b-%m-%y %H:%M:%S'), 'name_url': files.name_url
            }
            ans_list.append(a)
        return JsonResponse({'status_code': 1, 'ans_list': ans_list})


@csrf_exempt
def viewTextsInProject(request):
    username = json.loads(request.body)['username']
    project_id = json.loads(request.body)['project_id']
    if 'deleted' in json.loads(request.body):
        deleted = True
    else:
        deleted = False
    project = Projectt.objects.get(project_id=project_id)
    already_in = Member_in_Team.objects.filter(username=username, team_id=project.team_id)
    if already_in is None:
        return JsonResponse({'status_code': 2, 'msg': "该用户不在团队中，无权操作"})
    else:
        ans_list = []
        file_list = File.objects.filter(project_id=project_id, file_type=DOC, deleted=deleted)
        for files in file_list:
            a = {
                'project_id': files.project_id, 'creator': files.creator,
                'file_id': files.file_id, 'file_type': files.file_type,
                'file_name': files.file_name, 'file_content': files.file_url,
                'update_time': files.update_time.strftime('%b-%m-%y %H:%M:%S'),
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
        file.update_time = datetime.datetime.now()
        file.save()
        return JsonResponse({'status_code': 1, 'message': '保存成功'})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误'})


@csrf_exempt
def newXML(request):
    if request.method == 'POST':
        file = File()
        username = json.loads(request.body)['username']
        project_id = json.loads(request.body)['project_id']
        uml_name = json.loads(request.body)['uml_name']
        file.file_name = uml_name
        file.file_type = 0
        file.project_id = project_id
        file.creator = username
        file.save()

        project = Projectt.objects.get(project_id=project_id)
        project.update_time = datetime.datetime.now()
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
        file.update_time = datetime.datetime.now()
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
        file.file_type = 1
        file.project_id = project_id
        file.creator = username
        file.save()

        return JsonResponse({'status_code': 1, 'doc_id': file.file_id, 'message': '新建成功'})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误'})


@csrf_exempt
def load_axure(request):
    if request.method == 'POST':
        doc_id = json.loads(request.body)['axure_id']
        file = File.objects.get(file_id=doc_id)
        url = file.file_url
        url2 = file.name_url
        return JsonResponse({'status_code': 1, 'axure_url': url, 'name_url': url2, 'message': '获取成功'})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误'})


@csrf_exempt
def save_axure(request):
    if request.method == 'POST':
        axure_id = json.loads(request.body)['axure_id']
        axure_url = json.loads(request.body)['axure_url']
        name_url = json.loads(request.body)['name_url']
        file = File.objects.get(file_id=axure_id)
        file.file_url = axure_url
        file.name_url = name_url
        file.update_time = datetime.datetime.now()

        file.save()
        return JsonResponse({'status_code': 1, 'message': '保存成功'})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误'})


@csrf_exempt
def new_axure(request):
    if request.method == 'POST':
        file = File()
        username = json.loads(request.body)['username']
        project_id = json.loads(request.body)['project_id']
        axure_name = json.loads(request.body)['axure_name']
        file.file_name = axure_name
        file.file_type = DSN
        file.project_id = project_id
        file.creator = username
        file.save()
        return JsonResponse({'status_code': 1, 'axure_id': file.file_id, 'message': '新建成功'})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误'})


@csrf_exempt
def del_file_by_id(request):
    if request.method == 'POST':
        file_id = json.loads(request.body)['file_id']
        file = File.objects.get(file_id=file_id)
        file.deleted = True
        file.save()
        filebin = FileBin()
        filebin.project_id = file.project_id
        filebin.file_id = file_id
        filebin.delete_time = datetime.datetime.now()
        filebin.save()
        return JsonResponse({'status_code': 1, 'message': '删除成功!'})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误!'})


@csrf_exempt
def rename_file_by_id(request):
    if request.method == 'POST':
        file_id = json.loads(request.body)['file_id']
        new_name = json.loads(request.body)['new_file_name']
        file = File.objects.get(file_id=file_id)
        file.file_name = new_name
        file.update_time = datetime.datetime.now()
        file.save()
        return JsonResponse({'status_code': 1, 'message': '重命名成功！'})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误'})


@csrf_exempt
def get_projects_by_user(request):
    if request.method == 'POST':
        username = json.loads(request.body)['username']
        teams = Member_in_Team.objects.filter(username=username)
        project_infos = []
        if teams:
            for team in teams:
                team_id = team.team_id
                projects = Projectt.objects.filter(team_id=team_id)
                if projects:
                    for project in projects:
                        project_info = {'project_id': project.project_id, 'project_name': project.project_name,
                                        'brief_intro': project.brief_intro, 'team_name': project.team_name}
                        project_infos.append(project_info)
        return JsonResponse({'status_code': 1, 'projects': project_infos})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误!'})


@csrf_exempt
def get_files_by_project(request):
    if request.method == 'POST':
        project_id = json.loads(request.body)['project_id']
        files = File.objects.filter(project_id=project_id, file_type=DOC)
        file_infos = []
        if files:
            for file in files:
                file_info = {
                    'project_id': file.project_id, 'creator': file.creator,
                    'file_id': file.file_id, 'file_type': file.file_type,
                    'file_name': file.file_name, 'file_content': file.file_url,
                    'update_time': file.update_time.strftime('%b-%m-%y %H:%M:%S'),
                }
                file_infos.append(file_info)
        return JsonResponse({'status_code': 1, 'file_infos': file_infos})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误!'})


@csrf_exempt
def get_files_by_user(request):
    if request.method == 'POST':
        username = json.loads(request.body)['username']
        teams = Member_in_Team.objects.filter(username=username)
        file_infos = []
        if teams:
            for team in teams:
                team_id = team.team_id
                projects = Projectt.objects.filter(team_id=team_id)
                if projects:
                    for project in projects:
                        files = File.objects.filter(project_id=project.project_id, file_type=DOC)
                        if files:
                            for file in files:
                                file_info = {
                                    'project_id': file.project_id, 'creator': file.creator,
                                    'file_id': file.file_id, 'file_type': file.file_type,
                                    'file_name': file.file_name, 'file_content': file.file_url,
                                    'update_time': file.update_time.strftime('%b-%m-%y %H:%M:%S'), 'team_name': project.team_name,
                                }
                                file_infos.append(file_info)
        return JsonResponse({'status_code': 1, 'team_projects': file_infos})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误'})


@csrf_exempt
def get_files_by_creator(request):
    if request.method == 'POST':
        creator = json.loads(request.body)['creator']
        username = creator
        teams = Member_in_Team.objects.filter(username=username)
        file_infos = []
        project_files = []
        if teams:
            for team in teams:
                team_id = team.team_id
                projects = Projectt.objects.filter(team_id=team_id)
                if projects:
                    for project in projects:
                        files = File.objects.filter(project_id=project.project_id, creator=creator, file_type=DOC)
                        if files:
                            for file in files:
                                file_info = {
                                    'project_id': file.project_id, 'creator': file.creator,
                                    'file_id': file.file_id, 'file_type': file.file_type,
                                    'file_name': file.file_name, 'file_content': file.file_url,
                                    'update_time': file.update_time.strftime('%b-%m-%y %H:%M:%S'), 'team_name': project.team_name,
                                }
                                file_infos.append(file_info)
                            project_files.append(file_infos)
        return JsonResponse({'status_code': 1, 'team_projects': project_files})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误'})


@csrf_exempt
def completely_delete_file_by_id(request):
    if request.method == 'POST':
        file_id = json.loads(request.body)['file_id']
        file_bin = FileBin.objects.get(file_id=file_id)
        file = File.objects.get(file_id=file_id)
        file_bin.delete()
        file.delete()
        return JsonResponse({'status_code': 1, 'message': '删除成功!'})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误!'})


@csrf_exempt
def recover_file_by_id(request):
    if request.method == 'POST':
        file_id = json.loads(request.body)['file_id']
        file = File.objects.get(file_id=file_id)
        file_bin = FileBin.objects.get(file_id=file_id)
        file.deleted = False
        file.save()
        file_bin.delete()
        return JsonResponse({'status_code': 1, 'message': '恢复成功!'})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误!'})


@csrf_exempt
def completely_delete_project_by_id(request):
    if request.method == 'POST':
        project_id = json.loads(request.body)['project_id']
        project = Projectt.objects.get(project_id=project_id)
        project_bin = ProjectBin.objects.get(project_id=project_id)
        project_bin.delete()
        project.delete()
        return JsonResponse({'status_code': 1, 'message': '删除项目成功!'})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误!'})


@csrf_exempt
def recover_project_by_id(request):
    if request.method == 'POST':
        project_id = json.loads(request.body)['project_id']
        project = Projectt.objects.get(project_id=project_id)
        project_bin = ProjectBin.objects.get(project_id=project_id)
        project.deleted = False
        project_bin.delete()
        project.save()
        return JsonResponse({'status_code': 1, 'message': '恢复项目成功!'})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误!'})

@csrf_exempt
def update_project_info(request):
    if request.method == 'POST':
        project_id = json.loads(request.body)['project_id']
        brief_intro = json.loads(request.body)['brief_intro']
        project_name = json.loads(request.body)['project_name']
        project = Projectt.objects.get(project_id=project_id)
        project.project_name = project_name
        project.brief_intro = brief_intro
        project.update_time = datetime.datetime.now()
        project.save()
        return JsonResponse({'status_code': 1, 'message': '更新成功!'})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误!'})

@csrf_exempt
def viewProject(request):
    if request.method == 'POST':
        project_id = json.loads(request.body)['project_id']
        project = Projectt.objects.get(project_id=project_id)
        return JsonResponse({
            'status_code': 1, 'message': '访问成功!',
            'brief_intro': project.brief_intro, 'create_time': project.create_time.strftime('%b-%m-%y %H:%M:%S'),
            'update_time': project.update_time.strftime('%b-%m-%y %H:%M:%S'), 'creator': project.creator,
            'project_name': project.project_name,
            'team_name': Team.objects.get(team_id=project.team_id).team_name
            })
    return JsonResponse({'status_code': -1, 'message': '请求方式错误!'})
