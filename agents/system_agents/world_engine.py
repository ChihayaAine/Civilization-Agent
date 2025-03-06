from agents.base_agent import BaseAgent
from models.world_state import WorldState
import random
import math

class WorldEngineAgent(BaseAgent):
    """控制自然环境和资源变化的系统级Agent"""
    
    def __init__(self, name, llm_interface=None):
        super().__init__(name, None, llm_interface)  # 系统级Agent没有文明ID
        self.terrain_types = ['plains', 'mountains', 'forest', 'desert', 'tundra', 'coast', 'ocean']
        self.resource_types = ['food', 'wood', 'stone', 'iron', 'gold', 'oil', 'uranium']
        self.climate_zones = ['tropical', 'temperate', 'arid', 'continental', 'polar']
        self.current_climate = {}  # 每个区域的当前气候状态
        
    def initialize_world(self, config):
        """初始化世界状态"""
        world_size = config.world_size
        
        # 创建地形
        terrain = self._generate_terrain(world_size)
        
        # 分配资源
        resources = self._distribute_resources(terrain, config.resource_distribution)
        
        # 设置初始气候
        climate = self._initialize_climate(terrain)
        
        # 创建世界状态
        world_state = WorldState(
            size=world_size,
            terrain=terrain,
            resources=resources,
            climate=climate,
            current_turn=0
        )
        
        return world_state
    
    def update_environment(self, world_state):
        """更新环境状态"""
        # 更新回合数
        world_state.current_turn += 1
        
        # 更新气候
        self._update_climate(world_state)
        
        # 更新自然资源
        self._update_resources(world_state)
        
        # 可能触发自然灾害
        self._generate_natural_disasters(world_state)
        
        return world_state
    
    def process(self, world_state, **kwargs):
        """处理当前回合的环境变化"""
        return self.update_environment(world_state)
    
    def _generate_terrain(self, world_size):
        """生成地形"""
        width, height = world_size['width'], world_size['height']
        terrain = {}
        
        # 简单随机地形生成
        for x in range(width):
            for y in range(height):
                terrain_type = random.choice(self.terrain_types)
                terrain[f"{x},{y}"] = {
                    'type': terrain_type,
                    'elevation': random.uniform(0, 1) if terrain_type != 'ocean' else 0,
                    'fertility': random.uniform(0, 1) if terrain_type in ['plains', 'forest'] else 0.1
                }
        
        return terrain
    
    def _distribute_resources(self, terrain, distribution_type):
        """分配资源"""
        resources = {}
        
        # 根据地形类型分配资源
        for coord, tile in terrain.items():
            tile_resources = {}
            terrain_type = tile['type']
            
            if terrain_type == 'plains':
                tile_resources['food'] = random.uniform(50, 100)
            elif terrain_type == 'forest':
                tile_resources['wood'] = random.uniform(50, 100)
                tile_resources['food'] = random.uniform(20, 50)
            elif terrain_type == 'mountains':
                tile_resources['stone'] = random.uniform(50, 100)
                tile_resources['iron'] = random.uniform(10, 30)
                if random.random() < 0.2:  # 20%几率有金矿
                    tile_resources['gold'] = random.uniform(5, 20)
            elif terrain_type == 'desert':
                if random.random() < 0.1:  # 10%几率有油田
                    tile_resources['oil'] = random.uniform(20, 50)
            
            resources[coord] = tile_resources
        
        # 如果是随机分布，再添加一些随机资源
        if distribution_type == 'random':
            for coord in resources:
                if random.random() < 0.05:  # 5%几率有稀有资源
                    rare_resource = random.choice(['gold', 'oil', 'uranium'])
                    resources[coord][rare_resource] = random.uniform(5, 15)
        
        return resources
    
    def _initialize_climate(self, terrain):
        """初始化气候"""
        climate = {}
        
        for coord, tile in terrain.items():
            # 基于地形和随机因素确定气候区
            if tile['type'] in ['ocean', 'coast']:
                climate_zone = 'temperate'
            elif tile['type'] == 'tundra':
                climate_zone = 'polar'
            elif tile['type'] == 'desert':
                climate_zone = 'arid'
            else:
                climate_zone = random.choice(self.climate_zones)
            
            # 设置初始气候状态
            climate[coord] = {
                'zone': climate_zone,
                'temperature': self._get_base_temperature(climate_zone) + random.uniform(-3, 3),
                'precipitation': self._get_base_precipitation(climate_zone) + random.uniform(-10, 10),
                'wind_speed': random.uniform(0, 10),
                'wind_direction': random.uniform(0, 360)
            }
            
            # 记录当前气候状态
            self.current_climate[coord] = climate[coord].copy()
        
        return climate
    
    def _get_base_temperature(self, climate_zone):
        """获取基础温度"""
        base_temps = {
            'tropical': 28,
            'temperate': 15,
            'arid': 25,
            'continental': 10,
            'polar': -10
        }
        return base_temps.get(climate_zone, 15)
    
    def _get_base_precipitation(self, climate_zone):
        """获取基础降水量"""
        base_precip = {
            'tropical': 80,
            'temperate': 50,
            'arid': 10,
            'continental': 40,
            'polar': 20
        }
        return base_precip.get(climate_zone, 40)
    
    def _update_climate(self, world_state):
        """更新气候状态"""
        for coord, climate in world_state.climate.items():
            # 获取当前气候
            current = self.current_climate.get(coord, climate.copy())
            
            # 计算季节因素 (假设4个回合为一年)
            season_factor = math.sin(2 * math.pi * (world_state.current_turn % 4) / 4)
            
            # 更新温度 (季节变化 + 随机波动)
            temp_change = season_factor * 10 + random.uniform(-2, 2)
            current['temperature'] += temp_change * 0.1  # 缓慢变化
            
            # 更新降水 (季节变化 + 随机波动)
            precip_change = season_factor * 20 + random.uniform(-5, 5)
            current['precipitation'] += precip_change * 0.1  # 缓慢变化
            
            # 更新风速和风向
            current['wind_speed'] = max(0, current['wind_speed'] + random.uniform(-1, 1))
            current['wind_direction'] = (current['wind_direction'] + random.uniform(-10, 10)) % 360
            
            # 保存更新后的气候
            self.current_climate[coord] = current
            world_state.climate[coord] = current.copy()
    
    def _update_resources(self, world_state):
        """更新自然资源"""
        for coord, resources in world_state.resources.items():
            terrain = world_state.terrain.get(coord, {})
            climate = world_state.climate.get(coord, {})
            
            # 更新可再生资源
            if 'food' in resources:
                # 食物生长受气候和地形影响
                growth_factor = self._calculate_growth_factor(terrain, climate)
                resources['food'] = min(100, resources['food'] * (1 + growth_factor * 0.1))
            
            if 'wood' in resources and terrain.get('type') == 'forest':
                # 木材再生
                resources['wood'] = min(100, resources['wood'] * 1.02)
    
    def _calculate_growth_factor(self, terrain, climate):
        """计算生长因子"""
        # 基础生长因子
        base_factor = 0
        
        # 地形影响
        if terrain.get('type') == 'plains':
            base_factor += 0.5
        elif terrain.get('type') == 'forest':
            base_factor += 0.3
        
        # 气候影响
        temp = climate.get('temperature', 15)
        precip = climate.get('precipitation', 40)
        
        # 温度影响 (最适宜温度为15-25度)
        if 15 <= temp <= 25:
            temp_factor = 0.5
        elif 5 <= temp < 15 or 25 < temp <= 35:
            temp_factor = 0.3
        else:
            temp_factor = 0.1
        
        # 降水影响 (最适宜降水为40-60mm)
        if 40 <= precip <= 60:
            precip_factor = 0.5
        elif 20 <= precip < 40 or 60 < precip <= 80:
            precip_factor = 0.3
        else:
            precip_factor = 0.1
        
        return base_factor + temp_factor + precip_factor
    
    def _generate_natural_disasters(self, world_state):
        """生成自然灾害"""
        # 每回合有5%的几率发生自然灾害
        if random.random() < 0.05:
            disaster_type = random.choice(['drought', 'flood', 'earthquake', 'hurricane', 'wildfire'])
            affected_coords = self._select_disaster_area(world_state, disaster_type)
            
            # 创建灾害事件
            disaster = {
                'type': disaster_type,
                'affected_area': affected_coords,
                'severity': random.choice(['mild', 'moderate', 'severe']),
                'turn': world_state.current_turn
            }
            
            # 应用灾害效果
            self._apply_disaster_effects(world_state, disaster)
            
            # 添加到世界状态的灾害列表
            if not hasattr(world_state, 'disasters'):
                world_state.disasters = []
            world_state.disasters.append(disaster)
    
    def _select_disaster_area(self, world_state, disaster_type):
        """选择灾害影响区域"""
        all_coords = list(world_state.terrain.keys())
        center = random.choice(all_coords)
        
        # 根据灾害类型确定影响范围
        if disaster_type in ['earthquake', 'hurricane']:
            radius = random.randint(3, 5)
        else:
            radius = random.randint(1, 3)
        
        # 选择中心点周围的区域
        affected_coords = [center]
        center_x, center_y = map(int, center.split(','))
        
        for x in range(center_x - radius, center_x + radius + 1):
            for y in range(center_y - radius, center_y + radius + 1):
                coord = f"{x},{y}"
                if coord in world_state.terrain and coord != center:
                    # 计算到中心的距离
                    distance = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
                    if distance <= radius:
                        affected_coords.append(coord)
        
        return affected_coords
    
    def _apply_disaster_effects(self, world_state, disaster):
        """应用灾害效果"""
        severity_factor = {
            'mild': 0.2,
            'moderate': 0.5,
            'severe': 0.8
        }.get(disaster['severity'], 0.5)
        
        for coord in disaster['affected_area']:
            # 影响资源
            if coord in world_state.resources:
                resources = world_state.resources[coord]
                
                if disaster['type'] == 'drought':
                    # 干旱减少食物
                    if 'food' in resources:
                        resources['food'] *= (1 - severity_factor)
                
                elif disaster['type'] == 'flood':
                    # 洪水减少食物和木材
                    for resource in ['food', 'wood']:
                        if resource in resources:
                            resources[resource] *= (1 - severity_factor)
                
                elif disaster['type'] == 'earthquake':
                    # 地震减少所有资源
                    for resource in resources:
                        resources[resource] *= (1 - severity_factor * 0.5)
                
                elif disaster['type'] == 'hurricane':
                    # 飓风减少食物和木材
                    for resource in ['food', 'wood']:
                        if resource in resources:
                            resources[resource] *= (1 - severity_factor * 0.7)
                
                elif disaster['type'] == 'wildfire':
                    # 野火减少木材和食物
                    for resource in ['wood', 'food']:
                        if resource in resources:
                            resources[resource] *= (1 - severity_factor * 0.9) 