# RASA2.X版本对话机器人demo

一个基于rasa2.2.x版本的对话机器人，以调用心知天气api查询天气为例介绍该对话引擎的基础用法。

## 使用流程

rasa的训练使用流程比较简单，进入初始化好（rasa init）的工作路径中，

先使用rasa train训练，以本demo为例

```shell
rasa train -c configs.yml -d domain.yml --data data/demo/
```

再使用rasa run actions 启用后端服务

```shell
rasa run actions
```

再使用 rasa run --enable-api 就可以启用rasa服务

```shell
rasa run --log-file out.log --enable-api --endpoints endpoints.yml
```

建议使用postman测试，常用的测试指定[见链接](https://zhuanlan.zhihu.com/p/87747660)。

当然，debug时建议使用rasa run --debug。

```shell
rasa shell --debug
```

关于rasa的指令说明，[见链接](https://rasa.com/docs/rasa/command-line-interface)。

测试示例

```shell
Your input ->  上海的天气  
查询结果为：
            上海的天气情况为：多云，气温：4-15 °C
Your input ->  好的，我先走了
再见，Enjoy!

Your input ->	 你好
你好
```



## 详细介绍

在终端输入rasa init指令后rasa将为你自动创建一个workspace。每个部分的说明如下：

### actions：

用于自定义custom_actions操作，此demo中包含了一个自定义的查询心知天气api的动作，[详细介绍](https://rasa.com/docs/action-server/sdk-actions)

### data: 

训练数据路径，其中**nlu.yml**为标注好的训练数据，包含**intent**和**entity**，示例如下：

```yml
version: "2.0"
nlu:

# 意图数据标注格式
- intent: greet
  examples: |
    - 你好
    - 你好，rasa
    - 早上好
    - 中午好
    - 晚上好
    - 你好呀

- intent: goodbye
  examples: |
    - 再见!
    - 拜拜!
    - 88!
    - 拜！
    - 下次见。
    - 下次再见

# 实体数据标注格式，可以同时标注多个实体，rasa将自动按照格式进行解析
- intent: weather
  examples: |
    - [上海](location)的天气 
    - [上海](location)明天的天气
    - [上海](location)昨天的天气
    - [上海](location)前天的天气
    - 下个星期五[南京](location)的天气
```

rules.yml为一些对话模块的强规则，示例如下：

```yml
version: "2.0"

rules:

- rule: Say goodbye anytime the user says goodbye
  steps:
  - intent: goodbye
  - action: utter_goodbye
```

stories.yml为对话的流程，示例如下：

```yml
version: "2"
stories:

# 表示当意图为weather时，将触发操作action_report_weather
- story: weather_story
  steps:
    - intent: weather
    - action: action_report_weather
```

⚠️：action_report_weather这个名字（action.name属性）必须和custom_actions中的一致，且如果要将查询结果返回给user时，要在custom_actions中使用dispatcher.utter_message(text='XXXXXX')方法；若要将结果填入槽中，则需要使用SlotSet，SlotSet的意思是将结果填入slot中返回，user可以根据slot的结果进行其他操作，所以必须**显式**的在**domain.yml**中指定该slot，然后读取时在domain中使用{slotname}。

### models

NLU模型保存的路径，若不指定路径信息，rasa每次将调用最新的参数文件

### results

NLU模型测试结果

### tests

测试对话机器人功能

## 配置文件

### configs.yml

该文件主要指定训练NLU的方式（pipline），示例如下：

```yml
language: "zh"

pipeline:
  - name: "MitieNLP" # 预训练语言模型
    model: "data/total_word_feature_extractor_zh.dat" # 词向量的参数路径
  - name: "JiebaTokenizer" # 分词器
  - name: "MitieEntityExtractor" # NER模块
  - name: "MitieFeaturizer" # 特征模版，NER用
  - name: "MitieIntentClassifier" # Intent模块

# 指定对话管理策略，目前没有涉及
# policies:
# # No configuration for policies was provided. The following default policies were used to train your model.
# # If you'd like to customize them, uncomment and adjust the policies.
# # See https://rasa.com/docs/rasa/policies for more information.
#   - name: MemoizationPolicy
#   - name: TEDPolicy
#     max_history: 5
#     epochs: 100
#   - name: RulePolicy
```

### domain.yml

该文件指定了rasa机器人的一系列操作域，如：意图类别（intents），实体类别（entities），槽值（slots），动作(actions)，回复模版（responses）还有会话流程管理（session_config）。

```yml
version: "2.0"

intents:
  - greet
  - goodbye
  - weather

slots:
  location:
    type: text
  # matches:
  #   type: any ## 需要缓存一个槽值，用于缓存返回的结果，或者用dispatcher见一个队列返回，见 https://github.com/RasaHQ/rasa-demo/blob/master/actions/actions.py

entities:
  - location

actions:
  - action_report_weather ## 一个只负责写

responses:
  utter_greet:
  - text: 你好
  utter_goodbye:
  - text: 再见，Enjoy!
  # utter_report_weather:
  # - text: "{matches}"

session_config:
  session_expiration_time: 60
  carry_over_slots_to_new_session: true
```

### endpoints.yml

这个文件主要调用后端sdk服务用，rasa run actions会在本地启用这个http服务

```yml
action_endpoint:
  url: "http://localhost:5055/webhook"
```

## 中文词向量参数文件

链接: https://pan.baidu.com/s/1HnFyKdTdT4yjAhdCLZg0vA  密码: fsvi
下载后放置/data路径中
## TODO

