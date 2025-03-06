import argparse
import json
from config.simulation_config import SimulationConfig
from core.simulation import Simulation
from utils.logger import setup_logger

def parse_args():
    parser = argparse.ArgumentParser(description='Civilization Simulation System')
    parser.add_argument('--config', type=str, default='config.json', help='Path to configuration file')
    parser.add_argument('--turns', type=int, help='Number of turns to simulate')
    parser.add_argument('--output', type=str, default='output.json', help='Output file path')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose logging')
    return parser.parse_args()

def load_config(config_path):
    with open(config_path, 'r', encoding='utf-8') as f:
        config_data = json.load(f)
    return SimulationConfig(**config_data)

def main():
    args = parse_args()
    
    # 设置日志
    logger = setup_logger(verbose=args.verbose)
    logger.info("Starting civilization simulation")
    
    # 加载配置
    config = load_config(args.config)
    if args.turns:
        config.max_turns = args.turns
    
    # 创建并运行模拟
    simulation = Simulation(config)
    result = simulation.run()
    
    # 保存结果
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    logger.info(f"Simulation completed. Results saved to {args.output}")

if __name__ == "__main__":
    main() 