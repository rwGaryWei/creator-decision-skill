# 64 项任务实施进度 / Implementation ledger

更新：2026-09-25 · 0.1.0-alpha + 未发布修订。48项主线＋16项可选全部保留。

`done`：该具体交付完成；`partial`：已有产物但未达到完整验收；`blocked`：缺少实际研究、独立人员等条件；`owner_review`：需要所有者作出实际判断。文件、程序检查和模型输出不等于独立人工评价。

Counts: done=28, partial=27, blocked=8, owner_review=1

36次探索性模型试跑已执行。人工工时与独立评分未知，不以0代填。试跑之后的指令修订尚未重新进行模型比较。当前先完善产品、开展作者内部评审，正式研究后置；详见[路线与审查记录](owner-review.md)。

## TSK-001 · 确认产品目标与范围

- Track: core · Status: **done**
- 完成条件：用户确认首版四领域和三入口；不可牺牲目标与未知分开。
- 证据：[docs/scope.md](../docs/scope.md), [docs/owner-review.md](../docs/owner-review.md)
- 状态说明／剩余：四领域与三入口沿用已选范围；所有者确认先宏观分析后具体方案，并以相近作品调查、多因素优劣分析和问题支持作者自主决定。未知证据与作者选择保持分开；本项完成产品原则审查，不代表模型行为已验证。

## TSK-002 · 整理相关项目与研究定位

- Track: core · Status: **done**
- 完成条件：每项有来源和日期；不把相关项目声明当实测效果。
- 证据：[docs/related-work.md](../docs/related-work.md)
- 状态说明／剩余：该具体交付项已具备；不代表整体产品行为或实证有效性已经验证。

## TSK-003 · 制作四领域完整示范

- Track: core · Status: **done**
- 完成条件：能看见判断、改法、验证；包含证据充分时继续的分支。
- 证据：[examples/README.md](../examples/README.md)
- 状态说明／剩余：该具体交付项已具备；不代表整体产品行为或实证有效性已经验证。

## TSK-004 · 冻结首轮需求与案例规则

- Track: core · Status: **partial**
- 完成条件：P0/P1清晰；用户可纠正；估算按实际第一周投入校准。
- 证据：[docs/requirements.json](../docs/requirements.json)
- 状态说明／剩余：需求基线已保存；用户审查、实际投入校准和冻结记录尚未完成。

## TSK-005 · 编写通用Skill主流程

- Track: core · Status: **partial**
- 完成条件：从一句话得到范围明确短卡；不默认商业目标。
- 证据：[skills/creator-decision/SKILL.md](../skills/creator-decision/SKILL.md)
- 状态说明／剩余：流程已实现；尚需实际模型行为评估，不能以指令存在代替有效性。

## TSK-006 · 定义最小数据对象和格式

- Track: core · Status: **done**
- 完成条件：建议→陈述→来源、决定→版本关系完整；未知不填0。
- 证据：[skills/creator-decision/references/data-format.md](../skills/creator-decision/references/data-format.md), [tests/test_decision.py](../tests/test_decision.py)
- 状态说明／剩余：该具体交付项已具备；不代表整体产品行为或实证有效性已经验证。

## TSK-007 · 制作报告与实验模板

- Track: core · Status: **done**
- 完成条件：短卡可独立使用；计划与实际结果分开。
- 证据：[skills/creator-decision/assets/decision-card.md](../skills/creator-decision/assets/decision-card.md), [skills/creator-decision/assets/experiment.md](../skills/creator-decision/assets/experiment.md), [skills/creator-decision/assets/reassessment.md](../skills/creator-decision/assets/reassessment.md)
- 状态说明／剩余：该具体交付项已具备；不代表整体产品行为或实证有效性已经验证。

## TSK-008 · 连通本地最小流程

- Track: core · Status: **partial**
- 完成条件：无外网与Steam依赖也能完成；人工状态不得伪造。
- 证据：[skills/creator-decision/references/tools.md](../skills/creator-decision/references/tools.md), [tests/test_decision.py](../tests/test_decision.py)
- 状态说明／剩余：本地工具流程通过测试；尚无真实用户修正记录或宿主完整对话试用。

## TSK-009 · 实现网页工具领域

