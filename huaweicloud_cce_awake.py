#################################################################
# Author: Horikian, Leonardo (leonardo.horikian@huawei.com)     #
# Team: Huawei Cloud Team Argentina                             #
# Description: Script to Awake a CCE cluster                    #
#              (Master and Workers Nodes).                      #
# Date: 08-September-2022                                       #
# Version: 1.0                                                  #
#################################################################
from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkcce.v3.region.cce_region import CceRegion
from huaweicloudsdkecs.v2.region.ecs_region import EcsRegion
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkcce.v3 import *
from huaweicloudsdkecs.v2 import *
import time, ast

def cce_awake_cluster(cce_client, cluster_id):
    try:
        request = AwakeClusterRequest()
        request.cluster_id = cluster_id
        response = cce_client.awake_cluster(request)
        while(True):
          time.sleep(5)
          status = cce_status_cluster(cce_client, cluster_id)
          if status == 'Available':
            break
        return status
    except exceptions.ClientRequestException as e:
        print(e.status_code)
        print(e.request_id)
        print(e.error_code)
        print(e.error_msg)

def cce_status_cluster(cce_client, cluster_id):
    try:
        request = ShowClusterRequest()
        request.detail = "false"
        request.cluster_id = cluster_id
        response = cce_client.show_cluster(request)
        response_obj = response.to_json_object()
        return response_obj["status"]["phase"]
    except exceptions.ClientRequestException as e:
        print(e.status_code)
        print(e.request_id)
        print(e.error_code)
        print(e.error_msg)

def cce_list_nodes(cce_client, cluster_id):
    try:
        request = ListNodesRequest()
        request.cluster_id = cluster_id
        response = cce_client.list_nodes(request)
        response_obj = response.to_json_object()
        index = 0
        ListServerId = []
        for x in response_obj["items"]:
          ListServerId.append("{\"id\": \"" + response_obj["items"][index]["status"]["serverId"] + "\"}")
          index = index+1
        ListServerId = [ast.literal_eval(i) for i in ListServerId]
        return ListServerId
    except exceptions.ClientRequestException as e:
        print(e.status_code)
        print(e.request_id)
        print(e.error_code)
        print(e.error_msg)

def ecs_batch_start(cce_client, ecs_client, cluster_id):
    try:
        request = BatchStartServersRequest()
        listServersOsstart = cce_list_nodes(cce_client, cluster_id)
        osstartbody = BatchStartServersOption(servers=listServersOsstart)
        request.body = BatchStartServersRequestBody(os_start=osstartbody)
        response = ecs_client.batch_start_servers(request)
    except exceptions.ClientRequestException as e:
        print(e.status_code)
        print(e.request_id)
        print(e.error_code)
        print(e.error_msg)

if __name__ == "__main__":
    ak = ""
    sk = ""
    region = ""
    project_id = ""
    cluster_id = ""

    credentials = BasicCredentials(ak, sk, project_id) \

    cce_client = CceClient.new_builder() \
            .with_credentials(credentials) \
            .with_region(CceRegion.value_of(region)) \
            .build()    
    awake_cluster_status_code = cce_awake_cluster(cce_client, cluster_id)

    if awake_cluster_status_code == 'Available':
      ecs_client = EcsClient.new_builder() \
             .with_credentials(credentials) \
             .with_region(EcsRegion.value_of(region)) \
             .build()
    ecs_batch_start(cce_client, ecs_client, cluster_id)
