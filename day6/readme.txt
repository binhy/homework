#################################################
# Created on: 2016年03月06日
# @author: 陈耀斌
# Email: 123391713@qq.com
# Blog: http://www.cnblogs.com/binhy0428/
# GitHub: https://github.com/binhy/
#################################################


回到10年前小游戏 README
===============

程序介绍:
程序还有很多功能可以实现，由于时间的关系，而且主要理解写一下类，就不深入的实现各种功能了。


#详解：
1.程序结构：
day6
├── bin
│   └── run.py  #程序主入口
├── conf
│   │  
│   └── settings.py  #配置文件
├── core            #主要程序逻辑
│   ├── db_handler.py  #数据连接引擎
│   ├── dump_or_load.py #用于从文件里加载或者存储角色数据
│   ├── main.py #主逻辑交互程序
│   ├── scene.py #场景模块，用于用户交互操作，打怪、购物、升级等
│  
├── db #角色和商品武器数据存储的地方
│   ├── game_accounts #角色数据目录
│   │   ├── hy.json
│   │   └── yaobin.json
│   ├── __init__.py
│   └── weapon_shop   #商品武器数据目录
│       └── weapon_list.json
├── __init__.py
├── readme.txt
└── role    #角色模块目录
    ├── __init__.py
    └── role.py  #角色模块文件，用户初始化实例各种角色

2.运行环境：Python3.0

3.执行例子：
请选择1,选择已经存在的游戏角色  2,创建新的游戏角色 3,退出
            1
1 hy
2 yaobin
 请选择你要进入游戏的人物：1

            返回主菜单(r)  存档(s) 查看武器背包（p）
            角色名:hy  角色:man 等级:8 手持武器:knife 血量: 100 经验值:40 钱:230
            -----------------------------------------------------------

            1.打怪 2.购买武器 3.升级 4.询问天使

            -----------------------------------------------------------

<<1

        1.暴龙兽 2.加鲁鲁兽 3.飞鹰兽

请选择你要打的怪：1
 角色:hy 增加经验:10
角色:hy 增加钱:10

            返回主菜单(r)  存档(s) 查看武器背包（p）
            角色名:hy  角色:man 等级:8 手持武器:knife 血量: 100 经验值:50 钱:240
            -----------------------------------------------------------

            1.打怪 2.购买武器 3.升级 4.询问天使

            -----------------------------------------------------------

<<2
 1.武器:青龙偃月刀 数量:25 金额:30
 2.武器:巨型飞镖 数量:16 金额:20
 3.武器:双节棍 数量:10 金额:10
 请输入你想买的武器: 1
 请输入购买的数量: 1
青龙偃月刀修改库存数量为:24
 1.武器:青龙偃月刀 数量:24 金额:30
 2.武器:巨型飞镖 数量:16 金额:20
 3.武器:双节棍 数量:10 金额:10
 请输入你想买的武器: r

            返回主菜单(r)  存档(s) 查看武器背包（p）
            角色名:hy  角色:man 等级:8 手持武器:knife 血量: 100 经验值:50 钱:210
            -----------------------------------------------------------

            1.打怪 2.购买武器 3.升级 4.询问天使

            -----------------------------------------------------------

<<3
 还不够经验升级！

            返回主菜单(r)  存档(s) 查看武器背包（p）
            角色名:hy  角色:man 等级:8 手持武器:knife 血量: 100 经验值:50 钱:210
            -----------------------------------------------------------

            1.打怪 2.购买武器 3.升级 4.询问天使

            -----------------------------------------------------------

<<4
heroine 我是天使引领者，有什么可以帮到你？
hy 我想回到现实世界，请验证！
heroine 恭喜你，你等级通过了！
heroine 钱不够啊，去赚多点再来找我吧！
hy 好吧，继续赚钱去！

            返回主菜单(r)  存档(s) 查看武器背包（p）
            角色名:hy  角色:man 等级:8 手持武器:knife 血量: 100 经验值:50 钱:210
            -----------------------------------------------------------

            1.打怪 2.购买武器 3.升级 4.询问天使

            -----------------------------------------------------------

<<