- Track: core · Status: **done**
- 完成条件：任务完成、替代、纠错和维护均有实际判断。
- 证据：[skills/creator-decision/references/domains/web.md](../skills/creator-decision/references/domains/web.md), [docs/pilot-findings.md](../docs/pilot-findings.md), [evaluations/results/pilot-2026-09-25/README.md](../evaluations/results/pilot-2026-09-25/README.md)
- 状态说明／剩余：网页指南、示范及3个独立试跑场景已产生具体任务/恢复建议；作者AI审查，不宣称人类有效性。

## TSK-010 · 实现视频领域

- Track: core · Status: **done**
- 完成条件：观看承诺与回报可定位；脚本与成片观察区分。
- 证据：[skills/creator-decision/references/domains/video.md](../skills/creator-decision/references/domains/video.md), [docs/pilot-findings.md](../docs/pilot-findings.md), [evaluations/results/pilot-2026-09-25/README.md](../evaluations/results/pilot-2026-09-25/README.md)
- 状态说明／剩余：视频指南、示范及3个试跑场景区分了脚本/画面描述与实际音视频观察；未宣称真实媒体能力。

## TSK-011 · 实现作品访问范围记录

- Track: core · Status: **done**
- 完成条件：失败/部分材料仍有可用意见；未观察能力不冒充。
- 证据：[skills/creator-decision/references/capabilities.md](../skills/creator-decision/references/capabilities.md), [tests/test_decision.py](../tests/test_decision.py)
- 状态说明／剩余：该具体交付项已具备；不代表整体产品行为或实证有效性已经验证。

## TSK-012 · 审查两领域流程与反例

- Track: core · Status: **partial**
- 完成条件：修复套话、重复追问及错误观察；记录未解决项。
- 证据：[examples/web_tool/prototype.md](../examples/web_tool/prototype.md), [examples/video/prototype.md](../examples/video/prototype.md)
- 状态说明／剩余：示范和检查材料就绪；尚缺实际宿主运行与反馈修正。

## TSK-013 · 实现短剧领域

- Track: core · Status: **done**
- 完成条件：能解释具体因果和修改影响，不统一改成反转模板。
- 证据：[skills/creator-decision/references/domains/drama.md](../skills/creator-decision/references/domains/drama.md), [docs/pilot-findings.md](../docs/pilot-findings.md), [evaluations/results/pilot-2026-09-25/README.md](../evaluations/results/pilot-2026-09-25/README.md)
- 状态说明／剩余：短剧指南与3个试跑场景给出动机、因果及具体场景修改；保留不同创作取舍。

## TSK-014 · 实现游戏领域

- Track: core · Status: **done**
- 完成条件：核心判断无AppID依赖；录像不冒充试玩。
- 证据：[skills/creator-decision/references/domains/game.md](../skills/creator-decision/references/domains/game.md), [docs/pilot-findings.md](../docs/pilot-findings.md), [evaluations/results/pilot-2026-09-25/README.md](../evaluations/results/pilot-2026-09-25/README.md)
- 状态说明／剩余：游戏指南与3个试跑场景处理选择、反馈和范围，无Steam依赖；未冒充实际试玩。

## TSK-015 · 整理12个开发案例

- Track: core · Status: **done**
- 完成条件：材料来源、目标、期望行为和合成标记完整。
- 证据：[evaluations/cases/development.json](../evaluations/cases/development.json)
- 状态说明／剩余：该具体交付项已具备；不代表整体产品行为或实证有效性已经验证。

## TSK-016 · 审查四领域alpha

- Track: core · Status: **done**
- 完成条件：四领域有实质差异；修复默认劝退；保留失败案例。
- 证据：[docs/validation.md](../docs/validation.md), [docs/pilot-findings.md](../docs/pilot-findings.md), [evaluations/results/pilot-2026-09-25/README.md](../evaluations/results/pilot-2026-09-25/README.md)
- 状态说明／剩余：四领域alpha已形成，36次试跑原文保存，并记录基线同样有用及回答偏长的问题。

## TSK-017 · 实现来源和陈述校验

