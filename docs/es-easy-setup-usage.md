## 介绍

es-easy-setup 基于 [Ansible](https://www.ansible.com/) 开发，支持快速部署生产环境可用 es 集群。

## 使用说明

## 如何部署 mix 集群（测试集群）

mix 集群不单独部署 `maste/data/client` 角色节点，一个节点可以混合扮演多个角色，这种形式集群通常用于测试环境及非高可用集群。生产环境不建议使用。

`vars` 目录下新增了 `mix.yml`，用于配置 mix 节点通用选项。

`example.cfg` 配置文件下删除 `[master], [data], [client]` 配置组，放开 `[mix]` 组配置（默认被注释，不建议 mix 和其他配置组同时使用）。

合理配置 `minimum_master_nodes `值（`master` 角色节点数 / 2 + 1）。

默认每个 mix 节点都开启了 `master、data、client` 角色。

其他流程不变。

## 如何基于同一套 es-easy-setup 部署多个集群

多个部署集群部署流程完全一致，只是各集群配置项可能会有所不同。

es-easy-setup 配置项集中在 `vars` 目录和 `example.cfg` 中。

部署某个集群时，只需要将 `vars` 和 `example.cfg` 拷贝一份（可放至任何目录，但两者必须放在一起），修改配置项至需要值，然后多个集群用同一份 `setup.yml` 执行部署即可。

**es-easy-setup 首先会读取 `example.cfg` 所在本地的 `vars` 配置，如果没有再去读取 `setup.yml` 所在目录的 `vars` 配置。**

## 是否支持单个节点添加多个自定义配置选项

支持，多个选项间空格分开。如：

```yaml
[master]
# 指定其他参数例子
m1  ansible_host=10.201.113.5 node_master=true node_data=true http_port=9201 transport_port=9301 node_name=example
```

## 如何关闭某些 mix 节点的 `master/data` 角色

关闭 `master` 角色：`example.cfg` 配置文件 → `[mix]` 配置组 → 具体的某个节点 `host` → 在后面添加 `node_master=false`

关闭 `data` 角色：`node_data=false`，其他与上同理。

关闭 `master` 角色后，部署的 `unicast_host` 配置即不会包含这个节点地址。

## 如何单独配置某些节点的端口

在目标节点后面添加相关选项，如：`http_port=10601 transport_port=10701`

## 如何自定义某个节点名称

默认情况下，节点名称以 `节点类型+节点在配置组中序列号` 为前缀，如每个机器部署多个节点，则再加后缀 `_序号` 区分（完整名称如：`master0，client1，data0_1，data2_2`）。

用户可以自定义节点名称前缀，方法：在目标节点后添加配置项 `node_name=my_example_name`

## 多机房部署如何在节点名称前面添加机房前缀

多机房（或多可用域）部署时，指定节点 `node_zone` 属性即可。

譬如部署 3 机房机器，机房1：`az1`，机房2：`az2`，机房3：`az3`

`example.cfg` 配置文件中指定:

```yaml
node_zones = ["az1", "az2", "az3"]

[master]

m1  ansible_host=10.12.3.4 node_zone="{{ node_zones[0] }}"

m2  ansible_host=10.12.3.5 node_zone="{{ node_zones[1] }}"

m3  ansible_host=10.12.3.6 node_zone="{{ node_zones[2] }}"

[data]

d1  ansible_host=10.12.3.4 node_zone="{{ node_zones[0] }}"

d2  ansible_host=10.12.3.5 node_zone="{{ node_zones[1] }}"

[client]

c1  ansible_host=10.12.3.4 node_zone="{{ node_zones[0] }}"

c2  ansible_host=10.12.3.5 node_zone="{{ node_zones[1] }}"
```

则最终生成的各节点名称为：

```yaml
az1_master0, az2_master1, az3_master2

az1_data0_0, az2_data1_0

az1_client0, az2_client1
```

## 每个主机前 `m1,d1,c1,x1` 等标识及 `ansible_host` 意义

由于 Ansible 会自动覆盖相同主机名的主机参数，为了各个配置组下同名主机都能拥有独自配置，因此在每个主机前面加上 `m1,m2,c1` 等标识符便于区分，并使用 `ansible_host` 标明真正的主机地址。

标识符无实际意义，可以自由指定，但要求主机前标识符全局内唯一。

