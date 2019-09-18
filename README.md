# flask oauth2 server demo

# 快速开始

Windows PowerShell：

```PowerShell
# PowerShell
pipenv install
pipenv shell
flask initdb
flask createsuperuser
flask run
```

禁用 authlib 检查 https，`AUTHLIB_INSECURE_TRANSPORT=1`已经写在`.flaskenv`文件里。

```bash
# bash
# disable check https (DO NOT SET THIS IN PRODUCTION)
$ export AUTHLIB_INSECURE_TRANSPORT=1
```

# 使用步骤

创建一个OAuth2Client：

- Client Name: Hi
- Client URI: https://authlib.org/
- Allowed Scope: profile
- Redirect URIs: https://authlib.org/
- Allowed Grant Types: authorization_code password
- Allowed Response Types: code

之后用获取到的数据申请`access token`，发送请求

```bash
curl -u ${client_id}:${client_secret} -XPOST http://127.0.0.1:5000/oauth/token -F grant_type=password -F username=${username} -F password=${password}
```

`-u`表示使用Basic认证编码`${client_id}:${client_secret}`，然后在表单（form-data）里加入以下字段

```
grant_type=password
username=${username}
password=${password}
```

发送请求到`/oauth/token`获取access_token。

之后就可以拿这个access_token放在请求头`Authorization`处`Authorization: Bearer ${access_token}`请求`/api/me`获取资源。

```Python
# app\views\oauth2_views.py
@views.route('/api/me')
@require_oauth()
def api_me():
    ...
```

# 使用步骤2

修改`.env.example`创建`.env`，使用client目录下的脚本获取相关变量并设置。

```powershell
pipenv run python client/main.py
pipenv run python client/fetch_resource.py
```
