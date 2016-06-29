#_*_coding:utf-8_*_
__author__ = 'Alex Li'


from sqlalchemy import create_engine,Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String,ForeignKey,UniqueConstraint,UnicodeText,DateTime
from sqlalchemy.orm import relationship,sessionmaker
from sqlalchemy import or_,and_
from sqlalchemy import func
from sqlalchemy_utils import ChoiceType,PasswordType


Base = declarative_base() #生成一个SqlORM 基类




BindHost2Group = Table('bindhost_2_group',Base.metadata,
    Column('bindhost_id',ForeignKey('bind_host.id'),primary_key=True),
    Column('group_id',ForeignKey('group.id'),primary_key=True),
)

BindHost2UserProfile = Table('bindhost_2_userprofile',Base.metadata,
    Column('bindhost_id',ForeignKey('bind_host.id'),primary_key=True),
    Column('uerprofile_id',ForeignKey('user_profile.id'),primary_key=True),
)

Group2UserProfile = Table('group_2_userprofile',Base.metadata,
    Column('userprofile_id',ForeignKey('user_profile.id'),primary_key=True),
    Column('group_id',ForeignKey('group.id'),primary_key=True),
)


class UserProfile(Base):
    __tablename__ = 'user_profile'  #登陆堡垒机的用户表
    id = Column(Integer,primary_key=True,autoincrement=True)
    username = Column(String(32),unique=True,nullable=False)
    password = Column(String(128),unique=True,nullable=False)

    groups = relationship('Group',secondary=Group2UserProfile)  #堡垒机用户对应的主机组
    bind_hosts = relationship('BindHost',secondary=BindHost2UserProfile)  #堡垒机用户绑定的主机id,主机用户id
    audit_logs = relationship('AuditLog')  #堡垒机用户对应的日志信息

    def __repr__(self):
        return "<UserProfile(id='%s',username='%s')>" % (self.id,self.username)

class RemoteUser(Base):      #远端机器用户信息表
    __tablename__ = 'remote_user'
    AuthTypes = [
        (u'ssh-passwd',u'SSH/Password'),
        (u'ssh-key',u'SSH/KEY'),
    ]
    id = Column(Integer,primary_key=True,autoincrement=True)
    auth_type = Column(ChoiceType(AuthTypes))
    username = Column(String(64),nullable=False)
    password = Column(String(255))

    __table_args__ = (UniqueConstraint('auth_type', 'username','password', name='_user_passwd_uc'),)  #认证类型，用户名，密码，联合唯一

    def __repr__(self):
        return "<RemoteUser(id='%s',auth_type='%s',user='%s')>" % (self.id,self.auth_type,self.username)


class Host(Base):           #主机信息表
    __tablename__ = 'host'
    id = Column(Integer,primary_key=True,autoincrement=True)
    hostname = Column(String(64),unique=True,nullable=False)
    ip_addr = Column(String(128),unique=True,nullable=False)
    port = Column(Integer,default=22)

    bind_hosts = relationship("BindHost")  #主机信息对应主机id，主机用户id
    def __repr__(self):
        return "<Host(id='%s',hostname='%s')>" % (self.id,self.hostname)

class Group(Base):         #主机组表
    __tablename__ = 'group'
    id = Column(Integer,primary_key=True)
    name = Column(String(64),nullable=False,unique=True)

    bind_hosts = relationship("BindHost",secondary=BindHost2Group, back_populates='groups' ) #主机组对应绑定的主机信息
    user_profiles = relationship("UserProfile",secondary=Group2UserProfile )     #主机组对应绑定的堡垒机登陆帐号

    def __repr__(self):
        return "<HostGroup(id='%s',name='%s')>" % (self.id,self.name)


