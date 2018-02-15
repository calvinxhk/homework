项目名称：权限管理系统
项目功能：1. 登陆、注册、找回密码
    2. 权限管理
    3. 角色管理
    4. 角色分配权限
    5. 动态显示当前登陆用户权限菜单

表结构：
1.角色（id,name）
2.权限（id,authority）
3.角色权限（role_id,auth_id）
4.用户信息（id,name,password,id_card,role_id）

代码思路：
使用sqlalchemy 的orm 实现各个功能。