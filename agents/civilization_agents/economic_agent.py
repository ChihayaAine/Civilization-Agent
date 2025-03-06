from agents.base_agent import BaseAgent
from llm.prompt_templates import ECONOMIC_ADVICE_TEMPLATE

class EconomicAgent(BaseAgent):
    """负责经济事务的Agent"""
    
    def __init__(self, name, civilization_id, economic_style, llm_interface=None):
        super().__init__(name, civilization_id, llm_interface)
        self.economic_style = economic_style  # 例如：自由市场、计划经济、混合等
        self.resources = {}  # 资源库存
        self.infrastructure = {}  # 基础设施
        self.trade_agreements = []  # 贸易协议
        
    def provide_advice(self, world_state):
        """向领导提供经济建议"""
        civilization_state = world_state.get_civilization_state(self.civilization_id)
        economic_trends = self._analyze_economic_trends(world_state)
        trade_opportunities = self._analyze_trade_opportunities(world_state)
        
        prompt = ECONOMIC_ADVICE_TEMPLATE.format(
            treasurer_name=self.name,
            economic_style=self.economic_style,
            civilization_state=civilization_state,
            resources=self.resources,
            infrastructure=self.infrastructure,
            trade_agreements=self.trade_agreements,
            economic_trends=economic_trends,
            trade_opportunities=trade_opportunities
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
        """处理当前回合的经济事务"""
        leader_decision = kwargs.get('leader_decision', '')
        
        # 分析领导决策中的经济指令
        economic_orders = self._extract_economic_orders(leader_decision)
        
        # 执行经济行动
        actions = []
        for order in economic_orders:
            action = self._execute_economic_order(order, world_state)
            if action:
                actions.append(action)
                
        return actions
    
    def _analyze_economic_trends(self, world_state):
        """分析经济趋势"""
        # 实现经济趋势分析逻辑
        return {
            'growth_rate': 0.03,  # 示例值
            'inflation': 0.02,    # 示例值
            'unemployment': 0.05, # 示例值
            'market_stability': 'stable'
        }
    
    def _analyze_trade_opportunities(self, world_state):
        """分析贸易机会"""
        opportunities = []
        other_civs = world_state.get_other_civilizations(self.civilization_id)
        
        for civ_id, civ_state in other_civs.items():
            # 简单贸易机会评估逻辑
            our_resources = self.resources
            their_resources = civ_state.get('resources', {})
            
            for resource, amount in our_resources.items():
                if resource not in their_resources and amount > 100:
                    opportunities.append({
                        'civilization_id': civ_id,
                        'name': civ_state.get('name', f'Civilization {civ_id}'),
                        'resource': resource,
                        'type': 'export'
                    })
            
            for resource, amount in their_resources.items():
                if resource not in our_resources and amount > 100:
                    opportunities.append({
                        'civilization_id': civ_id,
                        'name': civ_state.get('name', f'Civilization {civ_id}'),
                        'resource': resource,
                        'type': 'import'
                    })
        
        return opportunities
    
    def _extract_economic_orders(self, leader_decision):
        """从领导决策中提取经济命令"""
        # 使用LLM解析领导决策中的经济部分
        prompt = f"""
        从以下领导决策中提取经济命令:
        
        {leader_decision}
        
        请以JSON格式返回经济命令列表，每个命令包含:
        1. 命令类型(建设、贸易、税收调整、资源分配等)
        2. 目标(如果适用)
        3. 资源分配
        4. 优先级
        """
        
        try:
            response = self.llm_interface.generate_structured_response(
                prompt, 
                response_format={
                    "economic_orders": [
                        {
                            "type": "string",
                            "target": "string or null",
                            "resources": "number",
                            "priority": "number"
                        }
                    ]
                }
            )
            return response.get("economic_orders", [])
        except:
            # 如果结构化解析失败，返回空列表
            return []
    
    def _execute_economic_order(self, order, world_state):
        """执行特定的经济命令"""
        order_type = order.get('type', '').lower()
        
        if order_type == 'build':
            return self._build_infrastructure(order, world_state)
        elif order_type == 'trade':
            return self._establish_trade(order, world_state)
        elif order_type == 'tax':
            return self._adjust_taxation(order, world_state)
        elif order_type == 'allocate':
            return self._allocate_resources(order, world_state)
        else:
            return None
    
    def _build_infrastructure(self, order, world_state):
        """建设基础设施"""
        # 实现建设逻辑
        return {
            'action': 'build_infrastructure',
            'details': order,
            'result': 'pending'
        }
    
    def _establish_trade(self, order, world_state):
        """建立贸易关系"""
        # 实现贸易逻辑
        return {
            'action': 'establish_trade',
            'details': order,
            'result': 'pending'
        }
    
    def _adjust_taxation(self, order, world_state):
        """调整税收"""
        # 实现税收调整逻辑
        return {
            'action': 'adjust_taxation',
            'details': order,
            'result': 'pending'
        }
    
    def _allocate_resources(self, order, world_state):
        """分配资源"""
        # 实现资源分配逻辑
        return {
            'action': 'allocate_resources',
            'details': order,
            'result': 'pending'
        } 