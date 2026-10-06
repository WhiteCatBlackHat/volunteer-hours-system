# volunteer-hours-system

开发组任务登记及志愿时长分配系统——一个用于登记开发组内部任务、自动统计并分配成员志愿时长的 Web 系统。

## 功能特性

- 任务管理（登记 / 查看 / 编辑 / 删除）
- 参与者管理（登记 / 查看 / 编辑 / 删除）
- 时长统计（首页自动汇总 + 参与者页面明细查询）
- 响应式界面（桌面 / 移动端）
- 账号登录与权限管理

## 技术栈

- **后端**：Python 3.x：Flask + Flask-SQLAlchemy + SQLite
- **前端**：原生 HTML + CSS + JavaScript
- **迁移**：Flask-Migrate（Alembic）
- **生产**：gunicorn

## 项目结构

```
volunteer-hours-system/
│
├── app/                                  # 应用包（核心代码）
│   ├── __init__.py                       # 应用工厂
│   ├── extensions.py                     # 扩展实例
│   ├── models.py                         # 所有数据模型
│   ├── routes.py                         # main 蓝图：所有业务路由
│   ├── validate.py                       # 输入校验
│   ├── auth/                             # 认证蓝图（管理员登录）
│   │   ├── __init__.py                   # auth_bp = Blueprint("auth", __name__)
│   │   ├── forms.py                      # LoginForm（FlaskForm）
│   │   └── routes.py                     # /login  /logout
│   ├── utils/                            # 工具模块
│   │   ├── __init__.py
│   │   └── decorators.py                 # admin_required 装饰器
│   ├── templates/                        # Jinja2 模板
│   └── static/                           # 静态资源
├── migrations/                           # Alembic 迁移目录
│   └── versions/                         # 迁移脚本
├── instance/                             # 运行时数据
├── app.py                                # 开发入口
├── config.py                             # 配置类
├── entrypoint.py                         # 生产部署入口
└── requirements.txt                      # 依赖清单
```

## 本地运行

```bash
git clone https://github.com/WhiteCatBlackHat/volunteer-hours-system
cd volunteer-hours-system
pip install -r requirements.txt
python app.py
```

## 服务器部署

```bash
git clone https://github.com/WhiteCatBlackHat/volunteer-hours-system
cd volunteer-hours-system
pip install -r requirements.txt
python entrypoint.py
```

## API 接口

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/` | 首页 |
| GET | `/task/list` | 任务列表 |
| POST | `/task/add` | 新建任务 |
| PUT | `/task/edit/<id>` | 编辑任务 |
| DELETE | `/task/delete/<id>` | 删除任务 |
| GET | `/user/list` | 参与者列表 |
| POST | `/user/add` | 新建参与者 |
| PUT | `/user/edit/<username>` | 编辑参与者 |
| DELETE | `/user/delete/<username>` | 删除参与者 |
| GET | `/user/<username>/total_hours` | 累计时长 |

## 管理员创建
使用前保证配置了环境变量：
```bash
$env:FLASK_APP = "app.py"
```
后续运行以下命令并根据提示进行操作：
```bash
flask create-admin
```
运行以下命令并根据提示操作以封禁管理员：
```bash
flask ban
```

## 团队

- 前端：@[WhiteCatBlackHat](https://github.com/WhiteCatBlackHat)
- 后端：@[aaa1145141919810](https://github.com/aaa1145141919810)

## License

MIT License