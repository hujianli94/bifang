import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bifangback.settings")
django.setup()

from django.conf import settings
from cmdb.models import App
from utils.gitlab import gitlab_trigger

app = App.objects.get(name='go-demo')

git_url = app.git.git_url
git_access_token = app.git.git_token
git_trigger_token = app.git_trigger_token
project_id = app.git_app_id

app_name = app.name
release = '202101090245XX'
git_branch = 'master'
build_script = app.build_script
deploy_script = app.deploy_script
file_up_server = settings.FILE_UP_SERVER


job_pipeline = gitlab_trigger(git_url, git_access_token,
                              project_id, app_name, release,
                              git_branch, git_trigger_token,
                              build_script, deploy_script, file_up_server)
print(job_pipeline)
print(job_pipeline.id)
print(job_pipeline.status)
print(job_pipeline.ref)
print(job_pipeline.web_url)
print(job_pipeline.duration)
