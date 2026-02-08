
文档中心
豆包语音
扣子
火山方舟大模型服务平台
API网关
云服务器
豆包语音
扣子
火山方舟大模型服务平台
API网关
云服务器
文档
备案
控制台
z
zhaoweibo.0820 / eps_yxd_group
账号管理
账号ID : 2108323502
联邦登陆
企业认证
费用中心
可用余额¥ 0.00
充值汇款
账户总览
账单详情
费用分析
发票管理
权限与安全
安全设置
访问控制
操作审计
API 访问密钥
工具与其他
公测申请
资源管理
配额中心
伙伴控制台
待办事项
待支付
0
待续费
0
待处理工单
0
未读消息
0
联网问答Agent
文档指南
请输入

文档首页

联网问答Agent

API参考

智能体API

智能体会话API

复制全文
我的收藏
智能体会话API
本文档介绍智能体会话API接口的输入输出参数。调用该接口可获取智能体的大模型回复、参考资料、富媒体卡片数据，实现追问、引用角标、图文混排、百科划线词等高级产品功能。​
​
接口限流：火山账号维度，默认300 RPM。​
​
认证方式​
提供APIKey接入和TOP网关接入两种方式，两种接入方式有不同的URL。​
APIKey接入(推荐)​
获取API Key​
打开并登录联网问答智能体-APIKey 管理。​
单击【联网问答Agent】页进入并创建API Key按钮。​
在弹出的名称文本框中填写API Key 名称，单击创建。​
说明：请妥善保存好API Key，强烈建议您不要将其直接写入到调用模型的代码中。​
签名构造​
API Key 签名鉴权方式要求在 HTTP 请求 header 中按如下方式添加 Authorization:​
​
Authorization: Bearer <API_KEY>​
​
注意：​
若使用APIKey接入，接口超时时间为30s。​
​
火山引擎TOP网关接入​
此接入方式基于火山引擎IAM的AK/SK鉴权，统一使用 ServiceName=volc_torchlight_api​
接口验签及请求公共参数逻辑遵循火山引擎官网的统一规范，详情请参见：签名方法--API签名调用指南-火山引擎；​
开通账号权限后，可获取AccessKey进行验签，详情请参见：Access Key(密钥)管理--API访问密钥(Access Key)-火山引擎。​
注意：​
若使用主账号接入，可跳过此步骤；(使用主账号有权限过大的风险，不建议直接使用)​
若使用子账号接入，需要首先登录控制台，开通接口访问权限；否则会报错100013:AccessDenied错误；​
开通接口权限步骤：​
使用火山引擎控制台主账号，登录控制台；​
点击用户头像进入访问控制模块，在用户模块点击管理按钮进入子账号权限管理界面；​
切换到权限TAB，点击添加权限按钮，在搜索栏输入“TorchlightApiFullAccess”权限，并选中确认；​
若有多个子账号访问平台，需对每个子账号进行相应权限配置。​
若使用火山引擎TOP网关接入，请求体整体长度不能超过8M，接口超时时间为30s。​
​
接口详情​
智能体会话​
URL​
​
URL​
APIKey接入：https://open.feedcoopapi.com/agent_api/agent/chat/completion​
TOP网关接入：https://mercury.volcengineapi.com?Action=ChatCompletion&Version=2024-01-01​
Method​
POST​
Content-Type​
application/json​
​
请求体ChatCompletionRequest​
​
参数​
类型​
必须​
描述​
bot_id​
String​
是​
智能体ID，在控制台创建智能体后获取​
messages​
​
Array[Message]​
​
是​
​
长度要求​
messages 数组不可为空​
我们最多使用传入的10条消息​
如果消息超过 10 条，则仅保留数组中最后 10 条消息​
特殊情况：如果第一个消息为 system 类型，则始终保留该消息​
上下文窗口越大，总结的上下文越全，但响应时间和消耗的Token也会变多，需根据实际场景合理选择​
示例​
单轮对话示例​
​
"messages": [ {"role": "user","content": "你好"}]​
​
多轮对话示例​
​
"messages": [ ​
    {"role":"system","content": "你是一个联网问答助手"},​
    {"role":"user","content": "你好"},​
    {"role":"assistant","content":"需要什么帮助"},​
    {"role":"user","content":"自我介绍下"}​
]​
​
stream​
Boolean​
否​
是否启用流式响应，默认 false（非流式）。建议流式调用。​
user_id​
String​
否​
用户身份标识​
device_id​
String​
否​
设备身份标识​
location_info​
LocationInfo​
否​
当前地理位置信息（使用出行工具时必传，其他情况选传）​
navigation_info​
NavigationInfo​
否​
当前导航信息（使用出行工具搜导航周边时必传）​
knowledge​
​
String​
否​
背景知识注入字段，需要带入环境信息、背景知识时使用​
​
"knowledge":"当前正在驾驶问界M8增程MAX版，车内正在播放音乐《天黑黑》"​
​
model​
​
String​
否​
默认无需传递​
model=thinking，开启深度思考模式​
model=auto_thinking，开启自动深度思考模式​
extension_options​
ExtensionOptions​
否​
扩展配置参数。在特定场景下开白启用，使用前请咨询销售/产解/售后同学。不承诺扩展参数在随意传入情况下的接口稳定返回。​
​
Message​
​
参数​
类型​
必须​
描述​
role​
​
String​
是​
user：表示用户的输入的问题或指令​
assistant：表示AI助手的回复​
system：SystemPrompt​
content​
​
String/Object​
​
是​
​
对话消息列表​
文本对话场景：​
​
"content": "You are a helpful assistant."​
​
多模态场景：​
多模态参数要求：​
图片张数：目前最多支持10张，超过10张会报参数错误​
数据类型：支持WebUrl和DataUrl​
建议使用Base64后的DataUrl，WebUrl需要下载，可能存在下载延迟和不稳定问题​
样例：​
WebUrl：https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg​
DataUrl：data:{MIME Type};base64,{base64_image}​
data:image/jpeg;base64,{base64_image}​
图片大小：​
推荐大小：<=500KB​
最大限制：​
WebUrl传入​
APIKey接入：单张图片大小<10M，超出会报参数错误​
TOP网关接入：请求体整体长度不能超过8M​
DataUrl传入​
APIKey接入：单张图片Base64编码后长度<20M，超出会报参数错误​
TOP网关接入：请求体整体长度不能超过8M​
单图片尺寸判断，如果图片超出下面的限制，会直接报错，传入图片满足下面条件（单位 px）：​
宽 > 14 且 高>14​
宽*高范围： [196, 36000000]​
​
"content": [​
  {​
    "type": "text",​
    "text": "What'\''s in this image?"​
  },​
  {​
    "type": "image_url",​
    "image_url": {​
      "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"​
    }​
  }​
]​
​
reasoning_content​
String​
否​
如果选择了深度思考模式，会在总结前输出模型的思考过程，通过此字段透出。​
​
LocationInfo​
​
参数​
类型​
必须​
描述​
备注​
province​
String​
否​
当前位置所在省份。天气/新闻/票务查询需传。​
组合传入（建议）​
参数传入哪一层级，则读取哪一层级返回总结​
city​
String​
否​
当前位置所在市。天气/新闻/票务查询需传。​
district​
String​
否​
当前位置所在区。天气/新闻类查询需传。​
town​
String​
否​
当前位置所在县/街道。天气/新闻类查询需传。​
longitude​
Number​
否​
当前位置经度。使用出行工具时必传，需与纬度组合传入。​
组合传入​
latitude​
Number​
否​
当前位置纬度。使用出行工具时必传，需与经度组合传入。​
​
NavigationInfo​
​
参数​
类型​
必须​
描述​
备注​
destination​
LocationInfo​
否​
目的地信息，搜导航周边时需传​
经纬度必传​
via​
Array[LocationInfo]​
否​
途经点信息，搜导航周边时需传​
经纬度必传，途径点依次按顺序传入，最多支持3个​
​
ExtensionOptions​
​
参数​
类型​
必须​
描述​
filter_emoji​
Boolean​
否​
为true时，过滤大模型输出的emoji表情​
enable_processing_state​
Boolean​
否​
为true时，输出智能体执行的关键过程，仅流式输出生效，详情见高级功能-输出关键执行过程​
disable_source_type_douyin_video​
Boolean​
否​
为true时，关闭控制台已经配置的抖音视频内容源​
disable_follow_up​
Boolean​
否​
为true时，关闭控制台已经开启的追问功能​
disable_citation​
Boolean​
否​
为true时，关闭控制台已经开启的引用角标功能​
disable_image_text_mix​
Boolean​
否​
为true时，关闭控制台已经开启的图文混排功能​
disable_baike_highlight​
Boolean​
否​
为true时，关闭控制台已经开启的百科划线词功能​
disable_text_to_image​
Boolean​
否​
为true时，关闭控制台已经开启的搜图功能​
enable_search_lite​
Boolean​
否​
为true时，开启控制台关闭的极速模式（耗时短，但效果会变差）​
browsing_mode​
Number​
​
否​
此参数用于控制联网行为，优先级高于控制台配置，影响文搜和图搜链路的处理逻辑​
参数值：​
1 - 自动联网：​
等价于控制台默认的“自动联网”设置​
2 - 强制联网：​
文搜链路至少使用一个搜索源进行联网搜索与总结​
图搜链路尽可能尝试联网，但不保证一定联网​
3 - 关闭联网：​
完全关闭联网能力，不使用任何联网资源进行搜索或总结​
card_position​
​
string​
​
否​
用于控制Cards字段返回位置。推荐元数据帧出卡，该方式会降低TTFT​
不传或first_frame-首帧出卡​
meta_frame-元数据帧出卡​
enable_followup_in_response​
Boolean​
否​
为true时，开启结尾强化追问功能​
​
响应体ChatCompletionResponse​
​
字段​
类型​
必须​
说明​
id​
String​
是​
响应的唯一标识符​
object​
​
String​
是​
响应对象的类型​
Chat​
chat.completion.chunk：流式聊天回复内容​
chat.completion：完整聊天回复内容​
choices​
Array[Choice]​
是​
返回项​
created​
Number​
是​
响应创建时间戳(秒)​
references​
Array[Reference]​
否​
大模型参考内容，流式只在首帧出​
search_results​
Array[Reference]​
否​
搜索到的结果，最多30个，流式只在首帧出​
follow_ups​
Array[FollowUp]​
否​
追问内容，控制台开通权限后可返回​
usage​
TokenUsage​
否​
token消耗量，流式只在尾帧出​
cards​
​
Array[Card]​
否​
​
富媒体卡片的结构化数据，卡片类型和详细字段见：智能体会话API-富媒体卡片数据​
通过请求体card_position参数可控制出卡位置，流式默认只在首帧出​
​
Choice​
​
字段​
类型​
必须​
说明​
delta​
​
Object​
否​
流式响应使用。包含增量更新内容​
role: 角色标识​
content: 文本片段​
message​
Object​
否​
非流式响应使用。包含完整的回复消息，和delta结构一致​
finish_reason​
​
String​
是​
生成终止的原因，可能的值：​
stop：API 返回完整的模型输出​
tool_calls：插件调用​
length：达到最大token限制​
content_filter：内容被过滤​
null：生成尚未完成​
index​
Number​
是​
当前选择的索引编号。在单个响应中通常为 0，在多选择配置下可能有多个索引​
​
Reference​
​
字段名​
类型​
必须​
说明​
id​
String​
是​
引用内容唯一ID​
source_type​
String​
是​
内容源​
site_name​
String​
否​
站点名，与SourceType存在映射，枚举场景优先使用SourceType​
title​
String​
否​
标题​
publish_time​
Number​
否​
发布时间，UnixSecond时间戳​
部分情况为0，例如部分搜索引擎结果​
url​
String​
否​
落地页，部分搜索引擎结果没有URL​
logo_url​
String​
否​
部分站点无logo​
cover_image​
Object​
否​
封面图​
​
{​
    "url": "https://xxx", // 封面图链接​
    "width": 123, // 封面图宽，不保证提供​
    "height": 123, // 封面图高，不保证提供​
}​
​
​
FollowUp​
​
字段​
类型​
必须​
说明​
item​
String​
是​
追问​
​
TokenUsage​
​
字段名​
类型​
必须​
说明​
prompt_tokens​
Number​
是​
本次请求中模型输入 token 数量（包含意图、改写、总结等环节）​
completion_tokens​
Number​
是​
本次请求中模型输出的 token 数量（包含意图、改写、总结等环节）​
total_tokens​
Number​
是​
本次请求消耗的总 token 数量（输入 + 输出）​
​
Card​
富媒体卡片的结构化数据，卡片类型和详细字段见：智能体会话API-富媒体卡片数据​
通过请求体card_position参数可控制出卡位置，流式默认只在首帧出​
请求示例​
​
{​
    "bot_id": "7429717161499017747",​
    "stream": false,​
    "messages": [​
        {​
            "role": "system",​
            "content": "你是智能语音助手,你的名字是韩梅梅，请用普通话回复用户。" //Systemprompt​
        },​
        {​
            "Role": "user",​
            "content": "周杰伦有什么歌" //上下文​
        },​
        {​
            "Role": "assistant",​
            "content": "周杰伦唱过《稻香》《叶惠美》《东风破》《菊花台》"​
        },​
        {​
            "Role": "user",​
            "content": "荣耀手机的最新动态" //当前问题​
        }​
    ],​
    "user_id": "hq53qh6683",​
    "knowledge":"当前正在驾驶问界M8增程MAX版，车内正在播放音乐《天黑黑》",​
    "location_info":{​
        "province": "陕西省",​
        "city": "西安市",​
        "district": "未央区",​
        "town": "玄武路",​
        "longitude": 108.962354,​
        "latitude": 34.303007​
    },​
    "navigation_info": {​
        "destination": {​
            "province": "",​
            "city": "北京市",​
            "district": "丰台区",​
            "town": "",​
            "longitude": 116.378517,​
            "latitude": 39.865246​
        },​
        "via": [​
            {​
                "province": "",​
                "city": "北京市",​
                "district": "海淀区",​
                "town": "",​
                "longitude": 116.313226,​
                "latitude": 39.970598​
            },​
            {​
                "province": "",​
                "city": "北京市",​
                "district": "海淀区",​
                "town": "",​
                "longitude": 116.337742,​
                "latitude": 39.992894​
            }​
        ]​
    }​
}​
​
响应示例​
非流式响应​
​
{​
    "id": "2025090814282017E9375ADE2F13A69656",​
    "object": "chat.completion",​
    "choices": [​
        {​
            "delta": null,​
            "message": {​
                "role": "assistant",​
                "content": "### 荣耀手机最新动态汇总  \n\n#### **一、即将发布的重磅新品**  \n- **荣耀Magic8系列**：  \n  预计**9月底发布，10月开售**，包含标准版、Pro版、Mini版及Ultra版。  \n  - **核心配置**：标准版与Pro版搭载**骁龙8至尊版第二代**芯片，Mini版或采用天玑9500芯片；全系配备潜望长焦镜头（Pro版或为2亿像素）、3D人脸识别+超声波指纹，以及近7000mAh超大电池，支持100W有线+80W无线快充。  \n  - **创新亮点**：*******仅做格式示例，后续篇幅省略*******",​
                "tool_calls": null​
            },​
            "finish_reason": "stop",​
            "index": 0​
        }​
    ],​
    "created": 1757312920,​
    "references": [​
        {​
            "id": "3d6c1693e1a00187-69168884de3550bd",​
            "source_type": "search_engine",​
            "site_name": "搜索引擎",​
            "title": "荣耀Magic7系列",​
            "summary": "",​
            "publish_time": 1757007498,​
            "url": "******",​
            "cover_image": null,​
            "logo_url": ""​
        },​
        {​
            "id": "********",​
            "source_type": "douyin_video",​
            "site_name": "抖音视频",​
            "title": "#荣耀Magic8 配置参数曝光，预计9月底发布，10月开售，这次发布会能不能喝上新任CEO#荣耀李健 的瑞幸就看大家了。\n标准版和pro版都是用的骁龙8至尊版第二代，顶满了！剩下大家悄眯眯去我视频里截图。#荣耀magic8pro #荣耀新品发布会 #荣耀Magic",​
            "summary": "",​
            "publish_time": 1756959049,​
            "url": "******",​
            "cover_image": {​
                "url": "******",​
                "width": 540,​
                "height": 960​
            },​
            "logo_url": ""​
        }​
    ],​
    "follow_ups": [​
        {​
            "item": "荣耀Magic8系列发布时间"​
        },​
        {​
            "item": "MagicOS10.0 Beta推送机型"​
        },​
        {​
            "item": "荣耀Magic V Flip2价格配置"​
        }​
    ],​
    "usage": {​
        "prompt_tokens": 6673,​
        "completion_tokens": 854,​
        "total_tokens": 7527​
    },​
    "cards": [​
        {​
            "card_type": "video",​
            "video_card": {​
                "id": "******",​
                "source_type": "douyin_video",​
                "site_name": "抖音视频",​
                "title": "#荣耀Magic8 配置参数曝光，预计9月底发布，10月开售，这次发布会能不能喝上新任CEO#荣耀李健 的瑞幸就看大家了。\n标准版和pro版都是用的骁龙8至尊版第二代，顶满了！剩下大家悄眯眯去我视频里截图。#荣耀magic8pro #荣耀新品发布会 #荣耀Magic",​
                "cover_image": {​
                    "url": "******",​
                    "width": 540,​
                    "height": 960​
                },​
                "url": "******",​
                "width": 0,​
                "height": 0,​
                "duration": 27981,​
                "author_name": "荣耀-阿黄（肖战版）"​
            }​
        }​
    ]​
}​
​
流式响应​
​
data:{"id":"202509081154548C7A7C13029EFAA557D1","object":"chat.completion.chunk","choices":[{"delta":{"role":"assistant","content":"###","tool_calls":null},"message":null,"finish_reason":"","index":0}],"created":1757303697,"references":[{"id":"68af2f737024280b-08c63c890a7eb2a0","source_type":"search_engine","site_name":"搜索引擎","title":"一张照片，一种对话。与HONOR Magic Moments荣耀手机影像计划全球评委 探寻心中的火花","summary":"","publish_time":1656259200,"url":"******","cover_image":null,"logo_url":""},{"id":"******","source_type":"douyin_video","site_name":"抖音视频","title":"#荣耀Magic8 配置参数曝光，预计9月底发布，10月开售，这次发布会能不能喝上新任CEO#荣耀李健 的瑞幸就看大家了。\n标准版和pro版都是用的骁龙8至尊版第二代，顶满了！剩下大家悄眯眯去我视频里截图。#荣耀magic8pro #荣耀新品发布会 #荣耀Magic","summary":"","publish_time":1756959049,"url":"******","cover_image":{"url":"******","width":540,"height":960},"logo_url":""}],"cards":[{"card_type":"video","video_card":{"id":"******","source_type":"douyin_video","site_name":"抖音视频","title":"#荣耀Magic8 配置参数曝光，预计9月底发布，10月开售，这次发布会能不能喝上新任CEO#荣耀李健 的瑞幸就看大家了。\n标准版和pro版都是用的骁龙8至尊版第二代，顶满了！剩下大家悄眯眯去我视频里截图。#荣耀magic8pro #荣耀新品发布会 #荣耀Magic","cover_image":{"url":"xxxxxx","width":540,"height":960},"url":"******","width":0,"height":0,"duration":27981,"author_name":"荣耀-阿黄（肖战版）"}}]}​
​
data:{"id":"202509081154548C7A7C13029EFAA557D1","object":"chat.completion.chunk","choices":[{"delta":{"role":"assistant","content":" ","tool_calls":null},"message":null,"finish_reason":"","index":0}],"created":1757303697,"references":null}​
​
data:{"id":"202509081154548C7A7C13029EFAA557D1","object":"chat.completion.chunk","choices":[{"delta":{"role":"assistant","content":"荣耀","tool_calls":null},"message":null,"finish_reason":"","index":0}],"created":1757303697,"references":null}​
​
...​
​
data:{"id":"202509081154548C7A7C13029EFAA557D1","object":"chat.completion.chunk","choices":[{"delta":{"role":"assistant","content":"评测","tool_calls":null},"message":null,"finish_reason":"","index":0}],"created":1757303711,"references":null}​
​
data:{"id":"202509081154548C7A7C13029EFAA557D1","object":"chat.completion.chunk","choices":[{"delta":{"role":"assistant","content":"。","tool_calls":null},"message":null,"finish_reason":"","index":0}],"created":1757303711,"references":null}​
​
data:{"id":"202509081154548C7A7C13029EFAA557D1","object":"chat.completion.chunk","choices":[{"delta":{"role":"assistant","content":"","tool_calls":null},"message":null,"finish_reason":"stop","index":0}],"created":1757303711,"references":null}​
​
data:{"id":"202509081154548C7A7C13029EFAA557D1","object":"chat.completion.chunk","choices":[{"delta":{"role":"assistant","content":"","tool_calls":null},"message":null,"finish_reason":"","index":0}],"created":1757303711,"references":null,"follow_ups":[{"item":"荣耀Magic8系列发布时间"},{"item":"MagicOS 10.0 Beta推送机型"},{"item":"荣耀IPO进程最新进展"}],"usage":{"prompt_tokens":6211,"completion_tokens":708,"total_tokens":6919}}​
​
data:[DONE]​
​
流式响应帧类型说明​
​
帧类型​
说明​
举例​
处理状态帧​
​
输出处理过程中调用的工具​
用于端上渲染，提升交互体验​
​
​
开启​
​
请求传入参数：​
"extension_options" : {​
    "enable_processing_state": true, // 默认false​
}​
​
结束​
​
在处理状态帧结束，内容帧首帧之前，输出一帧空帧，标记处理状态结束​
"finish_reason":"processing_finish"​
​
举例​
​
{​
    "id": "202503271640468507AA4C950F0039CEA0",​
    "object": "chat.completion.chunk",​
    "choices": [​
        {​
            "delta": {​
                "role": "assistant",​
                "content": "",​
                "tool_calls": null,​
                "processing_state": {​
                  "action": "planning",​
                  "description": "正在理解问题"​
                }​
            },​
            "message": null,​
            "finish_reason": "",​
            "index": 0​
        }​
    ],​
    "created": 1743064848,​
    "references": null​
}​
​
内容帧-首帧​
总结输出的首帧​
首帧返回的结构化数据​
Reference​
Cards（可调整到元数据帧）​
​
内容帧-中间帧​
大模型总结输出​
文本类型​
总结文本：content​
思考过程：reasoning_content​
​
​
{​
    "id": "202503271640468507AA4C950F0039CEA0",​
    "object": "chat.completion.chunk",​
    "choices": [​
        {​
            "delta": {​
                "role": "assistant",​
                "content": "是",​
                "tool_calls": null​
            },​
            "message": null,​
            "finish_reason": "",​
            "index": 0​
        }​
    ],​
    "created": 1743064848,​
    "references": null​
}​
​
内容帧-尾帧​
总结输出的最后一帧​
finish_reason=stop​
​
​
{​
    "id": "202503271640468507AA4C950F0039CEA0",​
    "object": "chat.completion.chunk",​
    "choices": [​
        {​
            "delta": {​
                "role": "assistant",​
                "content": "是",​
                "tool_calls": null​
            },​
            "message": null,​
            "finish_reason": "stop",​
            "index": 0​
        }​
    ],​
    "created": 1743064848,​
    "references": null​
}​
​
元数据帧​
​
总结输出完成后的补充帧​
元数据帧返回的结构化数据​
FollowUp​
TokenUsage​
​
​
{​
    // .....​
    "follow_ups": [​
        {​
            "item": "美的玲珑变频中央空调价格多少"​
        },​
        {​
            "item": "美的风尊空调静音效果如何"​
        },​
        {​
            "item": "科龙静省电空调噪音分贝是多少"​
        }​
    ],​
    "usage": {​
        "prompt_tokens": 9266,​
        "completion_tokens": 571,​
        "total_tokens": 9837​
    }​
}​
​
结束帧​
输出[DONE]​
无论成功失败都是最后一帧​
​
错误帧​
输出错误原因，只会出一次​
​
​
{​
    "error": {​
        "code": "invalid_parameter",​
        "message": "unsupported content type: <nil>",​
        "param": "messages",​
        "type": "validation_error"​
    }​
}​
​
​
​
高级功能​
引用角标​
说明：在总结输出中插入引用标记，指示文本来源于哪个参考资料​
格式：[ref_x]，其中 x 为参考资料的编号​
生效场景：流式输出、非流式输出​
开启方法：控制台开启开关​
注意事项：​
客户端可根据需要自定义处理引用角标的展示效果​
图文/视频混排​
说明：在输出内容中穿插图片，以Markdown格式呈现​
生效场景：仅支持流式输出​
开启方法：控制台开启开关​
输出格式：​
文本内容以常规方式输出​
图片以Markdown语法输出：![image](url)​
当仅开启视频混排时，图片url为视频封面图​
图片/视频信息会作为独立帧返回​
混排帧会包含图片的元数据在 delta.image_info 中，字段如下：​
​
字段名​
类型​
必须​
说明​
width​
Number​
否​
图片像素宽，可能为0​
height​
Number​
否​
图片像素高，可能为0​
image_url​
String​
是​
图片链接​
source_url​
String​
否​
图片源站链接​
​
如果需要渲染多图的客户，全量图片信息的元数据在delta.image_infos 中，字段类型为image_info的数组，详情见下方数据参考​
混排帧包含的视频元数据在delta.video_infos中，字段类型为video_info的数组，详情见下方参考​
video_info字段​
​
字段名​
类型​
必须​
说明​
id​
String​
是​
抖音视频id​
cover_image​
Object​
否​
封面图，样例：​
​
{​
  "url": "https://example.com/images/cover.jpg",​
  "width": 1920,​
  "height": 1080​
}​
​
width​
Number​
否​
视频像素宽，可能为0​
height​
Number​
否​
视频像素高，可能为0​
url​
String​
否​
播放链接，可能为空​
duration​
Number​
否​
视频时长，可能为0​
​
注意事项：​
支持Markdown渲染的客户端无需特殊处理​
返回数据参考：​
​
// 普通文本帧​
{​
    "id": "202503121053195DDBF4E949D2ECF224C4",​
    "object": "chat.completion.chunk",​
    "choices": [​
        {​
            "delta": {​
                "role": "assistant",​
                "content": "餐厅",​
                "tool_calls": null​
            },​
            "message": null,​
            "finish_reason": "",​
            "index": 0​
        }​
    ],​
    "created": 1741748005,​
    "references": null​
}​
// 图片插入帧​
{​
    "id": "202503121053195DDBF4E949D2ECF224C4",​
    "object": "chat.completion.chunk",​
    "choices": [​
        {​
            "delta": {​
                "role": "assistant",​
                "content": "\n![北京烤鸭](https://p3-search.byteimg.com/obj/tos-cn-i-qvj2lq49k0/1d9ee205d9554cc9bd4a473d2a33eeea)\n",​
                "tool_calls": null,​
                "image_info": {​
                    "width": 400,​
                    "height": 300,​
                    "image_url": "https://p3-search.byteimg.com/obj/tos-cn-i-qvj2lq49k0/1d9ee205d9554cc9bd4a473d2a33eeea",​
                    "source_url": "https://m.toutiao.com/11111111",​
                },​
                "image_infos": [​
                    {​
                        "width": 493,​
                        "height": 446,​
                        "image_url": "https://p26-volcsearch-sign.byteimg.com/tos-cn-i-xstd03g9pf/5ff9df98cb194889a96fa1df460318fc~tplv-obj.jpeg?lk3s=1515c32d&scene=volc_search&x-expires=1770641380&x-signature=VKK3bPyePnzOwfmSwIMk8%2Fpbdds%3D",​
                        "source_url": "https://m.toutiao.com/11111111"​
                    },​
                    {​
                        "width": 1280,​
                        "height": 960,​
                        "image_url": "https://p3-volcsearch-sign.byteimg.com/tos-cn-i-xv4ileqgde/e7070219833247138eea9ba12dd985e1~tplv-obj.jpeg?lk3s=1515c32d&scene=volc_search&x-expires=1770641366&x-signature=hVin4I75O0uHhe6sj15CTVE7SlQ%3D",​
                        "source_url": "https://m.toutiao.com/11111111"​
                    },​
                    {​
                        "width": 1280,​
                        "height": 960,​
                        "image_url": "https://p3-volcsearch-sign.byteimg.com/tos-cn-i-xv4ileqgde/e7070219833247138eea9ba12dd985e1~tplv-obj.jpeg?lk3s=1515c32d&scene=volc_search&x-expires=1770641369&x-signature=wvc4a0dsKIT%2F6tnjxBkM687Ps84%3D",​
                        "source_url": "https://m.toutiao.com/11111111"​
                    }​
                ]​
            },​
            "message": null,​
            "finish_reason": "",​
            "index": 0​
        }​
    ],​
    "created": 1741748006,​
    "references": null​
}​
​
百科划线词​
说明：在输出内容中，将自动识别百科词条并以下划线超链接形式在总结中呈现​
生效场景：仅支持联网问答pro文搜/图搜流式输出​
开启方法：控制台开启开关​
输出格式：​
下划线词条以Markdown语法输出： [百科词条名](百科url)​
注意事项：​
支持Markdown渲染的客户端无需特殊处理​
返回数据参考：​
​
// 普通文本帧​
{​
    "id": "202503121053195DDBF4E949D2ECF224C4",​
    "object": "chat.completion.chunk",​
    "choices": [​
        {​
            "delta": {​
                "role": "assistant",​
                "content": "餐厅",​
                "tool_calls": null​
            },​
            "message": null,​
            "finish_reason": "",​
            "index": 0​
        }​
    ],​
    "created": 1741748005,​
    "references": null​
}​
// 百科划线词帧​
{​
    "id": "202503121053195DDBF4E949D2ECF224C4",​
    "object": "chat.completion.chunk",​
    "choices": [​
        {​
            "delta": {​
                "role": "assistant",​
                "content": "[黑海](https://open.toutiao.com/article/url/?param=2v5e9zftZJNoZpWrngDvc2q5DSn3MhQSpNNyscfvpTU5JvxB3z74LP27mDnuEibEB1GbxWhav3dBqff8Uw57LXayNoAFWDaazMZJYYYnQR7rGQeo8BUjP96FwxGPhUhVgrqBrY1GB6K7XbzRK8TACMaUBybrBexh1ZzHcvZD3hteAx7n9x8PyBDhYdi2pTAdkhtVXBjbvN2hToDp331HDLfKp6QxCJEb2QgvkxgiT99VGusAiT&partner=agent_bot_7545058342901745178_default_content&version=3)",​
                "tool_calls": null​
            },​
            "message": null,​
            "finish_reason": "",​
            "index": 0​
        }​
    ],​
    "created": 1741748006,​
    "references": null​
}​
​
输出关键执行过程​
说明：执行过程中输出关键执行过程，提升端上交互效果​
开启方法：详情见请求体ChatCompletionRequest-ExtensionOptions-enable_processing_state​
过程范围和帧类型：​
​
action​
description(zh_CN)​
智能体实际动作​
planning​
正在理解问题​
智能体运行时初始化完成，开始理解用户问题​
search_begin​
正在搜索网页​
调用联网插件，常规联网总结时返回​
search_finish​
已阅读X个网页 (X>0)​
搜索完成 (空搜情况)​
调用联网插件，常规联网总结时返回​
​
返回数据参考：​
​
{​
    "id": "202503271640468507AA4C950F0039CEA0",​
    "object": "chat.completion.chunk",​
    "choices": [​
        {​
            "delta": {​
                "role": "assistant",​
                "content": "",​
                "tool_calls": null,                "processing_state": {                  "action": "planning",                  "description": "正在理解问题"                }​
            },​
            "message": null,​
            "finish_reason": "",​
            "index": 0​
        }​
    ],​
    "created": 1743064848,​
    "references": null​
}​
​
​
错误处理​
错误码​
网关错误：​
此接口基于火山引擎TOP网关发布，如果遇到网关层报错（例如验签错误），我们将返回火山引擎TOP网关错误，响应格式如下：​
​
{​
    "ResponseMetadata": {​
        "RequestId": "202210271151020102121450321B8D2A21",​
        "Action": "ScanSyncArticles",​
        "Version": "2023-01-01",​
        "Service": "volc_torchlight_api",​
        "Region": "cn-north-1",​
        "Error": {​
            "CodeN": 100010,​
            "Code": "SignatureDoesNotMatch",​
            "Message": "The request signature we calculated does not match the signature you provided. Check your Secret Access Key and signing method. Consult the service documentation for details."​
        }​
    }​
}​
​
业务错误：​
​
{​
    "error": {​
        "log_id": "错误logid",​
        "message": "错误的详细描述信息",​
        "type": "错误类型",​
        "code": "具体错误代码",​
        "param": "可选，导致错误的参数名称"​
    }​
}​
​
当流式输出过程中出现错误时，错误信息将在以 data: 开头的数据块中返回。字段解释如下：​
​
字段​
类型​
描述​
必须​
备注​
type​
String​
错误类型标识符​
是​
authentication_error：认证相关的错误​
validation_error：请求参数验证失败的错误​
permission_error：权限相关的错误​
model_error：AI 模型相关的错误​
bot_unavailable_error：智能体已停用、待正式开通或者试用次数已耗尽​
server_error：服务器内部错误​
code​
String​
具体错误代码​
是​
提供具体错误码，或者和type一致​
message​
String​
错误描述​
是​
提供具体错误描述，或者和type一致​
param​
String​
导致错误的参数名称​
否​
只有参数错误时会返回​
​
错误响应​
​
// 认证错误​
{​
  "error": {​
    "log_id": "错误logid",​
    "code": "invalid_api_key",​
    "message": "invalid api key",​
    "type": "authentication_error",​
    "param": null​
  }​
}​
// 请求参数错误​
{​
  "error": {​
    "log_id": "错误logid",​
    "code": "invalid_parameter",​
    "message": "stream requires bool type",​
    "type": "validation_error",​
    "param": "stream"​
  }​
}​
​
​
调用示例​
Python调用示例​
前提条件​
调用之前，您需要获取以下信息：​
bot_id: 控制台上创建的bot id，可参考联网问答Agent操作指南​
鉴权信息（任选一种即可，获取方式请参考本文档认证方式章节）：​
AccessKey、SecretKey​
APIKey​
Python环境​
Python：3.9版本及以上。​
Pip：25.1.1版本及以上。​
下载代码示例​
​
​
askecho_demo_python.zip
​
​
安装依赖​
解压代码包，进入代码包根目录后安装依赖。​
​
cd askecho_demo​
pip3 install -r requirements.txt​
​
运行代码​
APIKey接入​
bot_id替换为您的bot_id，api_key替换为您的APIKey​
​
python3 chat_completion_apikey.py --bot_id <bot_id> --api_key <api_key>​
​
火山引擎TOP网关接入​
bot_id替换为您的bot_id，access_key、secret_key替换为您的AccessKey和SecretKey​
​
python3 chat_completion_aksk.py --bot_id <bot_id> --access_key <access_key> --secret_key <secret_key>​
​
​
Java调用示例​
前提条件​
调用之前，您需要获取以下信息：​
bot_id: 控制台上创建的bot id，可参考联网问答Agent操作指南​
鉴权信息（任选一种即可，获取方式请参考本文档认证方式章节）：​
AccessKey、SecretKey​
APIKey​
Java环境​
Java：21版本及以上。​
Maven：3.9.10版本及以上。​
下载代码示例​
​
​
AskchoDemoJava.zip
​
​
解压代码​
解压代码包，进入代码包根目录。​
​
cd AskechoDemo​
​
运行代码​
APIKey接入​
botId替换为您的botId，apiKey替换为您的APIKey​
​
mvn compile exec:java -Dexec.mainClass=com.askecho.ChatCompletionApiKey -DbotId=<botId> -DapiKey=<apiKey>​
​
火山引擎TOP网关接入​
botId替换为您的botId，accessKey、secretKey替换为您的AccessKey和SecretKey​
​
mvn compile exec:java -Dexec.mainClass=com.askecho.ChatCompletionAKSK -DbotId=<botId> -DaccessKey=<accessKey> -DsecretKey=<secretKey>​
​
​
Postman调用示例​
使用APIKey直接通过Postman进行接口调用，实际参数替换为您的APIKey与botId。​
​
curl --location 'https://open.feedcoopapi.com/agent_api/agent/chat/completion' \​
--header 'Authorization: Bearer APIkey' \​
--header 'Content-Type: application/json' \​
--data '{​
    "bot_id": "botId",​
    "messages": [​
        {​
            "role": "user",​
            "content": "推荐一些好看的电影"​
        }​
    ],​
    "stream": true​
}'​
​
​
最近更新时间：2026.01.27 16:10:08
这个页面对您有帮助吗？
有用
无用
上一篇：
商品信息操作指南
智能体会话API-富媒体卡片数据
下一篇
认证方式
APIKey接入(推荐)
火山引擎TOP网关接入
接口详情
智能体会话
URL
请求体ChatCompletionRequest
Message
LocationInfo
NavigationInfo
ExtensionOptions
响应体ChatCompletionResponse
Choice
Reference
FollowUp
TokenUsage
Card
请求示例
响应示例
非流式响应
流式响应
流式响应帧类型说明
高级功能
引用角标
图文/视频混排
百科划线词
输出关键执行过程
错误处理
错误码
错误响应
调用示例
Python调用示例
前提条件
Python环境
下载代码示例
安装依赖
运行代码
APIKey接入
火山引擎TOP网关接入
Java调用示例
前提条件
Java环境
下载代码示例
解压代码
运行代码
APIKey接入
火山引擎TOP网关接入
Postman调用示例