- Track: core · Status: **done**
- 完成条件：能拒绝断裂引用；不把字符串命中当支持结论。
- 证据：[skills/creator-decision/scripts/decision.py](../skills/creator-decision/scripts/decision.py), [tests/test_decision.py](../tests/test_decision.py)
- 状态说明／剩余：该具体交付项已具备；不代表整体产品行为或实证有效性已经验证。

## TSK-018 · 实现调查模式与失败降级

- Track: core · Status: **partial**
- 完成条件：超时/限额/部分结果有状态；不无限重试或假装搜索。
- 证据：[skills/creator-decision/references/capabilities.md](../skills/creator-decision/references/capabilities.md)
- 状态说明／剩余：降级规则与资料状态已实现；宿主联网失败/限额行为尚需实际验证。

## TSK-019 · 实现AI制作与证据取舍

- Track: core · Status: **done**
- 完成条件：分析效率与校正负担；模拟和AI标签不污染事实。
- 证据：[skills/creator-decision/references/evidence.md](../skills/creator-decision/references/evidence.md), [docs/pilot-findings.md](../docs/pilot-findings.md), [evaluations/results/pilot-2026-09-25/README.md](../evaluations/results/pilot-2026-09-25/README.md)
- 状态说明／剩余：实际试跑记录出现生成/校核成本、具体制作角色以及AI标签不能代替质量证据的判断；不宣称普遍可靠。

## TSK-020 · 核验引用和发布资料来源

- Track: core · Status: **partial**
- 完成条件：每条核心外部断言人工核对；材料用途可追溯。
- 证据：[docs/related-work.md](../docs/related-work.md), [docs/licensing.md](../docs/licensing.md)
- 状态说明／剩余：相关项目来源已阅读；外部论断的独立人工语义审查未完成。

## TSK-021 · 实现人工决定与版本绑定

- Track: core · Status: **done**
- 完成条件：新报告不沿用旧批准；中断不损坏原件。
- 证据：[skills/creator-decision/scripts/decision.py](../skills/creator-decision/scripts/decision.py), [tests/test_decision.py](../tests/test_decision.py)
- 状态说明／剩余：该具体交付项已具备；不代表整体产品行为或实证有效性已经验证。

## TSK-022 · 实现新证据复盘

- Track: core · Status: **partial**
- 完成条件：能响应证据与目标改变；不因自信语气无理由翻转。
- 证据：[skills/creator-decision/assets/reassessment.md](../skills/creator-decision/assets/reassessment.md)
- 状态说明／剩余：版本差异和复盘模板已实现；证据/态度成对模型行为未测。

## TSK-023 · 加固外部材料与导出边界

- Track: core · Status: **partial**
- 完成条件：恶意资料不成为指令；无越权外发和路径写入。
- 证据：[SECURITY.md](../SECURITY.md), [tests/test_decision.py](../tests/test_decision.py)
- 状态说明／剩余：工具路径与报告边界有测试；提示注入和越权模型行为未测。

## TSK-024 · 执行可靠性检查点

- Track: core · Status: **partial**
- 完成条件：必测确定性通过；S0/S1未解决项阻止候选公开。
- 证据：[docs/validation.md](../docs/validation.md)
- 状态说明／剩余：工程测试通过；完整行为回归与严重缺陷审查仍待运行。

## TSK-025 · 验证首个宿主安装

- Track: core · Status: **partial**
- 完成条件：实际安装可复现；准确写宿主/系统/版本支持范围。
- 证据：[scripts/install.py](../scripts/install.py), [tests/test_install.py](../tests/test_install.py)
- 状态说明／剩余：临时项目安装并执行工具通过；宿主自动识别及跨平台运行待核实。

## TSK-026 · 编写中英文完整文档

- Track: core · Status: **done**
- 完成条件：非技术使用者可理解；两语言关键承诺一致。
- 证据：[README.md](../README.md), [README.zh-CN.md](../README.zh-CN.md), [docs/quickstart.md](../docs/quickstart.md)
- 状态说明／剩余：该具体交付项已具备；不代表整体产品行为或实证有效性已经验证。

## TSK-027 · 制作可分发包与自动检查

