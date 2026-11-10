#!/usr/bin/env python3
"""
API密钥安全配置验证工具
"""
import os
import re
import subprocess
from dotenv import load_dotenv

def check_env_file_security():
    """检查.env文件的安全配置"""
    print("🔒 API密钥安全配置验证")
    print("=" * 50)
    
    # 检查.env文件是否存在
    base_dir = os.path.expanduser("~/Trae")
    env_file = os.path.join(base_dir, ".env")
    if not os.path.exists(env_file):
        print("❌ .env文件不存在")
        return False
    
    print("✅ .env文件存在")
    
    # Let Git evaluate ignore rules, negations and whether the file is tracked.
    try:
        ignored = subprocess.run(
            ['git', '-C', base_dir, 'check-ignore', '--quiet', '--', '.env'],
            capture_output=True, check=False
        ).returncode == 0
    except OSError:
        ignored = False
    if not ignored:
        print("❌ 无法确认.env文件已被Git忽略且未被跟踪")
        return False
    print("✅ .env文件已被Git忽略且未被跟踪")
    
    # 加载环境变量
    load_dotenv(env_file)
    
    # 检查各个API密钥
    api_keys = {
        'KIMI_API_KEY': os.getenv('KIMI_API_KEY'),
        'ZHIPU_API_KEY': os.getenv('ZHIPU_API_KEY'),
        'GOOGLE_API_KEY': os.getenv('GOOGLE_API_KEY'),
        'ANTHROPIC_API_KEY': os.getenv('ANTHROPIC_API_KEY')
    }
    
    print("\n🔑 API密钥配置状态:")
    for key_name, key_value in api_keys.items():
        if key_value:
            print(f"✅ {key_name}: 已配置")
        else:
            print(f"❌ {key_name}: 未配置")
    
    return True

def check_code_security():
    """检查代码文件中是否有硬编码的API密钥"""
    print("\n🔍 代码安全检查:")
    
    # 检查的文件列表
    base_dir = os.path.expanduser("~/Trae")
    files_to_check = [
        os.path.join(base_dir, "test_openai.py"),
        os.path.join(base_dir, "test_claude.py"),
        os.path.join(base_dir, "test_gemini.py"),
        os.path.join(base_dir, "test_gemini_simple.py")
    ]
    
    # 可能的API密钥模式
    api_key_patterns = [
        r'sk-[a-zA-Z0-9]{48}',  # OpenAI格式
        r'AIza[a-zA-Z0-9_-]{35}',  # Google API格式
        r'[a-f0-9]{32}\.[a-zA-Z0-9]{16}',  # 智谱GLM格式
        r'api_key\s*=\s*["\'][^"\']+["\']',  # 通用API密钥赋值
    ]
    
    security_issues = []
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # 检查是否使用了os.getenv
                if 'os.getenv' in content:
                    print(f"✅ {os.path.basename(file_path)}: 使用环境变量")
                else:
                    print(f"⚠️  {os.path.basename(file_path)}: 未使用环境变量")
                
                # 检查是否有硬编码的API密钥
                for pattern in api_key_patterns:
                    for line_number, line in enumerate(content.splitlines(), 1):
                        for match in re.findall(pattern, line):
                            if not match.startswith('os.getenv') and 'your_' not in match.lower():
                                security_issues.append(f"{os.path.basename(file_path)}:{line_number}: 发现可能的硬编码API密钥")
    
    if security_issues:
        print("\n❌ 发现安全问题:")
        for issue in security_issues:
            print(f"  - {issue}")
        return False
    else:
        print("\n✅ 未发现硬编码的API密钥")
        return True

def generate_security_report():
    """生成安全报告"""
    print("\n📊 安全配置总结:")
    print("=" * 50)
    
    env_secure = check_env_file_security()
    code_secure = check_code_security()
    
    if env_secure and code_secure:
        print("\n🎉 所有安全检查通过！")
        print("✅ API密钥已安全存储在环境变量中")
        print("✅ 代码中未发现硬编码的API密钥")
        print("✅ .env文件已添加到.gitignore中")
    else:
        print("\n⚠️  发现安全问题，请及时修复")
    
    return env_secure and code_secure

if __name__ == "__main__":
    raise SystemExit(0 if generate_security_report() else 1)
