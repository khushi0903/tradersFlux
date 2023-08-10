from model import *
from app import *


risk_tolerance = 0.02  # 2% risk tolerance
position_size = 0.10    # 10% position size
entry_price = 150
take_profit = 160
stop_loss = 145
volume = 100
commission = 5
swap = 0.00

potential_profit = model_profit.predict([[entry_price, stop_loss, take_profit]])[0]
potential_loss = model_loss.predict([[entry_price, stop_loss, take_profit]])[0]

# Calculate risk exposure based on position size
risk_exposure = position_size * entry_price * volume

# Calculate risk-reward ratio
risk_reward_ratio = potential_profit / potential_loss

# Generate the risk management report
print("Risk Management Report for Simulated Trade\n")
print("Trade Details:")
print(f"Entry Price: ${entry_price:.2f} per share")
print(f"Take Profit (T/P): ${take_profit:.2f} per share")
print(f"Stop Loss (S/L): ${stop_loss:.2f} per share")
print(f"Volume: {volume} shares")
print(f"Commission: ${commission:.2f} per trade")
print(f"Swap: ${swap:.2f} (no overnight financing cost)\n")

print("User Inputs:")
print(f"Risk Tolerance: {risk_tolerance:.2%} (maximum acceptable loss per trade)")
print(f"Position Size: {position_size:.2%} (percentage of total capital per trade)\n")

print("Model-Generated Outputs:")
print(f"Risk Exposure: ${risk_exposure:.2f} ({risk_tolerance:.2%} of total capital)")
print(f"Risk-Reward Ratio: {risk_reward_ratio:.2f} (potential profit is {risk_reward_ratio:.2f} times the risk exposure)\n")

print("Simulated Trade Outcome:")
print("Based on the regression model and the user's inputs, the simulated trade outcome is as follows:\n")

# Scenario A (Take Profit is Hit)
if potential_profit >= risk_exposure:
    net_profit_a = potential_profit - risk_exposure
    print(f"Scenario A (Take Profit is Hit):")
    print(f"Exit Price: ${take_profit:.2f} per share")
    print(f"Gross Profit: ${potential_profit:.2f}")
    print(f"Net Profit: ${net_profit_a:.2f}")
    print(f"Profit Percentage: {net_profit_a / risk_exposure:.2%} (Net Profit / Risk Exposure)\n")
else:
    print("Scenario A (Take Profit is Hit): Take Profit level is not reached.\n")

# Scenario B (Stop Loss is Hit)
if potential_loss <= risk_exposure:
    net_loss_b = risk_exposure - potential_loss
    print(f"Scenario B (Stop Loss is Hit):")
    print(f"Exit Price: ${stop_loss:.2f} per share")
    print(f"Gross Loss: ${potential_loss:.2f}")
    print(f"Net Loss: ${net_loss_b:.2f}")
    print(f"Loss Percentage: {net_loss_b / risk_exposure:.2%} (Net Loss / Risk Exposure)\n")
else:
    print("Scenario B (Stop Loss is Hit): Stop Loss level is not reached.\n")
