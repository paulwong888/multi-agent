## Football Predict
体育赛事预测-transformer版
### 安装
```
conda create -n autogen python=3.10 -y
conda activate autogen


pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/
pip install -r src_muti_agent/requirements.txt
pip install autogen-ext[mcp]



export HF_HOME=/root/autodl-fs/paul/huggingface
```

### 安装autogenstudio
```
pip install autogenstudio

#启动
autogenstudio ui --port 8081
```

### 安装playwright
```
pip install playwright
playwright install
playwright install-deps
```

### 提取代码
```
git config --global user.name "huangp"
git config --global user.email "huangp@huangp.com"

```

### 安装mysql
```
# Ubuntu/Debian
sudo apt-get install libmysqlclient-dev

# Centos
sudo yum install mariadb-devel

# macOS
brew install mysql-client
```