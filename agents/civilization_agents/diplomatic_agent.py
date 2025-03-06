from agents.base_agent import BaseAgent
from llm.prompt_templates import DIPLOMATIC_ADVICE_TEMPLATE, DIPLOMATIC_NEGOTIATION_TEMPLATE

class DiplomaticAgent(BaseAgent):
    """负责外交关系的Agent"""
    
    def __init__(self, name, civilization_id, diplomatic_style, llm_interface=None):
        super().__init__(name, civilization_id, llm_interface)
        self.diplomatic_style = diplomatic_style  # 例如：和平、好战、孤立等
        self.relations = {}  # 与其他文明的关系状态
        
    def update_relations(self, other_civ_id, relation_change):
        """更新与其他文明的关系"""
        if other_civ_id not in self.relations:
            self.relations[other_civ_id] = 0  # 中立关系
        
        self.relations[other_civ_id] += relation_change
        # 限制关系值在一定范围内
        self.relations[other_civ_id] = max(-100, min(100, self.relations[other_civ_id]))
        
    def provide_advice(self, world_state):
        """向领导提供外交建议"""
        civilization_state = world_state.get_civilization_state(self.civilization_id)
        other_civs = world_state.get_other_civilizations(self.civilization_id)
        
        prompt = DIPLOMATIC_ADVICE_TEMPLATE.format(
            diplomat_name=self.name,
            diplomatic_style=self.diplomatic_style,
            civilization_state=civilization_state,
            other_civilizations=other_civs,
            current_relations=self.relations
        )
        
        advice = self.generate_decision(prompt)
        
        # 记录到记忆
        self.add_to_memory({
            'turn': world_state.current_turn,
            'type': 'advice',
            'content': advice
        })
        
        return advice
        
    def negotiate(self, other_diplomat, world_state, topic):
        """与其他文明的外交Agent进行谈判"""
        our_civ = world_state.get_civilization_state(self.civilization_id)
        their_civ = world_state.get_civilization_state(other_diplomat.civilization_id)
        current_relation = self.relations.get(other_diplomat.civilization_id, 0)
        
        prompt = DIPLOMATIC_NEGOTIATION_TEMPLATE.format(
            diplomat_name=self.name,
            diplomatic_style=self.diplomatic_style,
            our_civilization=our_civ,
            their_civilization=their_civ,
            current_relation=current_relation,
            negotiation_topic=topic
        )
        
        negotiation_stance = self.generate_decision(prompt)
        
        # 记录到记忆
        self.add_to_memory({
            'turn': world_state.current_turn,
            'type': 'negotiation',
            'with': other_diplomat.civilization_id,
            'topic': topic,
            'stance': negotiation_stance
        })
        
        return negotiation_stance
    
    def process(self, world_state, **kwargs):
        """处理当前回合的外交事务"""
        # 实现外交行动，如主动联系其他文明等
        diplomatic_actions = []
        
        # 检查是否需要与其他文明进行外交互动
        for civ_id, relation in self.relations.items():
            if kwargs.get('forced_diplomacy') or self._should_initiate_diplomacy(civ_id, relation):
                action = self._initiate_diplomatic_action(civ_id, relation, world_state)
                diplomatic_actions.append(action)
        
        return diplomatic_actions
    
    def _should_initiate_diplomacy(self, civ_id, relation):
        """决定是否应该主动与某文明进行外交"""
        # 这里可以实现更复杂的逻辑
        return True
    
    def _initiate_diplomatic_action(self, civ_id, relation, world_state):
        """发起外交行动"""
        # 实现具体的外交行动逻辑
        pass 