#sublime-plugin备份
1. 找到备份目录
![打开package目录](http://upload-images.jianshu.io/upload_images/1156837-0c86fc8db7c1dd10.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
`command+上`两次到上两级目录
在终端输入`cd `将sublime目录拖到终端
![sublime目录](http://upload-images.jianshu.io/upload_images/1156837-713e393c91d2a6fc.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
``` bash
cd /Users/tederen/Library/Application\ Support/Sublime\ Text\ 3
```
2. 创建git仓库进行备份
.gitignore
```
*
!Installed\ Packages
!Packages
!.gitignore
```
提交上传云端仓库就行了
3. 恢复
删除Installed Packages,Packages文件夹，把远程仓库中的插件pull下来
``` bash
rm -Rf Installed\ Packages
rm -Rf Packages
git init
git remote add origin https://git.oschina.net/inu1255/sublime-plugin.git
git pull origin master
```
4. 备注：
因为我安装了eslint插件，需要安装eslint并添加配置文件才有javascript的代码提示
``` bash
npm install -gd eslint-plugin-react 
vim ~/.eslintrc.js
```
.eslintrc.js
``` javascript
module.exports = {
    "env": {
        "es6": true,
        "node": true,
        "browser": true
    },
    "extends" : [],
    "parserOptions": {
        "ecmaFeatures": {
            "experimentalObjectRestSpread": true,
            "jsx": true,
            "blockBindings": true
        },
        "sourceType": "module"
    },
    "globals": {
        "$":true,
        "Jquery":true,
        "BMap": true,
        "Bmob": true,
        "wx": true
    },
    "plugins": [
        "react"
    ],
    "rules": {
    }
}
```
