#!/usr/bin/python
#coding=utf-8
__author__ = 'yaobin'

import os
from conf import settings
from modules import common,models
from sqlalchemy import create_engine,Table
from  sqlalchemy.orm import sessionmaker


class init_db(object):

    def __init__(self):
        self.engine = create_engine(settings.DB_CONN,echo=False)
        self.SessionCls = sessionmaker(bind=self.engine) #创建与数据库的会话session class ,注意,这里返回给session的是个class,不是实例
        self.session = self.SessionCls()
        self.select={
            'create_tables':self.create_tables,
            'create_hosts':self.create_hosts,
            'create_remoteusers':self.create_remoteusers,
            'create_bindhost':self.create_bindhost,
            'create_users':self.create_users
        }
        for i in self.select.keys():
            print(i)
        choice=common.input_msg(">:")
        if choice in self.select.keys():
            self.select[choice]()
        else:
            common.color_print("not this choice!",exits=True)



    def create_tables(self):
        common.color_print("create_tables...",color="green")
        models.Base.metadata.create_all(self.engine)



    def verify_file(func):
        def inner(self):
            self.yaml_file=common.input_msg("please input yaml file path>:")
            if os.path.exists(self.yaml_file):
                self.data=common.yaml_parser(self.yaml_file)
            else:
                common.color_print("this file not exits!",exits=True)
            return func(self)
        return inner


    def bind_hosts_filter(self,vals):
        print("**>",vals.get('bind_hosts'))
        bind_hosts=self.session.query(models.BindHost).filter(models.Host.hostname.in_(vals.get('bind_hosts'))).all()
        if not bind_hosts:
            common.color_print("none of {0} exists in bind_host table".format(vals.get('bind_hosts')),exits=True)
        return bind_hosts

    def user_profiles_filter(self,vals):
        user_profiles=self.session.query(models.UserProfile).filter(models.UserProfile.username.in_(vals.get("user_profiles"))).all()
        if not user_profiles:
            common.color_print("none of {0] exists in user_profile table".format(vals.get("user_profiles")),exits=True)
        return user_profiles





    @verify_file
    def create_users(self):
        #print(self.data)
        for key,val in self.data.items():
            print(key,val)
            obj=models.UserProfile(username=key,password=val.get('password'))
            if val.get('groups'):
                groups=self.session.query(models.Group).filter(models.Group.name.in_(val.get('groups'))).all()
                if not groups:
                    common.color_print("none of {0} exist in group table.".format(val.get('groups')),exits=True)
                obj.groups=groups
            if val.get('bind_hosts'):
                bind_hosts=self.bind_hosts_filter(val)
                obj.bind_hosts=bind_hosts

            self.session.add(obj)
        self.session.commit()

    @verify_file
    def create_groups(self):
        for key,val in self.data.items():
            print(key,val)
            obj=models.Group(name=key)
            if val.get('bind_hosts'):
                bind_hosts=self.bind_hosts_filter(val)
                obj.bind_hosts=bind_hosts

            if val.get("user_profiles"):
                user_profiles=self.user_profiles_filter(val)
                obj.user_profiles=user_profiles

            self.session.add(obj)
        self.session.commit()



    @verify_file
    def create_hosts(self):
        for key,val in self.data.items():
            print(key,val)
            obj=models.Host(hostname=key,ip_addr=val.get("ip_addr"),port=val.get("port") or 22)
            self.session.add(obj)
        self.session.commit()



    @verify_file
    def create_remoteusers(self):
        for key,val in self.data.items():
            print(key,val)
            obj=models.RemoteUser(username=val.get("username"),auth_type=val.get("auth_type"),password=val.get("password"))
            self.session.add(obj)
        self.session.commit()


    @verify_file
    def create_bindhost(self):
        for key,val in self.data.items():
            host_obj=self.session.query(models.Host).filter(models.Host.hostname==val.get("hostname")).first()
            assert host_obj
            for item in val['remote_users']:
                print(item)
                assert item.get('auth_type')
                if item.get('auth_type') == "ssh-passwd":
                    remoteuser_obj = self.session.query(models.RemoteUser).filter(
                        models.RemoteUser.username==item.get('username'),
                        models.RemoteUser.password==item.get('password')
                    ).first()
                else:
                    remoteuser_obj = self.session.query(models.RemoteUser).filter(
                        models.RemoteUser.username==item.get('username'),
                        models.RemoteUser.auth_type==item.get('auth_type')
                    ).first()

                if not remoteuser_obj:
                    common.color_print("RemoteUser obj {0} does not exist".format(item),exits=True)

                bindhost_obj=models.BindHost(host_id=host_obj.id,remoteuser_id=remoteuser_obj.id)
                self.session.add(bindhost_obj)

                if val.get('groups'):
                    group_objs=self.session.query(models.Group).filter(models.Group.name.in_(val.get('group'))).all()
                    assert group_objs
                    print("groups:",group_objs)
                    bindhost_obj.groups=group_objs

                if val.get('user_profiles'):
                    userprofile_objs=self.session.query(models.UserProfile).filter(models.UserProfile.username.in_(val.get("user_profiles"))).all()
                    assert userprofile_objs
                    print("userprofiles:",userprofile_objs)
                    bindhost_obj.user_profiles=userprofile_objs
        self.session.commit()


