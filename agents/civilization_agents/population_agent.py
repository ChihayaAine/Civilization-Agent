from agents.base_agent import BaseAgent
from llm.prompt_templates import POPULATION_FEEDBACK_TEMPLATE

class PopulationAgent(BaseAgent):
    """代表普通民众的Agent"""
    
    def __init__(self, name, civilization_id, initial_population, llm_interface=None):
        super().__init__(name, civilization_id, llm_interface)
        self.population = initial_population
        self.happiness = 50  # 0-100的满意度
        self.demographics = {
            'age_groups': {'young': 0.3, 'adult': 0.5, 'elderly': 0.2},
            'social_classes': {'upper': 0.1, 'middle': 0.3, 'lower': 0.6},
            'occupations': {'farmers': 0.5, 'craftsmen': 0.2, 'merchants': 0.1, 'soldiers': 0.1, 'others': 0.1}
        }
        self.needs = {
            'food': 0.7,  # 满足度 0-1
            'safety': 0.6,
            'housing': 0.5,
            'healthcare': 0.4,
            'education': 0.3,
            'entertainment': 0.2
        }
        
    def provide_advice(self, world_state):
        """向领导提供民众反馈"""
        civilization_state = world_state.get_civilization_state(self.civilization_id)
        social_issues = self._identify_social_issues()
        popular_demands = self._identify_popular_demands()
        
        prompt = POPULATION_FEEDBACK_TEMPLATE.format(
            civilization_name=civilization_state.get('name', f'Civilization {self.civilization_id}'),
            population=self.population,
            happiness=self.happiness,
            demographics=self.demographics,
            needs=self.needs,
            social_issues=social_issues,
            popular_demands=popular_demands
        )
        
        feedback = self.generate_decision(prompt)
        
        # 记录到记忆
        self.add_to_memory({
            'turn': world_state.current_turn,
            'type': 'feedback',
            'content': feedback
        })
        
        return feedback
    
    def process(self, world_state, **kwargs):
        """处理当前回合的人口变化"""
        # 人口Agent主要是被动的，不执行具体行动
        # 但可以模拟人口对领导决策的反应
        leader_decision = kwargs.get('leader_decision', '')
        
        # 分析领导决策对人口的影响
        happiness_change = self._analyze_decision_impact(leader_decision, world_state)
        
        # 更新幸福度
        self.happiness = max(0, min(100, self.happiness + happiness_change))
        
        return {
            'population': self.population,
            'happiness': self.happiness,
            'happiness_change': happiness_change
        }
    
    def update_population(self, civ_state, world_state):
        """更新人口状态"""
        # 计算人口增长率
        growth_rate = self._calculate_growth_rate(civ_state, world_state)
        
        # 更新人口
        old_population = self.population
        self.population = int(self.population * (1 + growth_rate))
        
        # 更新需求满足度
        self._update_needs_satisfaction(civ_state)
        
        return {
            'old_population': old_population,
            'new_population': self.population,
            'growth_rate': growth_rate,
            'needs': self.needs,
            'happiness': self.happiness
        }
    
    def _identify_social_issues(self):
        """识别社会问题"""
        issues = []
        
        # 基于需求满足度识别问题
        for need, satisfaction in self.needs.items():
            if satisfaction < 0.4:
                severity = 'critical' if satisfaction < 0.2 else 'serious'
                affected_groups = self._identify_affected_groups(need)
                
                issues.append({
                    'type': f'lack_of_{need}',
                    'severity': severity,
                    'affected_groups': affected_groups
                })
        
        # 基于幸福度识别问题
        if self.happiness < 30:
            issues.append({
                'type': 'general_unrest',
                'severity': 'critical' if self.happiness < 15 else 'serious',
                'affected_groups': ['all']
            })
        
        return issues
    
    def _identify_popular_demands(self):
        """识别民众需求"""
        demands = []
        
        # 基于需求满足度识别需求
        for need, satisfaction in self.needs.items():
            if satisfaction < 0.6:
                demands.append({
                    'type': f'improve_{need}',
                    'urgency': 'high' if satisfaction < 0.3 else 'medium',
                    'support_level': 'high' if satisfaction < 0.3 else 'medium'
                })
        
        return demands
    
    def _identify_affected_groups(self, need):
        """识别受特定问题影响的人口群体"""
        # 简化逻辑，实际应用中可以更复杂
        if need == 'food':
            return ['lower']
        elif need == 'healthcare':
            return ['elderly', 'lower']
        elif need == 'education':
            return ['young', 'lower']
        else:
            return ['all']
    
    def _analyze_decision_impact(self, decision, world_state):
        """分析领导决策对人口幸福度的影响"""
        # 使用LLM分析决策对人口的影响
        prompt = f"""
        分析以下领导决策对人口幸福度的影响:
        
        决策内容:
        {decision}
        
        当前人口状况:
        - 总人口: {self.population}
        - 幸福度: {self.happiness}/100
        - 人口需求满足度: {self.needs}
        
        请评估这个决策会如何影响人口幸福度，给出一个-10到+10的数值，其中:
        - 负值表示幸福度下降
        - 正值表示幸福度上升
        - 数值大小表示影响程度
        
        只返回一个数字，不要有其他内容。
        """
        
        try:
            response = self.generate_decision(prompt).strip()
            # 尝试将响应转换为数字
            return float(response)
        except:
            # 如果无法解析为数字，假设影响为零
            return 0
    
    def _calculate_growth_rate(self, civ_state, world_state):
        """计算人口增长率"""
        # 基础增长率
        base_rate = 0.01  # 1%的基础增长
        
        # 基于需求满足度调整
        food_factor = self.needs.get('food', 0.5) * 0.02  # 最多+2%
        healthcare_factor = self.needs.get('healthcare', 0.5) * 0.01  # 最多+1%
        
        # 基于幸福度调整
        happiness_factor = (self.happiness - 50) / 1000  # -5%到+5%
        
        # 战争影响
        war_factor = 0
        if civ_state.get('at_war', False):
            war_factor = -0.03  # 战争期间-3%
        
        # 灾难影响
        disaster_factor = 0
        if civ_state.get('disasters', []):
            disaster_factor = -0.05  # 灾难期间-5%
        
        # 计算总增长率
        growth_rate = base_rate + food_factor + healthcare_factor + happiness_factor + war_factor + disaster_factor
        
        # 确保增长率在合理范围内
        return max(-0.1, min(0.1, growth_rate))  # 限制在-10%到+10%之间
    
    def _update_needs_satisfaction(self, civ_state):
        """更新需求满足度"""
        # 基于文明状态更新各项需求的满足度
        resources = civ_state.get('resources', {})
        
        # 食物满足度
        if 'food' in resources:
            food_per_capita = resources['food'] / self.population
            self.needs['food'] = min(1.0, food_per_capita * 10)  # 假设每人需要0.1单位食物
        
        # 安全满足度
        military_power = civ_state.get('military_power', 0)
        self.needs['safety'] = min(1.0, military_power / (self.population * 0.01))  # 假设每100人需要1单位军事力量
        
        # 住房满足度
        if 'housing' in resources:
            housing_per_capita = resources['housing'] / self.population
            self.needs['housing'] = min(1.0, housing_per_capita * 5)  # 假设每人需要0.2单位住房
        
        # 医疗满足度
        if 'healthcare' in resources:
            healthcare_per_capita = resources['healthcare'] / self.population
            self.needs['healthcare'] = min(1.0, healthcare_per_capita * 20)  # 假设每人需要0.05单位医疗
        
        # 教育满足度
        if 'education' in resources:
            education_per_capita = resources['education'] / self.population
            self.needs['education'] = min(1.0, education_per_capita * 10)  # 假设每人需要0.1单位教育
        
        # 娱乐满足度
        if 'entertainment' in resources:
            entertainment_per_capita = resources['entertainment'] / self.population
            self.needs['entertainment'] = min(1.0, entertainment_per_capita * 20)  # 假设每人需要0.05单位娱乐 