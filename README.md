# Huawei Cloud - CCE Service - Awake/Hibernate Master and Workers Nodes

## Requirements

The scripts uses the following SDK's from Huawei Cloud Repository -> https://github.com/huaweicloud/huaweicloud-sdk-python-v3
```
huaweicloud-sdk-cce
huaweicloud-sdk-ecs
huaweicloud-sdk-core
```

Set the following variables in the main function of each script.
```
AK : Access Key of your Huawei Cloud account
SK : Secret Key of your Huawei Cloud account
REGION : Region of your Huawei Cloud account
PROJECT_ID : Project Id of your Huawei Cloud account
CLUSTER_ID : Cluster Id of the CCE cluster you want to awake/hibernate
```

## Description

The Python Scripts allows to Awake and Hibernate a CCE cluster (Master and Workers Nodes) in a particular Project/Region.

## Execution

Awake a CCE cluster
```
python3 huaweicloud_cce_awake.py
```
Hibernate a CCE cluster
```
python3 huaweicloud_cce_hibernate.py
```

Enjoy!
