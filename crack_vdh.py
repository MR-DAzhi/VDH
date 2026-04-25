import re
import os

def apply_final_patch(file_path):
    if not os.path.exists(file_path):
        print(f"错误: 找不到 {file_path}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # --- 1. 注入网络拦截器 (解决 402 错误) ---
    # 这段代码会拦截 fetch 请求，当插件询问服务器权限时，直接返回“已付费”的状态
    hook_code = """
(function() {
    const _fetch = window.fetch;
    window.fetch = async (...args) => {
        const url = typeof args[0] === 'string' ? args[0] : args[0].url;
        if (url && url.includes('entitlements/validate')) {
            console.log('VDH Patch: 拦截到验证请求，正在伪造授权响应...');
            return new Response(JSON.stringify({
                status: 'ok',
                entitled: true,
                is_premium: true,
                is_entitled: true,
                expires: 2524608000000
            }), {
                status: 200,
                statusText: 'OK',
                headers: {'Content-Type': 'application/json'}
            });
        }
        return _fetch(...args);
    };
    console.log('VDH Patch: 网络拦截器已就绪');
})();
"""
    
    if "entitlements/validate" not in content:
        content = hook_code + content
        print("- 已注入网络拦截逻辑")

    # --- 2. 修改本地 120 分钟逻辑 ---
    pattern = re.compile(r'(7200\*1e3.*?if\()([^)]+)(\))')
    if pattern.search(content):
        content = pattern.sub(r'\1false\3', content)
        print("- 已解除本地 120 分钟限制")
    else:
        print("! 未发现本地限制字符，可能之前已修改或版本不匹配")

    # --- 保存文件 ---
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(">>> 全部修改完成！")
    except Exception as e:
        print(f"写入失败: {e}")

if __name__ == "__main__":
    apply_final_patch("main.js")