- Track: core · Status: **done**
- 完成条件：无私有记录/开发依赖；旧模块范围单独注明。
- 证据：[scripts/package.py](../scripts/package.py), [scripts/check_release.py](../scripts/check_release.py), [.github/workflows/check.yml](../.github/workflows/check.yml)
- 状态说明／剩余：该具体交付项已具备；不代表整体产品行为或实证有效性已经验证。

## TSK-028 · 执行安装与使用预检

- Track: core · Status: **partial**
- 完成条件：新上下文四领域可走完；未测媒体能力明确。
- 证据：[docs/quickstart.md](../docs/quickstart.md), [docs/validation.md](../docs/validation.md)
- 状态说明／剩余：本地安装流程可用；真实首次使用者预检未完成。

## TSK-029 · 准备试用与研究合规材料

- Track: core · Status: **partial**
- 完成条件：如作为学术研究先核实流程；无授权不联系参与者。
- 证据：[docs/trial-kit.md](../docs/trial-kit.md)
- 状态说明／剩余：试用材料已准备；如作为学术研究，须先核实适用机构流程。尚无参与者授权。

## TSK-030 · 执行可得的外部或内部试用

- Track: core · Status: **partial**
- 完成条件：外部缺失则标内部alpha，不把作者模拟算外部样本。
- 证据：[docs/trial-kit.md](../docs/trial-kit.md), [docs/validation.md](../docs/validation.md)
- 状态说明／剩余：尚无真实试用；作者编写示例不计为外部或完整内部试用。

## TSK-031 · 修复首次使用障碍

- Track: core · Status: **partial**
- 完成条件：问题可复现，修复不损害四领域和真实性。
- 证据：[CHANGELOG.md](../CHANGELOG.md)
- 状态说明／剩余：已修正工程和说明问题；首次用户试用尚未产生可复现障碍。

## TSK-032 · 构建新的试跑案例与评分锚点

- Track: core · Status: **done**
- 完成条件：与开发集项目隔离；评分不奖励仅复制模板。
- 证据：[evaluations/cases/pilot.json](../evaluations/cases/pilot.json), [evaluations/rubric.md](../evaluations/rubric.md)
- 状态说明／剩余：该具体交付项已具备；不代表整体产品行为或实证有效性已经验证。

## TSK-033 · 冻结三种对照提示与条件

- Track: core · Status: **done**
- 完成条件：通用基线认真设计；条件差异记录，不人为弱化基线。
- 证据：[evaluations/harness.py](../evaluations/harness.py), [evaluations/run-record.example.json](../evaluations/run-record.example.json)
- 状态说明／剩余：该具体交付项已具备；不代表整体产品行为或实证有效性已经验证。

## TSK-034 · 完成36次小规模试跑

- Track: core · Status: **done**
- 完成条件：12项目×3方法；所有运行有记录，未完成标缺失。
- 证据：[evaluations/PROTOCOL.md](../evaluations/PROTOCOL.md), [docs/pilot-findings.md](../docs/pilot-findings.md), [evaluations/results/pilot-2026-09-25/README.md](../evaluations/results/pilot-2026-09-25/README.md)
- 状态说明／剩余：12项目×3方法的36次独立上下文试跑完成；宿主未公开精确模型部署/采样/用量，限制已记录。

## TSK-035 · 校准评分与错误分类

- Track: core · Status: **partial**
- 完成条件：作者/模型/独立评分区分；另用开发案例校准态度/证据对，分别测量评分时间。
- 证据：[evaluations/rubric.md](../evaluations/rubric.md), [docs/pilot-findings.md](../docs/pilot-findings.md), [evaluations/results/pilot-2026-09-25/README.md](../evaluations/results/pilot-2026-09-25/README.md)
- 状态说明／剩余：已有36次原始输出和评分表；独立校准、成对行为校准与实际评审工时仍未完成。

## TSK-036 · 决定扩展研究与产品修订

- Track: core · Status: **done**
- 完成条件：根据资源和问题决定，正式结果前固定规模，允许无优势。
- 证据：[docs/maintenance.md](../docs/maintenance.md), [docs/owner-review.md](../docs/owner-review.md)
- 状态说明／剩余：所有者已选择先完善产品、开展作者内部评审并后置正式研究；本项仅完成路线决定。正式规模未冻结，TSK-035校准仍未完成；后续启动研究须另行满足准备条件。

