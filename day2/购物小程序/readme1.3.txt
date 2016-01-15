Shopping_small_programs1.3.Py README
===============

##详解
8个函数
begin()  ##最开始执行的函数，里面会调用register()和login()函数
register() #注册函数
login() #登陆函数
budget() #预算金额函数
welcome() #选择函数
shangpin() #商品计算函数
balance_accounts() #结算函数
recharge() #金额充值函数
neaten_shopping_cart() #购物车整理函数

##example register
欢迎进入大甩卖商城，您目前可以有两个选择，1.登陆，2.注册

请选择：2
请输入注册用户名：
test
请输入注册密码：
123456
恭喜您注册成功！
欢迎进入大甩卖商城，您目前可以有两个选择，1.登陆，2.注册

##example login
欢迎进入大甩卖商城，您目前可以有两个选择，1.登陆，2.注册

请选择：1
请输入登陆用户名:test
请输入密码:123456
恭喜你:test 用户登陆成功！

##Complete example
欢迎进入大甩卖商城，您目前可以有两个选择，1.登陆，2.注册

请选择：1
请输入登陆用户名:test
请输入密码:123456
恭喜你:test 用户登陆成功！

购物之前，请输入您的预算金额: 50000
您的预算金额为:50000

    ###############################################
    #           ❤欢迎进入大甩卖商城❤              #
    #             您可以选择以下商品：              #
    #            (1): iphone7    7000             #
    #            (2): ipad_air2  8000             #
    #            (3): ipad_pro   9000             #
    #             w: 结算                         #
    #             z: 对购物车进行整理              #
    #             c: 金额充值                      #
    #             q: 不买了，走人                  #
    ###############################################
please choice your like shop and do somthing:1
...
omit...
...
please choice your like shop and do somthing:2
...
omit...
...
please choice your like shop and do somthing:3
...
omit...
...
please choice your like shop and do somthing:w
您最终的选择： 商品:ipad_air2，数量:1,商品花费: 8000
您最终的选择： 商品:iphone7，数量:1,商品花费: 7000
您最终的选择： 商品:ipad_pro，数量:1,商品花费: 9000
总花费：24000,剩余金额：26000