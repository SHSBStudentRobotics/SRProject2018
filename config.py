import configparser, os

def getConfigSettings():
    if not os.path.isfile("config.ini"):
        generateConfigFile()
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config

def generateConfigFile():
    config = configparser.RawConfigParser()
    config["Hardware"] = {
            "SpeedIncreasePerCube" : "0.1",
            "BaseSpeed" : "0.6",
            "MaxDistForFullPower": "1",
            "ProportionalConstant" : "0.1",
            "IntegralConstant"  : "0.1",
            "DerivativeConstant" : "0.1",
            "InvertLeftMotor" : "no",
            "InvertRightMotor": "no",
            "LeftMotorNumber" : "0",
            "RightMotorNumber" : "1"}
    
    with open('config.ini', 'w') as configfile:
        config.write(configfile)