## TSK-037 · 修复试跑暴露的关键问题

- Track: core · Status: **partial**
- 完成条件：保留修复理由，不能用测试集偷偷调方法。
- 证据：[docs/failure-analysis.md](../docs/failure-analysis.md), [docs/pilot-findings.md](../docs/pilot-findings.md), [evaluations/results/pilot-2026-09-25/README.md](../evaluations/results/pilot-2026-09-25/README.md)
- 状态说明／剩余：根据试跑补强简短卡片及外部记录状态说明；未重跑模型比较，不能宣称修复效果已验证。

## TSK-038 · 执行完整发布候选回归

- Track: core · Status: **blocked**
- 完成条件：无未解决S0/S1；四领域达内部行动质量门槛。
- 证据：[docs/behavioral-checks.json](../docs/behavioral-checks.json), [docs/validation.md](../docs/validation.md), [docs/owner-review.md](../docs/owner-review.md)
- 状态说明／剩余：工程检查可重跑；模型行为回归和人工有用性门槛未完成。

## TSK-039 · 冻结正式研究协议草案

- Track: core · Status: **done**
- 完成条件：主要/探索性区分；独立人力不足明确，测试集尚未用于调优。
- 证据：[evaluations/PROTOCOL.md](../evaluations/PROTOCOL.md)
- 状态说明／剩余：该具体交付项已具备；不代表整体产品行为或实证有效性已经验证。

## TSK-040 · 冻结候选版本与范围

- Track: core · Status: **partial**
- 完成条件：研究与产品声明仅对应实际证据；后改另记版本。
- 证据：[CHANGELOG.md](../CHANGELOG.md), [docs/scope.md](../docs/scope.md)
- 状态说明／剩余：仅alpha范围已明确；研究候选版不能在未验证时冻结为完成。

## TSK-041 · 完成公开文档和四演示

- Track: core · Status: **done**
- 完成条件：每领域独立可读；示例真实性和限制清楚。
- 证据：[README.md](../README.md), [README.zh-CN.md](../README.zh-CN.md), [examples/README.md](../examples/README.md)
- 状态说明／剩余：该具体交付项已具备；不代表整体产品行为或实证有效性已经验证。

## TSK-042 · 完善开源协作与维护入口

- Track: core · Status: **done**
- 完成条件：无需上传私有对话；贡献围绕真实用户任务。
- 证据：[CONTRIBUTING.md](../CONTRIBUTING.md), [SECURITY.md](../SECURITY.md), [.github/ISSUE_TEMPLATE/bug.md](../.github/ISSUE_TEMPLATE/bug.md)
- 状态说明／剩余：MIT许可、贡献指南、问题模板与维护规则已具备；没有上传私密对话或冒充用户量。

## TSK-043 · 审查许可、隐私和公开材料

- Track: core · Status: **done**
- 完成条件：未获许可材料替换；身份/名称/公开范围待用户明确。
- 证据：[docs/licensing.md](../docs/licensing.md), [LICENSE](../LICENSE)
- 状态说明／剩余：所有者明确选择MIT并授权公开项目；已检查发布文件，未包含私密聊天、凭据或第三方评论数据。

## TSK-044 · 准备发布说明和求职演示

- Track: core · Status: **partial**
- 完成条件：真实描述个人与AI贡献；不保证stars、就业、市场成功。
- 证据：[docs/portfolio.md](../docs/portfolio.md)
- 状态说明／剩余：演示与发布文案已准备；所有者仍需核实个人贡献、理解与公开表述。

## TSK-045 · 执行发布检查与授权内交付

- Track: core · Status: **done**
- 完成条件：无授权保留待发布包；外部门槛缺失只能准确标beta。
- 证据：[CHANGELOG.md](../CHANGELOG.md)
- 状态说明／剩余：完整项目已推送至指定公开仓库；以alpha标记，未冒充通过独立用户门槛的v1。

## TSK-046 · 撰写初步技术报告

- Track: core · Status: **done**
- 完成条件：未执行正式研究明确；不以36次试跑冒充普遍有效性。
- 证据：[docs/research-report.md](../docs/research-report.md)
- 状态说明／剩余：该具体交付项已具备；不代表整体产品行为或实证有效性已经验证。

