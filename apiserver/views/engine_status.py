#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/8/4 16:47
# software: PyCharm
# project: webapi
import logging
import time

from dongtai_models.models.agent import IastAgent

from AgentServer.base import R
from apiserver.base.openapi import OpenApiEndPoint

logger = logging.getLogger("django")


class EngineUpdateEndPoint(OpenApiEndPoint):
    name = "iast_engine_update_status_edit"
    description = "IAST 检测引擎更新状态修改接口"

    def get(self, request, status=None):
        """
        IAST 检测引擎 agent接口
        :param request:
        :return:
        """
        agent_name = request.query_params.get('agent_name')
        agent = IastAgent.objects.filter(user=request.user, token=agent_name).first()
        if not agent:
            return R.failure("agent不存在或无权限访问")

        if status:
            if agent.is_control == 1:
                agent.control = status
                agent.is_control = 0
                agent.latest_time = int(time.time())
                agent.save()
                return R.success(msg="安装完成")
            else:
                return R.failure(msg="引擎正在被安装或卸载，请稍后再试")
        else:
            if agent.control == 1 and agent.is_control == 0:
                agent.is_control = 1
                agent.latest_time = int(time.time())
                agent.save()
                return R.success(data=agent.control)
            else:
                return R.failure(msg="不需要更新或正在更新中")


class EngineStopStart(OpenApiEndPoint):
    name = "iast_engine_update_status_edit"
    description = "IAST 检测引擎更新状态修改接口"

    def get(self, request):
        """
        IAST 检测引擎 agent接口
        :param request:
        :return:
        """
        agent_name = request.query_params.get('agent_name')
        agent = IastAgent.objects.filter(user=request.user, token=agent_name).first()
        if not agent:
            return R.failure("agent不存在或无权限访问")
        
        if agent.is_control ==0:
            return R.failure(msg="暂无命令", data="notcmd")

        #启动
        if agent.control == 3:
            agent.is_control = 0
            agent.is_core_running = 1
            agent.latest_time = int(time.time())
            agent.save()
            return  R.success(data="start", msg=str(agent.is_running)+agent.token)
        #暂停
        if agent.control == 4:
            agent.is_control = 0
            agent.is_core_running = 0
            agent.latest_time = int(time.time())
            agent.save()
            return  R.success(data="stop")
        return  R.success(data="notcmd")