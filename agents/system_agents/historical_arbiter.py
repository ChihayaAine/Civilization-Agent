from agents.base_agent import BaseAgent
from llm.prompt_templates import HISTORICAL_ASSESSMENT_TEMPLATE

class HistoricalArbiterAgent(BaseAgent):
    """评估模拟与真实历史的偏差的系统级Agent"""
    
    def __init__(self, name, llm_interface=None):
        super().__init__(name, None, llm_interface)  # 系统级Agent没有文明ID
        self.historical_references = {}  # 存储历史参考数据
        self.divergence_points = []  # 记录历史偏差点
        
    def load_historical_references(self, references):
        """加载历史参考数据"""
        self.historical_references = references
        
    def assess(self, world_state):
        """评估当前世界状态与历史的偏差"""
        # 准备评估数据
        current_state_summary = self._summarize_world_state(world_state)
        historical_reference = self._get_relevant_historical_reference(world_state.current_turn)
        
        # 如果没有相关历史参考，返回空评估
        if not historical_reference:
            return {
                'turn': world_state.current_turn,
                'assessment': 'No historical reference available',
                'divergence_score': 0,
                'notable_divergences': []
            }
        
        # 使用LLM评估历史偏差
        prompt = HISTORICAL_ASSESSMENT_TEMPLATE.format(
            current_turn=world_state.current_turn,
            current_state=current_state_summary,
            historical_reference=historical_reference
        )
        
        assessment_response = self.generate_structured_response(
            prompt,
            response_format={
                'assessment': 'Overall assessment of historical accuracy',
                'divergence_score': 'A score from 0 to 10 where 0 is completely accurate and 10 is completely divergent',
                'notable_divergences': ['List of specific divergences from historical record']
            }
        )
        
        # 记录显著偏差点
        if assessment_response.get('divergence_score', 0) > 5:
            self.divergence_points.append({
                'turn': world_state.current_turn,
                'assessment': assessment_response
            })
        
        return assessment_response
    
    def process(self, world_state, **kwargs):
        """处理当前回合的历史评估"""
        return self.assess(world_state)
    
    def _summarize_world_state(self, world_state):
        """生成世界状态摘要"""
        summary = {
            'turn': world_state.current_turn,
            'civilizations': {}
        }
        
        for civ_id, state in world_state.civilization_states.items():
            summary['civilizations'][civ_id] = {
                'name': state.get('name', f'Civilization {civ_id}'),
                'population': state.get('population', 0),
                'military_power': state.get('military_power', 0),
                'technology_level': state.get('technology_level', 0),
                'cultural_influence': state.get('cultural_influence', 0),
                'diplomatic_relations': state.get('diplomatic_relations', {})
            }
        
        # 添加最近的重大事件
        recent_events = [event for event in world_state.events 
                        if world_state.current_turn - event.get('turn', 0) <= 5]
        summary['recent_events'] = recent_events
        
        return summary
    
    def _get_relevant_historical_reference(self, turn):
        """获取与当前回合相关的历史参考"""
        # 这里可以实现更复杂的逻辑，例如基于时间线映射等
        return self.historical_references.get(str(turn), None) 