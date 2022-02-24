
## kibana 部署说明

kibana 部署非常简单，只需要 2 步：

### 第一步：修改配置项

拷贝或直接修改 kibana.cfg 配置文件，填写对应的 es 集群版本，部署服务器地址.. 等信息。

### 第二步：一键安装

```
ansible-playbook -i kibana.cfg kibana.yml -v
```

### 几点说明

1. 如需通过 Nginx 等代理访问 Kibana 服务，请打开配置文件中的 server_base_path 选项。
