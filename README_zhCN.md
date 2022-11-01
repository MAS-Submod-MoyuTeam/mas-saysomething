<h1 align="center">🗨️ 说点东西子模组</h1>
<h3 align="center">让莫妮卡为你说你想听的话或摆你想看的姿势~</h3>

<p align="center">
  <a href="https://github.com/friends-of-monika/mas-saysomething/releases/latest">
    <img alt="Latest release" src="https://img.shields.io/github/v/release/friends-of-monika/mas-saysomething">
  </a>
  <a href="https://github.com/friends-of-monika/mas-saysomething/releases">
    <img alt="Release downloads" src="https://img.shields.io/github/downloads/friends-of-monika/mas-saysomething/total">
  </a>
  <a href="https://www.reddit.com/r/MASFandom/comments/yeqld8/heya_people_say_something_submod_is_out">
    <img alt="Reddit badge" src="https://img.shields.io/badge/dynamic/json?label=%F0%9D%97%8B%2Fmasfandom%20post&query=%24[0].data.children[0].data.score&suffix=%20upvotes&url=https%3A%2F%2Fwww.reddit.com%2Fr%2FMASFandom%2Fcomments%2Fyeqld8%2Fheya_people_say_something_submod_is_out.json&logo=reddit&style=social">
  </a>
  <a href="https://github.com/friends-of-monika/mas-saysomething/blob/main/LICENSE.txt">
    <img alt="MIT license badge" src="https://img.shields.io/badge/License-MIT-lightgrey.svg">
  </a>
  <a href="https://dcache.me/discord">
    <img alt="Discord server" src="https://discordapp.com/api/guilds/1029849988953546802/widget.png?style=shield">
  </a>
  <a href="https://ko-fi.com/Y8Y15BC52">
    <img alt="Ko-fi badge" src="https://ko-fi.com/img/githubbutton_sm.svg" height="20">
  </a>
</p>


## 🌟 功能

* 让莫妮卡对你说任何话!
* 一个内置的表情切换器!
* 一个内置的开关, 让你将莫妮卡放在屏幕的任意位置.
* 支持多行输入~
* [允许查看表情代码][15]以帮助子模组的开发.

## 🖼️ 截图

![莫妮卡在思考这是什么彩蛋...][12]
![莫妮卡印象深刻][13]

## ❓ 安装

1. 前往[最新发布][6]下滑到资源文件.
2. 针对你的MAS版本下载对应的 `say-something-版本号-MAS版本号.zip` 
3. 拖入你的`ddlc/mas`文件夹.

   **NOTE:** 不要拖到*`game`*里面！
4. 你已经准备好了!~

## 🔧 启用表情代码

要显示表情代码，你的MAS必须在*开发模式*
创建一个 `dev_devmode.rpy` 在 `game/Submods` 文件夹，并输入以下内容：

```renpy
init python:
    config.developer = True
```

保存文件，重启游戏, 然后你会在Submod设置界面看到“显示表情代码”选项，勾选它即可。

*为什么这么复杂?* 这是尽量避免对表情选择界面的破坏，同时对非子模组开发者的一个优化，他们不需要晦涩难懂的代码。

## 🏅 特别感谢

Say Something Submod的作者、维护者和贡献者对以下人员表示感谢：
* [SteveeWasTaken][1] &mdash; [MAS Custom Text][2] 子模组和灵感来源.
* [MaximusDecimus][3] &mdash; [MAS Custom Text Revamp][4] 子模组.

此外，我们感谢这些人在公开发布前对该子模组进行测试:
* [Otter][5] &mdash; 早期开发预览.
* [DJMayJay][14] &mdash; 早期开发预览.
* TheGuy &mdash; 早期开发预览.

## 💬 加入我们的 Discord

我们开始聊天了! 来加入 submod 作者的 [Discord服务器][8] 或者加入 Friends of Monika 的 [Discord 服务器][9].

[![Discord server invitation][10]][8]
[![Discord server invitation][11]][9]

[1]: https://github.com/SteveeWasTaken
[2]: https://github.com/SteveeWasTaken/mas-custom-text
[3]: https://github.com/AzhamProdLive
[4]: https://github.com/AzhamProdLive/AzhamMakesTrash-Submods/tree/main/Custom%20Text%20Revamp
[5]: https://github.com/my-otter-self
[6]: https://github.com/MAS-Submod-MoyuTeam/mas-saysomething/releases/latest
[7]: https://github.com/PencilMario
[8]: https://dcache.me/discord
[9]: https://mon.icu/discord
[10]: https://discordapp.com/api/guilds/1029849988953546802/widget.png?style=banner3
[11]: https://discordapp.com/api/guilds/970747033071804426/widget.png?style=banner3
[12]: doc/screenshots/1.png
[13]: doc/screenshots/2.png
[14]: https://github.com/mayday-mayjay
[15]: https://github.com/MAS-Submod-MoyuTeam/mas-saysomething/blob/py2/README_zhCN.md#-%E5%90%AF%E7%94%A8%E8%A1%A8%E6%83%85%E4%BB%A3%E7%A0%81