## TSK-047 · 制作作品集和面试材料

- Track: core · Status: **partial**
- 完成条件：能解释关键设计和一次失败；简历数字都有依据。
- 证据：[docs/portfolio.md](../docs/portfolio.md)
- 状态说明／剩余：作品集材料已准备；无法替用户证明对实现的理解或完成面试演练。

## TSK-048 · 建立维护与下一阶段决定

- Track: core · Status: **partial**
- 完成条件：无暗中遥测/自动外发；扩展条件与止损点明确。
- 证据：[docs/maintenance.md](../docs/maintenance.md)
- 状态说明／剩余：维护规则已写明；真实反馈与下一阶段选择尚未发生。

## TSK-049 · 落实独立评审与适用手续

- Track: optional_extension · Status: **blocked**
- 完成条件：依赖未落实时转文档/内部替代，不假装已独立评估。
- 证据：[docs/trial-kit.md](../docs/trial-kit.md), [evaluations/PROTOCOL.md](../evaluations/PROTOCOL.md), [docs/owner-review.md](../docs/owner-review.md)
- 状态说明／剩余：按所有者决定后置正式研究；独立评审者尚未确认；模型/作者不能冒充独立人类。

## TSK-050 · 构建并冻结24项目测试集

- Track: optional_extension · Status: **partial**
- 完成条件：与开发/试跑项目隔离；材料用途与随机顺序可复现。
- 证据：[evaluations/cases/test-candidates.json](../evaluations/cases/test-candidates.json)
- 状态说明／剩余：24个候选项目已补全；还需审查、泄漏检查和正式版本冻结。

## TSK-051 · 试评校准与锁定分析规则

- Track: optional_extension · Status: **blocked**
- 完成条件：校准只用非测试资料；重叠比例和比较对固定；单输出/态度对/证据对工时单列。
- 证据：[evaluations/rubric.md](../evaluations/rubric.md), [docs/owner-review.md](../docs/owner-review.md)
- 状态说明／剩余：按所有者决定后置正式研究；需要非测试集实际输出与评分者，完成校准和实际工时记录。

## TSK-052 · 正式运行前准备检查

- Track: optional_extension · Status: **blocked**
- 完成条件：研究设计在结果前冻结；失败和重试策略明确。
- 证据：[evaluations/PROTOCOL.md](../evaluations/PROTOCOL.md), [docs/owner-review.md](../docs/owner-review.md)
- 状态说明／剩余：按所有者决定后置正式研究；正式设计、模型预算、评审者及候选版尚未冻结。

## TSK-053 · 运行第一批冻结测试

- Track: optional_extension · Status: **blocked**
- 完成条件：同模型和材料预算，独立上下文，不按表现淘汰结果。
- 证据：[evaluations/harness.py](../evaluations/harness.py), [docs/owner-review.md](../docs/owner-review.md)
- 状态说明／剩余：按所有者决定后置正式研究；正式运行尚未开始；需要已冻结协议与可用模型环境。

## TSK-054 · 运行剩余冻结测试

- Track: optional_extension · Status: **blocked**
- 完成条件：运行数核对；若预算不足按事先规则停止并报告。
- 证据：[evaluations/harness.py](../evaluations/harness.py), [docs/owner-review.md](../docs/owner-review.md)
- 状态说明／剩余：按所有者决定后置正式研究；正式运行尚未开始；不能以生成任务清单算完成。

## TSK-055 · 准备盲评数据包

- Track: optional_extension · Status: **partial**
- 完成条件：方法映射受控；比较对保留所需输入差异；不修改正文；文风盲法限制说明。
- 证据：[evaluations/harness.py](../evaluations/harness.py), [tests/test_evaluation.py](../tests/test_evaluation.py), [docs/pilot-findings.md](../docs/pilot-findings.md), [evaluations/results/pilot-2026-09-25/README.md](../evaluations/results/pilot-2026-09-25/README.md)
- 状态说明／剩余：实际36次试跑已生成方法名隐藏的未评分材料，映射留在本地；正式研究包未产生，公开原文使盲化有限。

## TSK-056 · 核验运行数据完整性

