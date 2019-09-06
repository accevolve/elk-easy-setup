# 一键部署高可用 Elasticsearch 集群

![](https://img.shields.io/badge/ansible-%3E%3D2.5-red) ![](https://img.shields.io/badge/elasticsearch-5.x%2C%206.x-9cf) ![](https://img.shields.io/badge/license-Apache--2.0-brightgreen)

> 1. 此安装部署程序运行环境要求： Ansible >= 2.5（es 部署节点无须安装，只需确保有 SSH 登录权限）  
> 2. 目前支持部署的 es 版本：5.x, 6.x

## :rocket: 快速使用说明

### 第一步：修改配置项

拷贝或直接修改 `example.cfg` 配置文件，填写 `集群名称`、`es 版本..` 等信息。

### 第二步：节点 `ES_HEAP_SIZE` 配置

如必要，修改 `vars` 目录下，节点角色对应名称配置文件的 `jvm_heap_size` 默认值至自定义大小。

> 如 `master` 角色节点修改 `master.yml` 文件，`mix` 节点修改 `mix.yml` 文件，文件中其他配置项按需也可以修改。所有相同角色节点使用相同配置。

### 第三步：一键安装

```shell
ansible-playbook -i example.cfg setup.yml -v
```

### 第四步：启动集群

安装完毕后进入 `/home/<部署用户>/elk/elasticsearch`目录，内含 `start_elasticsearch.sh` 启动脚本。执行 `sh start_elasticsearch.sh` 命令启动 es 服务即可。

### 第五步：部署完毕

执行到这里部署就已经完毕了！可以使用 `GET /_cat/health?v` 等命令确认集群服务是否正常。ENJOY!

## :fire: 其他事项

1. 关于**节点角色**说明：如果部署的集群为`生产环境`使用，建议区分 es 节点角色 `master/data/client`，性能和稳定性更好。如果部署的集群为`测试环境`使用或仅为`功能验证`，希望尽量节省资源，对稳定性和性能无要求，可以使用 `mix` 模式集群（在配置文件中删除 `[master]/[data]/[client]` 配置）。

2. 安装程序会自动下载并安装配置 `Oracle JDK_1.8` 环境，如果已有现成的 Java 运行环境，可以在安装命令中添加如下选项跳过：
```shell
--skip-tags java
```

3. 如果当前用户 session 的 java 环境未生效（如找不到 Java 命令），可能是当前用户在安装部署前已登录，可以手动执行一下 `source ~/.profile` 命令，重新加载 Java 配置。

4. 安装过程中首先会对**目标节点系统配置**进行检查，以确认是否能满足 es 部署要求。检查项包括 [Elasticsearch 官方要求满足的系统配置项](https://www.elastic.co/guide/en/elasticsearch/reference/current/system-config.html)，以及`磁盘 io 调度策略`及`磁盘文件系统类型`。如想跳过`磁盘 io 调度策略`及`磁盘文件系统类型`检测，可以添加 skip tags：
```shell
--skip-tags scheduler,filesystem
```

5. 如果上一步检查中的 es 官方要求系统配置项不通过，且安装部署的用户具有 `sudo` 权限，则可以在安装命令中添加 tags 来要求用安装程序自动配置 Elasticsearch 官方要求的系统配置项。否则需要提前配置完毕。tags 如下：
```shell
--tags superuser,all
```

6. 集群已默认安装[开源 IK 中文分词器](https://github.com/medcl/elasticsearch-analysis-ik)，如不需要，可使用 skip tags 跳过：
```
--skip-tags ik
```

---

更多安装部署程序介绍及高级用法还可以参考：[这里](./docs/es-easy-setup-usage.md)。

## :memo: License

This project is [Apache 2.0](./LICENSE) licensed.

