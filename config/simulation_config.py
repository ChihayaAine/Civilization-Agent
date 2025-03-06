class SimulationConfig:
    """模拟配置类"""
    
    def __init__(self, **kwargs):
        self.max_turns = kwargs.get('max_turns', 100)
        self.world_size = kwargs.get('world_size', {'width': 100, 'height': 100})
        self.resource_distribution = kwargs.get('resource_distribution', 'random')
        self.climate_enabled = kwargs.get('climate_enabled', True)
        self.disaster_probability = kwargs.get('disaster_probability', 0.05)
        self.historical_accuracy = kwargs.get('historical_accuracy', False)
        self.balance_enabled = kwargs.get('balance_enabled', True)
        self.narrative_style = kwargs.get('narrative_style', 'historical')
        self.civilizations = kwargs.get('civilizations', [])
        self.seed = kwargs.get('seed', None)
        self.output_dir = kwargs.get('output_dir', 'output')
        self.verbose = kwargs.get('verbose', False) 