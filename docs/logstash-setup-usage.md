
## logstash 部署说明

logstash 部署非常简单，只需要 2 步：

### 第一步：修改配置项

拷贝或直接修改 logstash.cfg 配置文件，填写  对应的 es  集群版本，部署服务器地址.. 等信息。

### 第二步：一键安装

```
ansible-playbook -i logstash.cfg logstash.yml -v
```

### 几点说明

1. logstash 可配置多个 pipeline，只要配置不同的 pipeline_name 即可。部署后每个 pipeline 拥有独立的配置目录。（比如可用于消费不同的 kafka 集群）
2. logstash 默认配置的消费端为 kafka，写入端为 es。
