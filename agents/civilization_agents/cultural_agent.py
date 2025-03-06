from agents.base_agent import BaseAgent
from llm.prompt_templates import CULTURAL_ADVICE_TEMPLATE

class CulturalAgent(BaseAgent):
    """负责文化事务的Agent"""
    
    def __init__(self, name, civilization_id, cultural_style, llm_interface=None):
        super().__init__(name, civilization_id, llm_interface)
        self.cultural_style = cultural_style  # 例如：传统、创新、多元等
        self.cultural_achievements = []  # 文化成就
        self.research_projects = {}  # 研究项目
        self.cultural_influence = {}  # 对其他文明的文化影响
        
    def provide_advice(self, world_state):
        """向领导提供文化建议"""
        civilization_state = world_state.get_civilization_state(self.civilization_id)
        cultural_trends = self._analyze_cultural_trends(world_state)
        research_opportunities = self._analyze_research_opportunities(world_state)
        
        prompt = CULTURAL_ADVICE_TEMPLATE.format(
            minister_name=self.name,
            cultural_style=self.cultural_style,
            civilization_state=civilization_state,
            cultural_achievements=self.cultural_achievements,
            research_projects=self.research_projects,
            cultural_influence=self.cultural_influence,
            cultural_trends=cultural_trends,
            research_opportunities=research_opportunities
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
        """处理当前回合的文化事务"""
        leader_decision = kwargs.get('leader_decision', '')
        
        # 分析领导决策中的文化指令
        cultural_orders = self._extract_cultural_orders(leader_decision)
        
        # 执行文化行动
        actions = []
        for order in cultural_orders:
            action = self._execute_cultural_order(order, world_state)
            if action:
                actions.append(action)
                
        return actions
    
    def _analyze_cultural_trends(self, world_state):
        """分析文化趋势"""
        # 实现文化趋势分析逻辑
        return {
            'dominant_ideology': 'humanism',  # 示例值
            'artistic_movements': ['realism', 'expressionism'],
            'religious_trends': 'secularization',
            'social_values': ['individualism', 'equality']
        }
    
    def _analyze_research_opportunities(self, world_state):
        """分析研究机会"""
        opportunities = []
        our_tech = world_state.get_civilization_state(self.civilization_id).get('technology', {})
        
        # 简单研究机会评估逻辑
        all_possible_tech = {
            'writing': {'prerequisites': []},
            'mathematics': {'prerequisites': ['writing']},
            'philosophy': {'prerequisites': ['writing']},
            'astronomy': {'prerequisites': ['mathematics']},
            'physics': {'prerequisites': ['mathematics', 'astronomy']},
            'chemistry': {'prerequisites': ['physics']},
            'biology': {'prerequisites': ['chemistry']},
            'medicine': {'prerequisites': ['biology']},
            'engineering': {'prerequisites': ['mathematics', 'physics']},
            'metallurgy': {'prerequisites': ['chemistry', 'engineering']},
            'printing': {'prerequisites': ['writing', 'engineering']},
            'gunpowder': {'prerequisites': ['chemistry', 'metallurgy']},
            'steam_power': {'prerequisites': ['physics', 'engineering']},
            'electricity': {'prerequisites': ['physics', 'engineering']},
            'radio': {'prerequisites': ['electricity']},
            'computers': {'prerequisites': ['electricity', 'mathematics']},
            'nuclear_power': {'prerequisites': ['physics', 'engineering']},
            'space_flight': {'prerequisites': ['physics', 'engineering', 'computers']},
            'internet': {'prerequisites': ['computers', 'radio']},
            'artificial_intelligence': {'prerequisites': ['computers', 'mathematics']}
        }
        
        for tech, info in all_possible_tech.items():
            if tech not in our_tech:
                # 检查是否满足前提条件
                prerequisites_met = True
                for prereq in info['prerequisites']:
                    if prereq not in our_tech:
                        prerequisites_met = False
                        break
                
                if prerequisites_met:
                    opportunities.append({
                        'technology': tech,
                        'prerequisites': info['prerequisites'],
                        'potential_impact': 'high' if len(info['prerequisites']) > 2 else 'medium'
                    })
        
        return opportunities
    
    def _extract_cultural_orders(self, leader_decision):
        """从领导决策中提取文化命令"""
        # 使用LLM解析领导决策中的文化部分
        prompt = f"""
        从以下领导决策中提取文化和研究命令:
        
        {leader_decision}
        
        请以JSON格式返回文化命令列表，每个命令包含:
        1. 命令类型(研究、艺术项目、宗教活动、教育等)
        2. 目标(如果适用)
        3. 资源分配
        4. 优先级
        """
        
        try:
            response = self.llm_interface.generate_structured_response(
                prompt, 
                response_format={
                    "cultural_orders": [
                        {
                            "type": "string",
                            "target": "string or null",
                            "resources": "number",
                            "priority": "number"
                        }
                    ]
                }
            )
            return response.get("cultural_orders", [])
        except:
            # 如果结构化解析失败，返回空列表
            return []
    
    def _execute_cultural_order(self, order, world_state):
        """执行特定的文化命令"""
        order_type = order.get('type', '').lower()
        
        if order_type == 'research':
            return self._conduct_research(order, world_state)
        elif order_type == 'art':
            return self._create_art(order, world_state)
        elif order_type == 'religion':
            return self._religious_activity(order, world_state)
        elif order_type == 'education':
            return self._improve_education(order, world_state)
        else:
            return None
    
    def _conduct_research(self, order, world_state):
        """进行研究"""
        # 实现研究逻辑
        return {
            'action': 'conduct_research',
            'details': order,
            'result': 'pending'
        }
    
    def _create_art(self, order, world_state):
        """创作艺术作品"""
        # 实现艺术创作逻辑
        return {
            'action': 'create_art',
            'details': order,
            'result': 'pending'
        }
    
    def _religious_activity(self, order, world_state):
        """宗教活动"""
        # 实现宗教活动逻辑
        return {
            'action': 'religious_activity',
            'details': order,
            'result': 'pending'
        }
    
    def _improve_education(self, order, world_state):
        """改善教育"""
        # 实现教育改善逻辑
        return {
            'action': 'improve_education',
            'details': order,
            'result': 'pending'
        } 