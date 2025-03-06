class WorldState:
    """世界状态模型，包含地形、资源、气候和文明状态"""
    
    def __init__(self, size, terrain, resources, climate, current_turn=0):
        self.size = size  # 世界大小
        self.terrain = terrain  # 地形数据
        self.resources = resources  # 资源分布
        self.climate = climate  # 气候状态
        self.current_turn = current_turn  # 当前回合
        self.civilization_states = {}  # 各文明状态
        self.events = []  # 事件记录
        self.disasters = []  # 自然灾害
        
    def get_civilization_state(self, civilization_id):
        """获取特定文明的状态"""
        return self.civilization_states.get(civilization_id, {})
    
    def get_other_civilizations(self, civilization_id):
        """获取除指定文明外的所有其他文明状态"""
        return {civ_id: state for civ_id, state in self.civilization_states.items() if civ_id != civilization_id}
    
    def update_civilization_state(self, civilization_id, state_update):
        """更新文明状态"""
        if civilization_id not in self.civilization_states:
            self.civilization_states[civilization_id] = {}
        
        self.civilization_states[civilization_id].update(state_update)
    
    def add_event(self, event):
        """添加事件"""
        event['turn'] = self.current_turn
        self.events.append(event)
    
    def get_region_resources(self, region_coords):
        """获取特定区域的资源"""
        region_resources = {}
        
        for coord in region_coords:
            if coord in self.resources:
                for resource_type, amount in self.resources[coord].items():
                    if resource_type in region_resources:
                        region_resources[resource_type] += amount
                    else:
                        region_resources[resource_type] = amount
        
        return region_resources
    
    def get_region_climate(self, region_coords):
        """获取特定区域的气候状态"""
        if not region_coords:
            return {}
        
        # 计算区域平均气候
        avg_temp = 0
        avg_precip = 0
        avg_wind_speed = 0
        wind_directions = []
        
        for coord in region_coords:
            if coord in self.climate:
                climate = self.climate[coord]
                avg_temp += climate.get('temperature', 0)
                avg_precip += climate.get('precipitation', 0)
                avg_wind_speed += climate.get('wind_speed', 0)
                wind_directions.append(climate.get('wind_direction', 0))
        
        count = len(region_coords)
        return {
            'temperature': avg_temp / count,
            'precipitation': avg_precip / count,
            'wind_speed': avg_wind_speed / count,
            'wind_direction': sum(wind_directions) / len(wind_directions) if wind_directions else 0
        }
    
    def get_disasters_in_region(self, region_coords, turns_ago=None):
        """获取特定区域的灾害"""
        region_disasters = []
        
        for disaster in self.disasters:
            # 检查是否在指定回合范围内
            if turns_ago is not None and self.current_turn - disaster['turn'] > turns_ago:
                continue
                
            # 检查是否影响了指定区域
            affected_region = False
            for coord in disaster['affected_area']:
                if coord in region_coords:
                    affected_region = True
                    break
            
            if affected_region:
                region_disasters.append(disaster)
        
        return region_disasters
    
    def to_dict(self):
        """将世界状态转换为字典"""
        return {
            'size': self.size,
            'current_turn': self.current_turn,
            'civilization_states': self.civilization_states,
            'events': self.events,
            'disasters': self.disasters
        } 