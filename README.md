# volunteer-hours-system

开发组任务登记及志愿时长分配系统——一个用于登记开发组内部任务、自动统计并分配成员志愿时长的 Web 系统。

## 功能特性

- 任务管理（登记 / 查看 / 编辑 / 删除）
- 参与者管理（登记 / 查看 / 编辑 / 删除）
- 时长统计（首页自动汇总 + 参与者页面明细查询）
- 响应式界面（桌面 / 移动端）

## 技术栈

- **后端**：Python 3.x：Flask + Flask-SQLAlchemy + SQLite
- **前端**：原生 HTML + CSS + JavaScript
- **迁移**：Flask-Migrate（Alembic）
- **生产**：gunicorn

## 项目结构

```
volunteer-hours-system/
├── app/
│   ├── templates/       # HTML
│   ├── static/          # JS & CSS
│   ├── __init__.py      # Flask 应用工厂
│   ├── extensions.py    # SQLAlchemy, Migrate 实例
│   ├── models.py        # 数据模型
│   ├── routes.py        # 路由与 API
│   └── validate.py      # 输入校验
├── migrations/          # Alembic 迁移
├── instance/            # 运行时数据
├── app.py               # 开发入口
├── config.py            # 配置
├── entrypoint.py        # 生产启动脚本
└── requirements.txt     # 依赖
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

## 团队

- 前端：@[WhiteCatBlackHat](https://github.com/WhiteCatBlackHat)
- 后端：@[aaa1145141919810](https://github.com/aaa1145141919810)

## License

MIT License