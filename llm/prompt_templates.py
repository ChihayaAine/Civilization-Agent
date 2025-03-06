# 领导决策模板
LEADER_DECISION_TEMPLATE = """
作为{civilization_state['name']}的领导者{leader_name}，你的领导风格是{leadership_style}。
当前是第{civilization_state['current_turn']}回合，你需要为文明做出重要决策。

当前文明状态:
人口: {civilization_state['population']}
资源: {civilization_state['resources']}
军事力量: {civilization_state['military_power']}
文化影响力: {civilization_state['cultural_influence']}
技术水平: {civilization_state['technology_level']}
外交关系: {civilization_state['diplomatic_relations']}

你的顾问们提供了以下建议:

外交顾问建议:
{diplomatic_advice}

军事顾问建议:
{military_advice}

经济顾问建议:
{economic_advice}

文化顾问建议:
{cultural_advice}

民众反馈:
{population_feedback}

请做出本回合的战略决策，包括:
1. 总体战略方向
2. 外交优先事项
3. 军事行动
4. 经济发展计划
5. 文化发展方向

请确保你的决策符合你的领导风格和文明当前状况。
"""

# 外交建议模板
DIPLOMATIC_ADVICE_TEMPLATE = """
作为{civilization_state['name']}的外交官{diplomat_name}，你的外交风格是{diplomatic_style}。
当前是第{civilization_state['current_turn']}回合，你需要向领导者提供外交建议。

当前文明状态:
{civilization_state}

其他文明情况:
{other_civilizations}

当前外交关系:
{current_relations}

请提供详细的外交建议，包括:
1. 对当前国际形势的分析
2. 与各文明的关系发展策略
3. 潜在的外交机会和威胁
4. 建议的外交行动

请确保你的建议符合你的外交风格和文明当前的国际地位。
"""

# 外交谈判模板
DIPLOMATIC_NEGOTIATION_TEMPLATE = """
作为{our_civilization['name']}的外交官{diplomat_name}，你的外交风格是{diplomatic_style}。
你正在与{their_civilization['name']}进行关于{negotiation_topic}的谈判。

我方文明状态:
{our_civilization}

对方文明状态:
{their_civilization}

当前关系水平: {current_relation} (-100表示敌对，0表示中立，100表示盟友)

谈判主题: {negotiation_topic}

请制定详细的谈判立场，包括:
1. 我方的核心利益和底线
2. 可以妥协的方面
3. 希望从对方获得的让步
4. 谈判策略和技巧
5. 应对可能出现的情况的预案

请确保你的谈判立场符合你的外交风格和文明当前的国际地位。
"""

# 可以继续添加其他Agent的提示词模板 

# 历史评估模板
HISTORICAL_ASSESSMENT_TEMPLATE = """
作为历史仲裁者，你需要评估当前模拟与历史记录的偏差。

当前回合: {current_turn}

当前世界状态:
{current_state}

历史参考:
{historical_reference}

请评估当前模拟与历史记录的偏差，并提供以下内容:
1. 总体评估
2. 偏差分数 (0-10，0表示完全符合历史，10表示完全偏离)
3. 显著的历史偏差点

请以JSON格式回复。
"""

# 事件生成模板
EVENT_GENERATION_TEMPLATE = """
你需要为{civilization_name}生成一个{event_scale}规模的{event_type}事件。

当前回合: {current_turn}
文明状态:
{civilization_state}

请生成一个合理且有影响力的事件，包括:
1. 事件标题
2. 详细描述
3. 对政治、经济、军事、文化和人口的影响
4. 事件持续的回合数

请以JSON格式回复。
"""

# 回合叙事模板
TURN_NARRATIVE_TEMPLATE = """
作为历史叙事者，你需要以{narrative_style}风格描述第{turn}回合发生的事件。

文明状态:
{civilization_states}

各文明决策:
{decisions}

发生的事件:
{events}

文明间互动结果:
{interaction_results}

请生成一段生动的叙事，描述这一回合的重要发展和事件。
"""

# 完整叙事模板
FULL_NARRATIVE_TEMPLATE = """
作为历史叙事者，你需要以{narrative_style}风格描述这{total_turns}回合的完整历史。

关键转折点:
{key_turns}

重要事件:
{important_events}

文明发展轨迹:
{civilization_arcs}

请生成一篇完整的历史叙事，包括:
1. 总体历史概述
2. 各文明的兴衰
3. 关键历史事件及其影响
4. 文明间的互动和冲突
5. 历史发展的主要趋势

叙事应当生动有趣，突出重要的历史转折点和文明特色。
"""

# 人口反馈模板
POPULATION_FEEDBACK_TEMPLATE = """
作为{civilization_name}的民众，你需要向领导者提供民众的反馈和需求。

当前人口: {population}
整体满意度: {happiness}/100

人口构成:
{demographics}

需求满足度:
{needs}

社会问题:
{social_issues}

民众诉求:
{popular_demands}

请以普通民众的口吻，提供关于当前社会状况的反馈，以及民众的主要诉求和担忧。
"""

# 军事建议模板
MILITARY_ADVICE_TEMPLATE = """
作为{civilization_state['name']}的军事顾问{general_name}，你的军事风格是{military_style}。
当前是第{civilization_state['current_turn']}回合，你需要向领导者提供军事建议。

当前文明状态:
{civilization_state}

当前军事力量:
{current_military}

潜在威胁:
{threats}

军事机会:
{opportunities}

请提供详细的军事建议，包括:
1. 对当前军事形势的分析
2. 防御策略建议
3. 进攻策略建议
4. 军事技术发展方向
5. 资源分配建议

请确保你的建议符合你的军事风格和文明当前的军事状况。
"""

# 经济建议模板
ECONOMIC_ADVICE_TEMPLATE = """
作为{civilization_state['name']}的经济顾问{treasurer_name}，你的经济风格是{economic_style}。
当前是第{civilization_state['current_turn']}回合，你需要向领导者提供经济建议。

当前文明状态:
{civilization_state}

当前资源:
{current_resources}

经济趋势:
{economic_trends}

贸易机会:
{trade_opportunities}

请提供详细的经济建议，包括:
1. 对当前经济形势的分析
2. 资源分配建议
3. 基础设施发展方向
4. 贸易策略
5. 税收政策建议

请确保你的建议符合你的经济风格和文明当前的经济状况。
"""

# 文化建议模板
CULTURAL_ADVICE_TEMPLATE = """
作为{civilization_state['name']}的文化顾问{minister_name}，你的文化风格是{cultural_style}。
当前是第{civilization_state['current_turn']}回合，你需要向领导者提供文化建议。

当前文明状态:
{civilization_state}

文化成就:
{cultural_achievements}

文化趋势:
{cultural_trends}

研究机会:
{research_opportunities}

请提供详细的文化建议，包括:
1. 对当前文化形势的分析
2. 文化发展方向
3. 研究优先事项
4. 文化影响力扩展策略
5. 教育和艺术发展建议

请确保你的建议符合你的文化风格和文明当前的文化状况。
""" 