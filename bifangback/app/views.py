from cmdb.models import App
from cmdb.models import Project
from cmdb.models import GitTb
from .serializers import AppSerializer
from rest_framework.generics import ListAPIView
from rest_framework.generics import CreateAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import UpdateAPIView
from rest_framework.generics import DestroyAPIView
from utils.ret_code import *
from .filters import AppFilter


class AppListView(ListAPIView):
    queryset = App.objects.all()
    serializer_class = AppSerializer
    filter_class = AppFilter

    def get(self, request, *args, **kwargs):
        res = super().get(self, request, *args, **kwargs)
        return_dict = build_ret_data(OP_SUCCESS, res.data)
        return render_json(return_dict)


class AppCreateView(CreateAPIView):
    serializer_class = AppSerializer

    def post(self, request):
        """
        {
            "name": "appA",
            "cn_name":"A应用",
            "description": "这是一个A应用",
            "app_id": 4325,
            "git_app_id": 2,
            "git_id": 1,
            "project_id": 6,
            "git_trigger_token": "i98sdfasdf935345",
            "build_script": "script/build.sh",
            "deploy_script": "script/bifang.sh",
            "zip_package_name": "go-demo.zip",
            "service_port": 8080,
            "service_username": "root",
            "service_group": "root"
        }
        """
        req_data = request.data
        data = dict()
        data['name'] = req_data['name']
        data['description'] = req_data['description']
        data['cn_name'] = req_data['cn_name']
        data['app_id'] = req_data['app_id']
        data['git_app_id'] = req_data['git_app_id']
        # 外键关联
        data['git'] = req_data['git_id']
        data['project'] = req_data['project_id']
        # 普通字段
        data['git_trigger_token'] = req_data['git_trigger_token']
        data['build_script'] = req_data['build_script']
        data['deploy_script'] = req_data['deploy_script']
        data['zip_package_name'] = req_data['zip_package_name']
        data['service_port'] = req_data['service_port']
        data['service_username'] = req_data['service_username']
        data['service_group'] = req_data['service_group']
        # 从drf的request中获取用户(对django的request作了扩展的)
        data['create_user'] = request.user.id
        serializer = AppSerializer(data=data)
        if serializer.is_valid() is False:
            return_dict = build_ret_data(THROW_EXP, str(serializer.errors))
            return render_json(return_dict)
        data = serializer.validated_data
        App.objects.create(**data)
        return_dict = build_ret_data(OP_SUCCESS, serializer.data)
        return render_json(return_dict)


class AppRetrieveView(RetrieveAPIView):
    queryset = App.objects.all()
    serializer_class = AppSerializer

    def get(self, request, *args, **kwargs):
        res = super().get(self, request, *args, **kwargs)
        return_dict = build_ret_data(OP_SUCCESS, res.data)
        return render_json(return_dict)


class AppUpdateView(UpdateAPIView):
    """
    url获取pk,修改时指定序列化类和query_set
    """
    serializer_class = AppSerializer
    queryset = App.objects.all()

    # 前端使用patch方法，到达这里
    def patch(self, request, *args, **kwargs):
        req_data = request.data
        pid = req_data['id']
        name = req_data['name']
        cn_name = req_data['cn_name']
        description = req_data['description']
        app_id = req_data['app_id']
        # 这样更新，可以把那些update_date字段自动更新，而使用filter().update()则是不会
        try:
            _a = App.objects.get(id=pid)
            _a.name = name
            _a.cn_name = cn_name
            _a.description = description
            _a.app_id = app_id
            _a.save()
            return_dict = build_ret_data(OP_SUCCESS, str(req_data))
            return render_json(return_dict)
        except Exception as e:
            print(e)
            return_dict = build_ret_data(THROW_EXP, str(e))
            return render_json(return_dict)


class AppDestroyView(DestroyAPIView):
    queryset = App.objects.all()

    def destroy(self, request, *args, **kwargs):
        try:
            res = super().destroy(self, request, *args, **kwargs)
            return_dict = build_ret_data(OP_SUCCESS, str(res))
            return render_json(return_dict)
        except Exception as e:
            print(e)
            return_dict = build_ret_data(THROW_EXP, str(e))
            return render_json(return_dict)
