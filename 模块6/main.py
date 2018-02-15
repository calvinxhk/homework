from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,  Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine('mysql+pymysql://root:xhk313025644@127.0.0.1:3306/author?charset=utf8', max_overflow=10)
Base = declarative_base()


class User(Base):
    __tablename__ = '用户信息'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(10))
    password = Column(String(16))
    id_card = Column(String(18))
    role_id = Column(Integer, default=3)


class Role(Base):
    __tablename__ = '角色'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))


class Authority(Base):
    __tablename__ = '权限'
    id = Column(Integer, primary_key=True, autoincrement=True)
    authority = Column()


class RoleAuthority(Base):
    __tablename__ = '角色权限'
    role_id = Column(Integer, primary_key=True)
    auth_id = Column(String(20))


def drop():
    Base.metadata.drop_all(engine)


def create():
    Base.metadata.create_all(engine)


def login():
    while True:
        name = input('input your name:').strip()
        password = input('input your password:').strip()
        ret = session.query(User).filter(User.name == name,User.password == password).first()
        if ret:
            print('login successfully!')
            return ret
        else:
            print('wrong name or password!')


def registration():
    while True:
        name = input('input your name:').strip()
        ret = session.query(User).filter(User.name == name).first()
        if ret:
            print('name has been registrated!')
            continue
        password = input('password').strip()
        password_c = input('password again').strip()
        if password != password_c:
            print('password is wrong!')
            continue
        id_number = input('id number:').strip()
        ret = session.query(User).filter(User.name == name).first()
        if ret :
            print('name has been registrated!')
        session.add(User(name = name,password = password,id_card = id_number))
        session.commit()
        print('registart successfully!')
        return


def get_passwd():
    while True:
        name = input('name:')
        id_number = input('id number:')
        ret = session.query(User).filter(User.name == name,User.id_card == id_number).first()
        if ret:
            print('password is %s'%ret.password)
            return
        else:
            print('wrong information!')


def display_auth(ret):
    roleid= ret.role_id
    ret = session.query(RoleAuthority).filter(RoleAuthority.role_id ==roleid).first()
    auth = ret.auth_id.split(',')
    res = session.query(Authority).filter(Authority.id.in_(auth)).all()
    auth = []
    for i in res:
        auth.append(i.authority)
    return auth


def auth_gov():
    while True:
        choice2 = input('1.增 2.删 3.改 4.查')
        if choice2 == 'q':
            return
        if choice2 == '1':
            auth = input('authority:').strip()
            res = session.query(Authority).filter(Authority.authority == auth).first()
            if res:
                print('authority is existed.')
                continue
            session.add(Authority(authority=auth))
            session.commit()
            print('successfully!')
        if choice2 == '2':
            auth = input('id:').strip()
            session.query(Authority).filter(Authority.id == auth).delete()
            session.commit()
            print('successfully!')
        if choice2 == '3':
            auth_id = input('old id :').strip()
            new_auth = input('new authority:').strip()
            session.query(Authority).filter(Authority.id == auth_id).update({'authority': new_auth})
            session.commit()
            print('successfully!')
        if choice2 == '4':
            auth_id = input('id:').strip()
            res = session.query(Authority).filter(Authority.id == auth_id).first()
            print(res.authority)


def role_gov():
    while True:
        choice2 = input('1.增 2.删 3.改 4.查')
        if choice2 =='q':
            return
        if choice2 == '1':
            role = input('role:').strip()
            res = session.query(Role).filter(Role.name == role).first()
            if res:
                print('role is existed.')
                continue
            session.add(Role(name=role))
            session.commit()
            print('successfully!')
        if choice2 == '2':
            role = input('id:').strip()
            session.query(Role).filter(Role.id == role).delete()
            session.commit()
            print('successfully!')
        if choice2 == '3':
            auth_id = input('old id :').strip()
            new_auth = input('new name:').strip()
            session.query(Role).filter(Role.id == auth_id).update({'name': new_auth})
            session.commit()
            print('successfully!')
        if choice2 == '4':
            auth_id = input('id:').strip()
            res = session.query(Role).filter(Role.id == auth_id).first()
            print(res.name)


def relation_gov():
    while True:
        choice2 = input('1.增 2.删 3.改 4.查')
        if choice2 == 'q':
            return
        if choice2 == '1':
            role = input('role id:').strip()
            res = session.query(RoleAuthority).filter(RoleAuthority.role_id == role).first()
            if res:
                print('role is existed.')
                continue
            authority_id = input('authority_id').strip()
            session.add(RoleAuthority(role_id=role, auth_id=authority_id))
            session.commit()
            print('successfully!')
        if choice2 == '2':
            role = input('id:').strip()
            session.query(RoleAuthority).filter(RoleAuthority.role_id == role).delete()
            session.commit()
            print('successfully!')
        if choice2 == '3':
            role_id = input('old id :').strip()
            new_auth = input('new authority id :').strip()
            session.query(RoleAuthority).filter(RoleAuthority.role_id == role_id).update({'auth_id': new_auth})
            session.commit()
            print('successfully!')
        if choice2 == '4':
            id = input('id:').strip()
            res = session.query(RoleAuthority).filter(RoleAuthority.role_id == id).first()
            print(res.auth_id)


Session = sessionmaker(bind= engine)
session = Session()

while True:
    choice = input('1.登录 2.注册 3.找回密码  ').strip()
    if choice == '1':
        ret = login()
        while True:
            auth = display_auth(ret)
            choice1 = input('1.权限管理 2.角色管理 3.关系管理 4.自身权限')
            if choice1 == 'q':
                break
            if choice1 == '4':
                print(auth)
            if '管理' not in auth:
                print('no authority!')
                continue
            if choice1 == '1':
                auth_gov()
            if choice1 == '2':
                role_gov()
            if choice1 == '3':
                relation_gov()

    if choice == '2':
        registration()

    if choice == '3':
        get_passwd()

    if choice == 'q':
        break
session.close()


