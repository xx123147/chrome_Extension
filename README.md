## manifest.json文件字段详解
```json
{
    //配置文件版本
  "manifest_version": 3,
    //定义扩展的名称
  "name": "Web Info Grabber",
    //扩展的版本号
  "version": "1.0",
    //对扩展的简要描述
  "description": "Get the current page title and URL, and copy the URL.",
    //定义扩展的权限
  "permissions": ["activeTab", "scripting"],
  "action": {
    //点击图标时现实的弹出窗口的html文件
    "default_popup": "popup.html",
    //不同尺寸的图标文件
    "default_icon": {
      "16": "icon.png",
      "48": "icon.png",
      "128": "icon.png"
    }
  },
  "icons": {
    "16": "icon.png",
    "48": "icon.png",
    "128": "icon.png"
  }
}

