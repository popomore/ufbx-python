# 发布到 PyPI

## 概述

本项目使用 GitHub Actions 自动化发布流程，支持发布到 PyPI 和 TestPyPI。

## 🚀 快速发布（推荐）

### 通过 GitHub Release 发布

1. **更新版本号**
   ```bash
   # 编辑 ufbx/__init__.py
   vim ufbx/__init__.py
   # 修改 __version__ = '0.2.0'
   ```

2. **提交更改**
   ```bash
   git add ufbx/__init__.py
   git commit -m "Bump version to 0.2.0"
   git push
   ```

3. **创建并推送 tag**
   ```bash
   git tag v0.2.0
   git push origin v0.2.0
   ```

4. **在 GitHub 创建 Release**
   - 访问 https://github.com/popomore/ufbx-python/releases/new
   - 选择 tag: `v0.2.0`
   - 填写 Release 说明
   - 点击 "Publish release"

5. **自动发布完成**
   - GitHub Actions 自动构建
   - 自动上传到 PyPI
   - 10-15 分钟后可在 https://pypi.org/project/ufbx/ 看到新版本

## 🔧 配置 PyPI 可信发布（一次性设置）

### 步骤 1: 在 PyPI 上配置

1. 登录 PyPI: https://pypi.org/
2. 访问 "Publishing" 页面: https://pypi.org/manage/account/publishing/
3. 点击 "Add a new pending publisher"
4. 填写信息：
   - **PyPI Project Name**: `ufbx`
   - **Owner**: `popomore`
   - **Repository name**: `ufbx-python`
   - **Workflow name**: `publish.yml`
   - **Environment name**: `pypi`
5. 点击 "Add"

### 步骤 2: 在 GitHub 上配置环境

1. 访问 https://github.com/popomore/ufbx-python/settings/environments
2. 点击 "New environment"
3. 名称: `pypi`
4. （可选）添加保护规则：
   - Required reviewers: 添加可以批准发布的人
   - Wait timer: 设置等待时间
5. 点击 "Configure environment"

### 步骤 3: 首次发布

首次发布后，PyPI 会自动关联项目和可信发布配置。

## 🧪 测试发布（TestPyPI）

用于测试发布流程，不影响正式版本。

### 配置 TestPyPI（可选）

1. 访问 https://test.pypi.org/manage/account/publishing/
2. 使用相同的配置，Environment 改为 `testpypi`

### 手动触发测试发布

1. 访问 https://github.com/popomore/ufbx-python/actions/workflows/publish.yml
2. 点击 "Run workflow"
3. 选择分支（通常是 `main`）
4. 点击 "Run workflow"

### 测试安装

```bash
pip install --index-url https://test.pypi.org/simple/ ufbx
```

## 📋 工作流说明

### `.github/workflows/publish.yml`

**触发条件：**
- GitHub Release 发布时（自动）
- 手动触发（workflow_dispatch）

**构建流程：**
1. 检出代码
2. 安装 Python 和依赖
3. 下载 ufbx 源码（`sfs.py update`）
4. 构建源码分发包和轮子
5. 上传构建产物

**发布流程：**
- **PyPI**: Release 触发时自动发布
- **TestPyPI**: 仅手动触发时发布

### `.github/workflows/test.yml`

**测试流程：**
- 在多个 Python 版本（3.8-3.12）测试
- 在多个操作系统（Linux, macOS, Windows）测试
- 运行 pytest 测试套件
- 生成代码覆盖率报告

## 📦 本地构建测试

### 安装构建工具

```bash
pip install build twine
```

### 构建分发包

```bash
# 下载依赖
python sfs.py update --all

# 构建源码分发包
python -m build --sdist

# 构建轮子
python -m build --wheel

# 构建两者
python -m build
```

### 检查分发包

```bash
# 检查包的元数据
twine check dist/*

# 查看包内容
tar -tzf dist/ufbx-*.tar.gz | less

# 本地测试安装
pip install dist/ufbx-*.whl
```

## 🔍 故障排查

### 问题: 发布失败 - "Authentication failed"

**原因**: PyPI 可信发布未正确配置

**解决方案**:
1. 检查 PyPI 上的可信发布配置
2. 确保 GitHub 环境名称与配置一致
3. 确保 workflow 文件名正确

### 问题: 构建失败 - "Cannot find ufbx.h"

**原因**: sfs.py 未正确下载依赖

**解决方案**:
1. 检查 `sfs-deps.json` 配置
2. 确保 GitHub Actions 可以访问外网
3. 手动运行 `python sfs.py update --all` 测试

### 问题: 版本冲突

**原因**: 尝试上传已存在的版本号

**解决方案**:
1. PyPI 不允许重新上传相同版本
2. 增加版本号后重新发布
3. 不要删除 tag，创建新的版本

### 问题: 测试失败

**原因**: 代码问题或环境问题

**解决方案**:
1. 本地运行 `pytest tests/` 确保测试通过
2. 查看 GitHub Actions 日志
3. 检查特定 Python 版本或操作系统的问题

## 📚 参考资料

- [PyPI 可信发布文档](https://docs.pypi.org/trusted-publishers/)
- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [Python 打包用户指南](https://packaging.python.org/)
- [setuptools 文档](https://setuptools.pypa.io/)

## ✅ 发布检查清单

发布前确认：

- [ ] 所有测试通过（本地和 CI）
- [ ] 更新了版本号（`ufbx/__init__.py`）
- [ ] 更新了 README（如有新功能）
- [ ] 添加了 CHANGELOG 条目（如有的话）
- [ ] 代码已合并到 main 分支
- [ ] 创建了 Git tag
- [ ] 创建了 GitHub Release
- [ ] PyPI 可信发布已配置
- [ ] GitHub 环境已设置
