import configparser, os

def getConfigSettings(filePath = "config.ini"):
    if not os.path.isfile(filePath):
        generateConfigFile(filePath)
    config = configparser.ConfigParser()
    config.read(filePath)
    return config

def generateConfigFile(filePath = "config.ini"):
    config = configparser.RawConfigParser()
    config["Movement"] = {
            "SpeedIncreasePerCube" : "0.1",
            "BaseSpeed" : "0.6",
            "MaxDistForFullPower": "1",
            "ProportionalConstant" : "0.1",
            "IntegralConstant"  : "0.1",
            "DerivativeConstant" : "0.1"}
    config["Hardware"] = {
            "InvertLeftMotor" : "no",
            "InvertRightMotor": "no",
            "LeftMotorNumber" : "0",
            "RightMotorNumber" : "1",
            "CurrentProtectionMaxChange" : "0.5"}
    
    with open(filePath, 'w') as configfile:
        config.write(configfile)