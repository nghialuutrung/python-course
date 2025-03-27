# Hướng Dẫn Thiết Lập Môi Trường Phát Triển

## Yêu Cầu Cơ Bản

### Công Cụ & Phiên Bản
- **Python**: 3.11
- **Git**: 2.30+
- **Docker**: 20.10+ (Tùy chọn, cho môi trường đồng nhất)
- **IDE**: VS Code, PyCharm, hoặc tương đương
- **Jupyter**: Notebook hoặc Lab

## Cài Đặt Môi Trường Python

### Sử Dụng pyenv (Khuyến nghị)

**Cài đặt pyenv**:

**Trên macOS**:
```bash
brew install pyenv
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init --path)"' >> ~/.zshrc
source ~/.zshrc
```

**Trên Linux**:
```bash
curl https://pyenv.run | bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
source ~/.bashrc
```

**Trên Windows**:
```bash
pip install pyenv-win --target $HOME/.pyenv
# Thêm %USERPROFILE%\.pyenv\pyenv-win\bin và %USERPROFILE%\.pyenv\pyenv-win\shims vào PATH
```

**Cài đặt Python**:
```bash
pyenv install 3.10.8
pyenv global 3.10.8
```

### Sử Dụng Conda

**Cài đặt Miniconda**:
- Tải từ [https://docs.conda.io/en/latest/miniconda.html](https://docs.conda.io/en/latest/miniconda.html)
- Cài đặt theo hướng dẫn

**Tạo Environment**:
```bash
conda create -n python-course python=3.10
conda activate python-course
```

## Cài Đặt Dependencies

### Sử Dụng Virtual Environment

**Tạo và kích hoạt venv**:
```bash
python -m venv venv
# Trên Windows
venv\Scripts\activate
# Trên macOS/Linux
source venv/bin/activate
```

**Cài đặt packages**:
```bash
pip install -r environment/requirements.txt
```

### Cài đặt Pre-commit Hooks

**Cài đặt pre-commit**:
```bash
pip install pre-commit
```

**Cài đặt hooks**:
```bash
pre-commit install
```

## Thiết Lập IDE

### VS Code

**Extensions Khuyến Nghị**:
- Python
- Pylance
- Jupyter
- Docker
- Git History
- markdownlint
- PowerPoint Slides

**Thiết Lập Settings**:
```json
{
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "editor.formatOnSave": true,
    "python.testing.pytestEnabled": true,
    "jupyter.alwaysTrustNotebooks": true
}
```

### PyCharm

**Plugins Khuyến Nghị**:
- Jupyter
- Markdown
- Docker
- Requirements

**Thiết Lập**:
1. Mở Settings (Ctrl+Alt+S)
2. Chọn Project > Python Interpreter > Add
3. Chọn Existing Environment và trỏ đến venv/bin/python
4. Enable code inspections và formatting tools

## Thiết Lập Jupyter

### Jupyter Notebook Setup

**Cài đặt**:
```bash
pip install jupyter notebook
pip install ipykernel
python -m ipykernel install --user --name=python-course
```

**Cài đặt Extensions**:
```bash
pip install jupyter_contrib_nbextensions
jupyter contrib nbextension install --user
```

**Khuyến nghị kích hoạt các extensions**:
- Table of Contents
- Collapsible Headings
- ExecuteTime
- Codefolding
- spellchecker

### JupyterLab Setup

**Cài đặt**:
```bash
pip install jupyterlab
```

**Cài đặt Extensions**:
```bash
pip install jupyterlab-git
pip install jupyterlab-drawio
```

## Thiết Lập Docker

### Docker Basics

**Cài đặt Docker**:
- [Docker Desktop cho Windows/Mac](https://www.docker.com/products/docker-desktop)
- [Docker Engine cho Linux](https://docs.docker.com/engine/install/)

**Build Docker Image**:
```bash
docker build -t python-course:latest -f environment/Dockerfile .
```

**Chạy Docker Container**:
```bash
docker run -it --rm -p 8888:8888 -v $(pwd):/app python-course:latest
```

### Docker Compose

**Sử dụng docker-compose.yml**:
```bash
docker-compose up
```

## Thiết Lập GitHub Classroom

### Tạo Organization

1. Tạo GitHub Organization mới
2. Thiết lập GitHub Team với các thành viên
3. Cấu hình quyền và roles

### Thiết Lập Classroom

1. Truy cập [GitHub Classroom](https://classroom.github.com/)
2. Connect với Organization
3. Tạo Classroom mới
4. Import roster (nếu có)

### Tạo Assignment

1. Tạo assignment mới
2. Thiết lập repository template
3. Cấu hình deadline và visibility
4. Thiết lập auto-grading (nếu cần)

## Thiết Lập Auto-Grading

### Sử Dụng pytest

**Cài đặt Pytest**:
```bash
pip install pytest pytest-cov
```

**Viết Tests**:
```python
# test_exercise.py
def test_function():
    from student_solution import my_function
    assert my_function(10) == 20
```

### GitHub Actions CI/CD

**Tạo Workflow File**:
```yaml
# .github/workflows/classroom.yml
name: GitHub Classroom Workflow

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  build:
    name: Autograding
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install pytest
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
      - name: Test with pytest
        run: |
          pytest -v
```

## Thiết Lập Môi Trường Slide

### PowerPoint Template

1. Tải template từ resources/templates/slide_template.pptx
2. Sử dụng master slides đã được thiết kế
3. Tuân thủ color scheme và typography

### Keynote Template

1. Tải template từ resources/templates/slide_template.key
2. Sử dụng master slides đã được thiết kế
3. Export sang PowerPoint khi cần thiết

## Cấu Hình Git

### Git Config

**Thiết lập cơ bản**:
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
git config --global core.editor "code --wait"
```

**Thiết lập alias hữu ích**:
```bash
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status
git config --global alias.last 'log -1 HEAD'
```

### Git Flow

**Cài đặt Git Flow**:
```bash
# macOS
brew install git-flow

# Linux
apt-get install git-flow

# Windows
git flow init
```

**Sử dụng Git Flow**:
```bash
# Khởi tạo
git flow init

# Bắt đầu feature mới
git flow feature start feature_name

# Hoàn thành feature
git flow feature finish feature_name
```

## Kiểm Tra Cài Đặt

### Verification Script

Tạo file `verify_environment.py`:

```python
#!/usr/bin/env python3
import sys
import platform
import subprocess
import importlib.util

def check_python_version():
    min_version = (3, 9)
    current = sys.version_info
    if current < min_version:
        print(f"❌ Python {current.major}.{current.minor} detected. Minimum required: {min_version[0]}.{min_version[1]}")
        return False
    print(f"✅ Python {current.major}.{current.minor}.{current.micro}")
    return True

def check_package(package, min_version=None):
    try:
        spec = importlib.util.find_spec(package)
        if spec is None:
            print(f"❌ {package} not installed")
            return False
        
        if min_version:
            pkg = __import__(package)
            version = pkg.__version__
            if version < min_version:
                print(f"❌ {package} version {version} detected. Minimum required: {min_version}")
                return False
            print(f"✅ {package} {version}")
        else:
            print(f"✅ {package} installed")
        return True
    except ImportError:
        print(f"❌ {package} not installed")
        return False

def check_command(command, args=["--version"]):
    try:
        result = subprocess.run([command] + args, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {command} {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {command} not working properly")
            return False
    except FileNotFoundError:
        print(f"❌ {command} not found")
        return False

def main():
    print("Environment Verification")
    print("=======================")
    
    # Check Python
    check_python_version()
    
    # Check packages
    packages = [
        "jupyter", 
        "pytest", 
        "numpy", 
        "pandas", 
        "matplotlib"
    ]
    
    for pkg in packages:
        check_package(pkg)
    
    # Check commands
    commands = [
        "git",
        "docker",
        "jupyter"
    ]
    
    for cmd in commands:
        check_command(cmd)
    
    print("\nVerification completed!")

if __name__ == "__main__":
    main()
```

**Chạy verification**:
```bash
python verify_environment.py
```

## Troubleshooting

### Vấn Đề Phổ Biến

#### Python Path Issues

**Vấn đề**: Không tìm thấy module khi import
**Giải pháp**:
```python
import sys
sys.path.append('/path/to/your/project')
```

#### Jupyter Kernel Not Found

**Vấn đề**: Không tìm thấy kernel Python
**Giải pháp**:
```bash
python -m ipykernel install --user --name=python-course
```

#### Git Permission Issues

**Vấn đề**: Permission denied khi push/pull
**Giải pháp**:
```bash
# Kiểm tra SSH key
ssh -T git@github.com

# Tạo SSH key mới nếu cần
ssh-keygen -t ed25519 -C "your.email@example.com"
```

## Resources

### Documentation Links

- [Python Documentation](https://docs.python.org/3/)
- [Jupyter Documentation](https://jupyter.org/documentation)
- [Git Documentation](https://git-scm.com/doc)
- [Docker Documentation](https://docs.docker.com/)
- [GitHub Classroom Guide](https://docs.github.com/en/education/manage-coursework-with-github-classroom)

### Tutorials & Guides

- [Real Python Tutorials](https://realpython.com/)
- [Jupyter Notebook Best Practices](https://jupyter.readthedocs.io/en/latest/running.html)
- [Git Branching Model](https://nvie.com/posts/a-successful-git-branching-model/)
- [Python Testing with pytest](https://docs.pytest.org/en/latest/getting-started.html) 