鼠标选中内容，快速反馈问题
选中存在疑惑的内容，即可快速反馈问题，我们将会跟进处理
不再提示
好的，知道了

全天候售后服务
7x24小时专业工程师品质服务

极速服务应答
秒级应答为业务保驾护航

客户价值为先
从服务价值到创造客户价值

全方位安全保障
打造一朵“透明可信”的云
logo
关于我们
为什么选火山
文档中心
联系我们
人才招聘
云信任中心
友情链接
产品
云服务器
GPU云服务器
机器学习平台
客户数据平台 VeCDP
飞连
视频直播
全部产品
解决方案
汽车行业
金融行业
文娱行业
医疗健康行业
传媒行业
智慧文旅
大消费
服务与支持
备案服务
服务咨询
建议与反馈
廉洁舞弊举报
举报平台
联系我们
业务咨询：service@volcengine.com
市场合作：marketing@volcengine.com
电话：400-850-0030
地址：北京市海淀区北三环西路甲18号院大钟寺广场1号楼

微信公众号

抖音号

视频号
© 北京火山引擎科技有限公司 2025 版权所有
代理域名注册服务机构：新网数码 商中在线
服务条款
隐私政策
更多协议

京公网安备11010802032137号
京ICP备20018813号-3
营业执照
增值电信业务经营许可证京B2-20202418，A2.B1.B2-20202637
网络文化经营许可证：京网文（2023）4872-140号
