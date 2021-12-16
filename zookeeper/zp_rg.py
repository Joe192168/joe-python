#!/usr/bin/env python
# -*- coding: utf-8 -*

import time
import random
import logging
from kazoo.client import KazooClient
from kazoo.exceptions import NodeExistsError
from kazoo.client import KazooState

logger = logging.getLogger(__name__)


class ServiceRegister:
    """
    hosts:  the connection string for zk server, such as
            '10.0.1.1:2181,10.0.1.2:2181'
    The object should be created after service has been started successfully.
    """

    ZOOKEEPER_CONFIG = {"zk_server": "127.0.0.1:2181", "zk_auth_data": "注册"}
    HOST_CONFIG = {"zk_path": "zk", "host": "192.168.0.12", "port": "8080"}

    def __init__(self):

        self._hosts = self.ZOOKEEPER_CONFIG["zk_server"]
        self._zk_path = self.HOST_CONFIG["zk_path"]
        self._zk = None
        self.start_zk()

    def start_zk(self):
        self._info = self._zk_path + '/' + self.HOST_CONFIG["host"] + ':' + self.HOST_CONFIG["port"]
        self._zk = None
        try:
            self._zk = KazooClient(self._hosts, auth_data=self.ZOOKEEPER_CONFIG["zk_auth_data"], logger=logger)
            self._zk.start()
        except Exception as start_zk_e:
            logger.error('Fail to connect to zk hosts %s, exception %s' %
                         (self._hosts, start_zk_e))
            self._zk = None
            raise start_zk_e

        def zk_listener(state):
            logger.info('注册 到 zookeeper')
            if state == KazooState.CONNECTED:
                # Handle being connected/reconnected to Zookeeper
                logger.debug('reconnect to zookeeper')
                try:
                    self.start_zk()
                    self.register()
                except Exception as e:
                    logger.error('Fail to register info %s, exception %s' %
                                 (self._info, e))
                    self._zk.stop()
                    self._zk = None
                    time.sleep(5)
            else:
                logger.debug('zk_listener state %s' % state)

        logger.info('add_listener to zookeeper')
        self._zk.add_listener(zk_listener)

    def create_znode(self):
        def retryCreateNode(self):
            print('重试')
            self.register()

        """
        create an ephemeral and not sequence node in root with service info
        :param info: znode info including ip and port
        """
        logger.info('1111')
        try:
            self._zk.ensure_path(self._zk_path)
            path = self._zk.create(self._info,
                                   value=b"{\'title\':\'test\'}",
                                   ephemeral=True,
                                   sequence=False)
            children = self._zk.get_children(self._zk_path, watch=retryCreateNode(self))
            # self._zk.stop
        except Exception as e:
            logger.error('Fail to register info %s, exception %s' %
                         (self._info, e))
            return False, ""
        return True, path

    def register(self):
        # When worker start, register on zookeeper forever
        logger.info('注册')
        flag = True
        while flag:
            if not self._zk.exists(self._info):
                success, path = self.create_znode()
                if success:
                    flag = False
                    logger.info('register on %s; hosts %s end' %
                                (path, self._hosts))
            # zookeeper syncLimit=5
            time.sleep(5)

    def create_zone(self, zone):
        """
        create zone in cluster
        If the zone is already exist, do nothing, else create
        the given zone path.
        """
        try:
            self._zk.create(zone, 'zone of %s' % zone, makepath=True)
        except NodeExistsError:
            pass
        except Exception as e:
            logger.error('Fail to create zone %s' % e)
            raise e
        pass

    def get_zk_children(self, _zk_path):
        try:
            self._zk_path = '/BD/services/' + _zk_path
            self._zk = KazooClient(self._hosts, auth_data=self.ZOOKEEPER_CONFIG["zk_auth_data"], logger=logger)
            self._zk.start()
            if self._zk.exists(self._zk_path):
                children = self._zk.get_children(self._zk_path)
            else:
                result = {
                    "success": False,
                    "message": _zk_path + "服务获取失败",
                    "data": None,
                    "failed": True
                }
                return result
            return children
        except Exception as e:
            logger.error('Fail to get children %s' % e)
            raise e

    def get_service(self, _zk_path):
        """
        获取单个服务
        """
        children = self.get_zk_children(_zk_path)
        if not children:
            raise Exception("获取zk中的 %s 服务失败！" % _zk_path)
        choice = random.sample(children, 1)
        result = {
            "success": True,
            "message": _zk_path + "服务获取成功",
            "data": 'http://' + choice[0] + '/',
            "failed": False
        }
        self._zk.stop()
        return result

    def get_services(self, _zk_path, k=0):
        """
        获取多个服务，k为获取指定数量的服务
        如果k为0或者为None 则返回目录下全部服务
        """
        children = self.get_zk_children(_zk_path)
        if not k or k > len(children):
            k = len(children)
        choice = random.sample(children, k)
        data = list()
        for item in choice:
            data.append('http://{url}/'.format(url=item))
        result = {
            "success": True,
            "message": _zk_path + "服务获取成功",
            "data": data,
            "failed": False
        }
        self._zk.stop()
        return result

    def is_slave(self):
        return not self.is_master

if __name__ == '__main__':
    reg = ServiceRegister()
    reg.register()