# aecccloud 集成
用于监测AECC设备数据的传感器集成，支持实时数据更新。

## 安装步骤
1. 打开HACS商店，搜索“aecccloud”并安装。
2. 重启Home Assistant。

## 配置示例
在`configuration.yaml`中添加：
  ```yaml
  ha_aecc_cloud:
    api_key: "你的设备API密钥"