class BindHost(Base):  #主机绑定多个登陆用户表，这里是host表的host_id和 remote_user表的host_id对应，即是：我这台主机host_id对应哪几个用户remoteuser_id可以登陆
    '''Bind host with different remote user,
       eg. 192.168.1.1 mysql passAbc123
       eg. 10.5.1.6    mysql pass532Dr!
       eg. 10.5.1.8    mysql pass532Dr!
       eg. 192.168.1.1 root
    '''
    __tablename__ = 'bind_host'
    id = Column(Integer,primary_key=True,autoincrement=True)
    host_id = Column(Integer,ForeignKey('host.id'))   #主机id
    remoteuser_id = Column(Integer,ForeignKey('remote_user.id'))  #登陆远端主机用户id

    host = relationship("Host")  #关联Host类
    remoteuser = relationship("RemoteUser") #关联RemoteUser 类
    groups = relationship("Group",secondary=BindHost2Group,back_populates='bind_hosts')  #绑定主机组，指定中间表BindHost2Group
    user_profiles = relationship("UserProfile",secondary=BindHost2UserProfile) #绑定堡垒机用户
    audit_logs = relationship('AuditLog') #绑定日志记录

    __table_args__ = (UniqueConstraint('host_id', 'remoteuser_id', name='_bindhost_and_user_uc'),)  #联合唯一，主机id，远程用户id

    def __repr__(self):
        return "<BindHost(id='%s',hostname='%s',remoteuser='%s',auth_type='%s')>" % (self.id,
                                                           self.host.hostname, #理解为反射到Host类，调用hostname
                                                           self.remoteuser.username, #理解为反射到remoteuser类，调用username
                                                           self.remoteuser.auth_type  #理解为反射到remoteuser类，调用auth_type
                                                                      )

class AuditLog(Base):
    __tablename__ = 'audit_log'
    id = Column(Integer,primary_key=True)
    user_id = Column(Integer,ForeignKey('user_profile.id'))  #堡垒机用户id
    bind_host_id = Column(Integer,ForeignKey('bind_host.id'))  #对应的主机id
    action_choices = [
        (0,'CMD'),
        (1,'Login'),
        (2,'Logout'),
        (3,'GetFile'),
        (4,'SendFile'),
        (5,'Exception'),
    ]
    action_choices2 = [
        (u'cmd',u'CMD'),
        (u'login',u'Login'),
        (u'logout',u'Logout'),
        #(3,'GetFile'),
        #(4,'SendFile'),
        #(5,'Exception'),
    ]
    action_type = Column(ChoiceType(action_choices2))
    #action_type = Column(String(64))
    cmd = Column(String(255))
    date = Column(DateTime)

    user_profile = relationship("UserProfile")
    bind_host = relationship("BindHost")

    '''def __repr__(self):
        return "<user=%s,host=%s,action=%s,cmd=%s,date=%s>" %(self.user_profile.username,
                                                      self.bind_host.host.hostname,
                                                              self.action_type,
                                                              self.date)
    '''
'''
class AuditLog(models.Model):
    session = models.ForeignKey(SessionTrack)
    user = models.ForeignKey('UserProfile')
    host = models.ForeignKey('BindHosts')
    action_choices = (
        (0,'CMD'),
        (1,'Login'),
        (2,'Logout'),
        (3,'GetFile'),
        (4,'SendFile'),
        (5,'exception'),
    )
    action_type = models.IntegerField(choices=action_choices,default=0)
    cmd = models.TextField()
    memo = models.CharField(max_length=128,blank=True,null=True)
    date = models.DateTimeField()


    def __unicode__(self):
        return '%s-->%s@%s:%s' %(self.user.user.username,self.host.host_user.username,self.host.host.ip_addr,self.cmd)
    class Meta:
        verbose_name = u'审计日志'
        verbose_name_plural = u'审计日志'

'''

