import datetime
import random
import string
from cmdb.models import App
from cmdb.models import Release
from cmdb.models import ReleaseStatus
from cmdb.models import Action
from .serializers import ReleaseSerializer
from .serializers import ReleaseCreateSerializer
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import CreateAPIView
from rest_framework.generics import UpdateAPIView
from rest_framework.generics import DestroyAPIView
from utils.ret_code import *
from .filters import ReleaseFilter
from utils.permission import is_right
from utils.write_history import write_release_history


class ReleaseListView(ListAPIView):
    queryset = Release.objects.all()
    serializer_class = ReleaseSerializer
    filter_class = ReleaseFilter

    def get(self, request, *args, **kwargs):
        res = super().get(self, request, *args, **kwargs)
        return_dict = build_ret_data(OP_SUCCESS, res.data)
        return render_json(return_dict)


class ReleaseCreateView(CreateAPIView):
    serializer_class = ReleaseCreateSerializer

    def post(self, request):
        """
        {
            "description": "这是一个测试发布单",
            "app_id": 1,
            "git_branch": "master"
        }
        """
        req_data = request.data
        user = request.user
        app_id = req_data['app_id']

        """
        # 前端开发完成后开启权限测试
        action = Action.objects.get(name='Create')
        if not is_right(app_id, action.id, user):
            return_dict = build_ret_data(THROW_EXP, '你无权在此应用下新建发布单！')
            return render_json(return_dict)
        """

        data = dict()
        random_letter = ''.join(random.sample(string.ascii_letters, 2))
        name = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + random_letter.upper()
        deploy_status_name = 'Create'
        deploy_status = ReleaseStatus.objects.get(name=deploy_status_name)
        data['name'] = name
        data['description'] = req_data['description']
        data['git_branch'] = req_data['git_branch']
        data['app'] = app_id
        data['deploy_status'] = deploy_status.id

        # 从drf的request中获取用户(对django的request作了扩展的)
        data['create_user'] = user.id
        serializer = ReleaseCreateSerializer(data=data)
        if serializer.is_valid() is False:
            return_dict = build_ret_data(THROW_EXP, str(serializer.errors))
            return render_json(return_dict)
        data = serializer.validated_data
        release = Release.objects.create(**data)
        write_release_history(release_name=release.name,
                              env_name=None,
                              deploy_status_name=deploy_status_name,
                              deploy_type=None,
                              log='Create',
                              create_user=user)
        return_dict = build_ret_data(OP_SUCCESS, serializer.data)
        return render_json(return_dict)


class ReleaseRetrieveView(RetrieveAPIView):
    queryset = Release.objects.all()
    serializer_class = ReleaseSerializer

    def get(self, request, *args, **kwargs):
        res = super().get(self, request, *args, **kwargs)
        return_dict = build_ret_data(OP_SUCCESS, res.data)
        return render_json(return_dict)


class ReleaseUpdateView(UpdateAPIView):
    """
    url获取pk,修改时指定序列化类和query_set
    """
    serializer_class = ReleaseSerializer
    queryset = Release.objects.all()

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


class ReleaseDestroyView(DestroyAPIView):
    queryset = Release.objects.all()

    def destroy(self, request, *args, **kwargs):
        try:
            res = super().destroy(self, request, *args, **kwargs)
            return_dict = build_ret_data(OP_SUCCESS, str(res))
            return render_json(return_dict)
        except Exception as e:
            print(e)
            return_dict = build_ret_data(THROW_EXP, str(e))
            return render_json(return_dict)
