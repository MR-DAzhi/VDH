# 在 main.js 的最开头插入一段强制置零的代码
def patch_force_zero(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 注入 Hook 代码：拦截存储并强制 lsd 为 0
    hook_code = """
(function() {
    const _get = chrome.storage.local.get;
    chrome.storage.local.get = function(k, c) {
        if (k === 'lsd' || (Array.isArray(k) && k.includes('lsd'))) {
            if (c) return _get.call(this, k, r => { if(r) r.lsd = 0; c(r); });
            return _get.call(this, k).then(r => { if(r) r.lsd = 0; return r; });
        }
        return _get.apply(this, arguments);
    };
})();
"""
    if "chrome.storage.local.get" not in content[:500]: # 避免重复注入
        new_content = hook_code + content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("已注入底层 Hook 逻辑！")