if __name__ == '__main__':
    DB_CONN ="mysql+pymysql://root:123456@localhost:3306/little_finger"
    engine = create_engine(DB_CONN,echo=False)
    #Base.metadata.create_all(engine)  #创建全部表

    SessionCls = sessionmaker(bind=engine) #创建与数据库的会话session class ,注意,这里返回给session的是个class,不是实例
    session = SessionCls()
    #h1 = session.query(Host).filter(Host.hostname=='ubuntu4').first()
    #hg1 = session.query(HostGroup).filter(HostGroup.name=='t2').first()

    # h2 = Host(hostname='ubuntu4',ip_addr='192.168.1.21')
    # h3 = Host(hostname='ubuntu5',ip_addr='192.168.1.24',port=20000)
    # session.add_all([h2,h3])
    #
    # hg1= Group(name='TestServers3',host_id=h3.id)
    # hg2= Group(name='TestServers2',host_id=h2.id)
    # hg3= Group(name='TestServers3')
    # hg4= Group(name='TestServers4')
    # session.add_all([hg1,hg2,hg3,hg4])
    #
    # h2.host_groups = [HostGroup(name="t1"),HostGroup(name="t2")]
    # h3.host_groups = [HostGroup(name="t2")]
    # h1.host_groups.append(HostGroup(name="t3") )
    # print(h1.host_groups)
    # print("hg1:",hg1.host.hostname)
    # join_res = session.query(Host).join(Host.host_groups).filter(HostGroup.name=='t1').group_by("Host").all()
    # print('join select:',join_res)
    # group_by_res = session.query(HostGroup, func.count(HostGroup.name )).group_by(HostGroup.name).all()
    # print("-------------group by res-----")

#--------------------------------------------------------------------------------------
    # h1=Host(hostname='h1',ip_addr='1.1.1.1')
    # h2=Host(hostname='h2',ip_addr='1.1.1.2')
    # h3=Host(hostname='h3',ip_addr='1.1.1.3')
    #
    #r1=RemoteUser(auth_type=u'ssh-passwd',username='alex',password='abc123')
    #r2=RemoteUser(auth_type=u'ssh-key',username='test')
    #
    # g1 = Group(name='g1')
    # g2 = Group(name='g2')
    # g3 = Group(name='g3')
    # session.add_all([h1,h2,h3,r1,r2])  #增加主机信息，remoteuser信息
    # session.add_all([g1,g2,g3])        #增加组

    #
    #
    # b1 = BindHost(host_id=1,remoteuser_id=1)
    # b2 = BindHost(host_id=1,remoteuser_id=2)
    # b3 = BindHost(host_id=2,remoteuser_id=2)
    # b4 = BindHost(host_id=3,remoteuser_id=2)
    # session.add_all((b1,b2,b3,b4)) #增加主机对应的登陆用户信息

    all_groups = session.query(Group).filter().all() #first()
    #all_groups = session.query(Group).filter().first()
    all_bindhosts = session.query(BindHost).filter().all()
    #
    h1 = session.query(BindHost).filter(BindHost.host_id==1).first()
    print(all_bindhosts)
    print(all_groups)

    #h1.groups.append(all_groups[1])  #指定h1 对应的组，中间表bindhost_2_group 会自动生成一条记录，bindhost_id -->group_id
    #print("h1:",h1)
    #print("h1:",h1.groups)  #打印h1 对应group表的信息
    #print("----------->",all_groups.name,all_groups.bind_hosts)


    # u1 = UserProfile(username='alex',password='123')  #增加堡垒机用户
    # u2 = UserProfile(username='rain',password='abc!23')  #增加堡垒机用户
    # session.add_all([u1,u2]) #增加堡垒机用户


    #u1 = session.query(UserProfile).filter(UserProfile.id==1).first()  #查找堡垒机用户id为1的用户
    #print('--user:',u1.bind_hosts)
    #print('--user:',u1.groups[0].bind_hosts)

    #u1.groups = [all_groups[1] ]  #增加堡垒机用户对应的主机组_id，会自动在group_2_userprofile表生成一条记录 userprofile_id  --> group_id
    #u1.bind_hosts.append(all_bindhosts[1])  #增加堡垒机用户对应的bindhost_id，会自动在bindhost_2_userprofile表生成一条记录 bindhost_id --> uerprofile_id



    #b1 = BindHost()
    session.commit()
    #print(h2.host_groups)


