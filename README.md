# 云顶修仙命令行版本

浏览器版本地址：http://yundingxx.com:3344

```bash
# 克隆代码
git clone git@github.com:hanhan-GKD/yundingxx-cmdline.git
cd yundingxx-cmdline

# 环境安装（建议虚拟环境安装）
pip install -r requirements/dev.txt

# 初始化代码检查钩子函数
# 执行commit的时候会进行代码检查，图形化界面可能会报错
pip install -U pre-commit
pre-commit install
```

