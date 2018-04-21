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
        "CurrentProtectionMaxChange" : "0.5",
        "UseUltrasound" : "no",
        "UltrasoundBuffer" : "1"}
    config["loggers"] = {
        "keys" : "root"}
    config["logger_root"] = {
        "level": "NOTSET",
        "handlers" : "warning, info, debug"}
    config["handlers"] = {
        "keys": "warning, info, debug"}
    config["handler_warning"] = {
        "class" : "FileHandler",
        "level" : "WARNING",
        "args" : "('logs/warning.txt',)",
        "formatter" : "default"}
    config["handler_info"] = {
        "class" : "FileHandler",
        "level" : "INFO",
        "args" : "('logs/info.txt',)",
        "formatter" : "default"}
    config["handler_debug"] = {
        "class" : "FileHandler",
        "level" : "DEBUG",
        "args" : "('logs/debug.txt',)",
        "formatter" : "default"}
    config["formatters"] = {
        "keys" : "default"}
    config["formatter_default"] = {
        "format" : "%(asctime)s - %(name)s - %(levelname)s - %(message)s"}

    with open(filePath, 'w') as configfile:
        config.write(configfile)