- Track: optional_extension · Status: **partial**
- 完成条件：每条可追溯；不把432相关观测算432独立项目。
- 证据：[scripts/check_release.py](../scripts/check_release.py), [evaluations/PROTOCOL.md](../evaluations/PROTOCOL.md), [docs/pilot-findings.md](../docs/pilot-findings.md), [evaluations/results/pilot-2026-09-25/README.md](../evaluations/results/pilot-2026-09-25/README.md)
- 状态说明／剩余：36次试跑的输入/输出哈希、分组和数量已核对；正式180/432次研究未运行。

## TSK-057 · 组织评分与记录分歧

- Track: optional_extension · Status: **blocked**
- 完成条件：外部时间单列；共识结果不冒充原始一致性。
- 证据：[evaluations/rubric.md](../evaluations/rubric.md), [docs/owner-review.md](../docs/owner-review.md)
- 状态说明／剩余：按所有者决定后置正式研究；缺少实际输出及独立评审人员；不能生成虚构评分。

## TSK-058 · 执行按项目配对分析

- Track: optional_extension · Status: **partial**
- 完成条件：主要/探索指标分开；小样本和随机性限制明确。
- 证据：[evaluations/harness.py](../evaluations/harness.py), [tests/test_evaluation.py](../tests/test_evaluation.py)
- 状态说明／剩余：配对计算工具通过已知算例；没有真实评分可分析。

## TSK-059 · 分析失败与领域差异

- Track: optional_extension · Status: **partial**
- 完成条件：不精选成功；合理更新与态度不稳定分开。
- 证据：[docs/failure-analysis.md](../docs/failure-analysis.md), [docs/pilot-findings.md](../docs/pilot-findings.md), [evaluations/results/pilot-2026-09-25/README.md](../evaluations/results/pilot-2026-09-25/README.md)
- 状态说明／剩余：已逐条阅读36次回答并写非盲实施AI质性复盘；未产生独立评分或正式研究错误率。

## TSK-060 · 独立复核研究结论

- Track: optional_extension · Status: **blocked**
- 完成条件：每个对外效果声明有对应分析；不足则降低声明。
- 证据：[docs/research-report.md](../docs/research-report.md), [docs/pilot-findings.md](../docs/pilot-findings.md), [evaluations/results/pilot-2026-09-25/README.md](../evaluations/results/pilot-2026-09-25/README.md), [docs/owner-review.md](../docs/owner-review.md)
- 状态说明／剩余：按所有者决定后置正式研究；探索性报告有36次输出；独立人类审查和正式效应结论仍缺少必要评分。

## TSK-061 · 形成完整技术报告

- Track: optional_extension · Status: **partial**
- 完成条件：清楚记录实际完成/未完成，论文形式待贡献确定。
- 证据：[docs/research-report.md](../docs/research-report.md), [docs/pilot-findings.md](../docs/pilot-findings.md), [evaluations/results/pilot-2026-09-25/README.md](../evaluations/results/pilot-2026-09-25/README.md)
- 状态说明／剩余：已更新为36次探索性试跑报告，完整披露限制；正式研究与独立评价尚未完成。

## TSK-062 · 整理导师沟通与投稿准备

- Track: optional_extension · Status: **done**
- 完成条件：只准备材料；不未经授权联系，不承诺录用。
- 证据：[docs/research-brief.md](../docs/research-brief.md)
- 状态说明／剩余：该具体交付项已具备；不代表整体产品行为或实证有效性已经验证。

## TSK-063 · 更新英文作品集并模拟演示

- Track: optional_extension · Status: **partial**
- 完成条件：用户能解释本人贡献和限制，不夸大AI生成实现。
- 证据：[docs/portfolio.md](../docs/portfolio.md)
- 状态说明／剩余：英文材料与演示步骤已准备；需所有者实际讲解并确认贡献。

## TSK-064 · 确定下一版或有限维护

- Track: optional_extension · Status: **owner_review**
- 完成条件：基于使用价值和投入，用户决定是否改变四领域承诺。
- 证据：[docs/maintenance.md](../docs/maintenance.md), [docs/owner-review.md](../docs/owner-review.md)
- 状态说明／剩余：下一阶段选项已准备；最终产品定位与维护投入由所有者决定。
