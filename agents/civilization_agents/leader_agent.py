from agents.base_agent import BaseAgent
from llm.prompt_templates import LEADER_DECISION_TEMPLATE

class LeaderAgent(BaseAgent):
    """文明的领导Agent，负责最终决策"""
    
    def __init__(self, name, civilization_id, leadership_style, llm_interface=None):
        super().__init__(name, civilization_id, llm_interface)
        self.leadership_style = leadership_style  # 例如：独裁、民主、军事等
        self.advisors = {}  # 存储顾问Agent的引用
        
    def register_advisor(self, role, agent):
        """注册顾问Agent"""
        self.advisors[role] = agent
        
    def collect_advice(self, world_state):
        """从所有顾问收集建议"""
        advice = {}
        for role, advisor in self.advisors.items():
            advice[role] = advisor.provide_advice(world_state)
        return advice
        
    def process(self, world_state, **kwargs):
        """处理当前状态并做出领导决策"""
        # 收集所有顾问的建议
        advice = self.collect_advice(world_state)
        
        # 准备决策提示
        civilization_state = world_state.get_civilization_state(self.civilization_id)
        prompt = LEADER_DECISION_TEMPLATE.format(
            leader_name=self.name,
            leadership_style=self.leadership_style,
            civilization_state=civilization_state,
            diplomatic_advice=advice.get('diplomatic', 'No advice'),
            military_advice=advice.get('military', 'No advice'),
            economic_advice=advice.get('economic', 'No advice'),
            cultural_advice=advice.get('cultural', 'No advice'),
            population_feedback=advice.get('population', 'No feedback')
        )
        
        # 使用LLM生成决策
        decision = self.generate_decision(prompt)
        
        # 记录决策到记忆
        self.add_to_memory({
            'turn': world_state.current_turn,
            'type': 'decision',
            'content': decision
        })
        
        return decision 