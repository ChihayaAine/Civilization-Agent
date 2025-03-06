from agents.base_agent import BaseAgent
from llm.prompt_templates import MILITARY_ADVICE_TEMPLATE

class MilitaryAgent(BaseAgent):
    """负责军事事务的Agent"""
    
    def __init__(self, name, civilization_id, military_style, llm_interface=None):
        super().__init__(name, civilization_id, llm_interface)
        self.military_style = military_style  # 例如：进攻型、防御型、游击型等
        self.military_units = {}  # 军事单位及其数量
        self.military_tech = []   # 已掌握的军事技术
        
    def provide_advice(self, world_state):
        """向领导提供军事建议"""
        civilization_state = world_state.get_civilization_state(self.civilization_id)
        threats = self._analyze_threats(world_state)
        opportunities = self._analyze_opportunities(world_state)
        
        prompt = MILITARY_ADVICE_TEMPLATE.format(
            general_name=self.name,
            military_style=self.military_style,
            civilization_state=civilization_state,
            current_military=self.military_units,
            military_tech=self.military_tech,
            threats=threats,
            opportunities=opportunities
        )
        
        advice = self.generate_decision(prompt)
        
        # 记录到记忆
        self.add_to_memory({
            'turn': world_state.current_turn,
            'type': 'advice',
            'content': advice
        })
        
        return advice
    
    def process(self, world_state, **kwargs):
        """处理当前回合的军事事务"""
        leader_decision = kwargs.get('leader_decision', '')
        
        # 分析领导决策中的军事指令
        military_orders = self._extract_military_orders(leader_decision)
        
        # 执行军事行动
        actions = []
        for order in military_orders:
            action = self._execute_military_order(order, world_state)
            if action:
                actions.append(action)
                
        return actions
    
    def _analyze_threats(self, world_state):
        """分析潜在军事威胁"""
        threats = []
        other_civs = world_state.get_other_civilizations(self.civilization_id)
        
        for civ_id, civ_state in other_civs.items():
            # 简单威胁评估逻辑，可以扩展为更复杂的分析
            if civ_state.get('military_power', 0) > world_state.get_civilization_state(self.civilization_id).get('military_power', 0):
                threats.append({
                    'civilization_id': civ_id,
                    'name': civ_state.get('name', f'Civilization {civ_id}'),
                    'threat_level': 'high',
                    'military_power': civ_state.get('military_power', 0)
                })
            elif civ_state.get('military_power', 0) * 1.5 > world_state.get_civilization_state(self.civilization_id).get('military_power', 0):
                threats.append({
                    'civilization_id': civ_id,
                    'name': civ_state.get('name', f'Civilization {civ_id}'),
                    'threat_level': 'medium',
                    'military_power': civ_state.get('military_power', 0)
                })
        
        return threats
    
    def _analyze_opportunities(self, world_state):
        """分析军事机会"""
        opportunities = []
        other_civs = world_state.get_other_civilizations(self.civilization_id)
        
        for civ_id, civ_state in other_civs.items():
            # 简单机会评估逻辑
            if world_state.get_civilization_state(self.civilization_id).get('military_power', 0) > civ_state.get('military_power', 0) * 1.5:
                opportunities.append({
                    'civilization_id': civ_id,
                    'name': civ_state.get('name', f'Civilization {civ_id}'),
                    'opportunity_type': 'conquest',
                    'military_power': civ_state.get('military_power', 0)
                })
        
        return opportunities
    
    def _extract_military_orders(self, leader_decision):
        """从领导决策中提取军事命令"""
        # 这里可以使用LLM来解析领导决策中的军事部分
        prompt = f"""
        从以下领导决策中提取军事命令:
        
        {leader_decision}
        
        请以JSON格式返回军事命令列表，每个命令包含:
        1. 命令类型(训练、进攻、防御、研发等)
        2. 目标(如果适用)
        3. 资源分配
        4. 优先级
        """
        
        try:
            response = self.llm_interface.generate_structured_response(
                prompt, 
                response_format={
                    "military_orders": [
                        {
                            "type": "string",
                            "target": "string or null",
                            "resources": "number",
                            "priority": "number"
                        }
                    ]
                }
            )
            return response.get("military_orders", [])
        except:
            # 如果结构化解析失败，返回空列表
            return []
    
    def _execute_military_order(self, order, world_state):
        """执行特定的军事命令"""
        order_type = order.get('type', '').lower()
        
        if order_type == 'train':
            return self._train_units(order, world_state)
        elif order_type == 'attack':
            return self._attack_target(order, world_state)
        elif order_type == 'defend':
            return self._strengthen_defense(order, world_state)
        elif order_type == 'research':
            return self._research_technology(order, world_state)
        else:
            return None
    
    def _train_units(self, order, world_state):
        """训练新军事单位"""
        # 实现训练逻辑
        return {
            'action': 'train_units',
            'details': order,
            'result': 'pending'
        }
    
    def _attack_target(self, order, world_state):
        """攻击目标"""
        # 实现攻击逻辑
        return {
            'action': 'attack',
            'details': order,
            'result': 'pending'
        }
    
    def _strengthen_defense(self, order, world_state):
        """加强防御"""
        # 实现防御逻辑
        return {
            'action': 'defend',
            'details': order,
            'result': 'pending'
        }
    
    def _research_technology(self, order, world_state):
        """研究军事技术"""
        # 实现研究逻辑
        return {
            'action': 'research',
            'details': order,
            'result': 'pending'
        } 