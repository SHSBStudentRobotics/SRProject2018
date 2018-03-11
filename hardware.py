import math
import time
from action import *

#global variables for the PID controller.
prevTime = time.time()
prevError = 0
integral = 0
turnValue = 0 #This value is added to the right hand motor, subtracted from the left hand motor.
    
def move(robot,action,tokens, config):
    #The increase in speed because of the number of cubes.
    CUBE_SPEED_INCREASE = float(config["Movement"]["SpeedIncreasePerCube"]) * tokens #Compensate for drag of cube

    averageSpeed = CUBE_SPEED_INCREASE + float(config["Movement"]["BaseSpeed"])
    
    if action.type == "move":
        #lowers speed when close to target , rarely used.
        if action.dist < float(config["Movement"]["MaxDistForFullPower"]):
            averageSpeed *= action.dist / float(config["Movement"]["MaxDistForFullPower"])

        #Start of PID controller.
        #calculates deltatime, cant be 0.
        global prevTime
        dt = max(0.0000001, time.time() - prevTime)
        prevTime = time.time()

        #integral only measured when angle < 5 to avoid integral windup
        global integral
        if math.fabs(action.angle) < 5:
            integral += dt * action.angle

        proportionalTerm = float(config["Movement"]["ProportionalConstant"]) * action.angle
        integralTerm = float(config["Movement"]["IntegralConstant"]) * integral
        derivativeTerm = float(config["Movement"]["DerivativeConstant"]) * ((action.angle - prevError) /dt)

        global turnValue
        turnValue += proportionalTerm + integralTerm + derivativeTerm
        #End of PID controller.

        #Limits the turn value such that both values can not be out of bounds.
        if turnValue < 0 and averageSpeed + turnValue < -1:
            turnValue = -(averageSpeed + 1)
        elif turnValue > 0 and averageSpeed - turnValue < -1:
            turnValue = averageSpeed + 1

        setBothMotors(robot,config,min(1,averageSpeed - turnValue), min(1,averageSpeed + turnValue))
                
    elif action.type == "stop":
        powerMotor(robot, 0, 0, config)
        powerMotor(robot, 1, 0, config)  
        
    elif action.type == "turn":
        leftSpeed = averageSpeed
        rightSpeed = averageSpeed
        if action.angle < 0:
            leftSpeed *= -1
        else:
            rightSpeed *= -1
        
        if math.fabs(action.angle) < 45:
            #Not updated to PID system as turning is typically only done before moving
            #when the angle is too large. Therefore it does not handle movements that need
            #precision.
            proportion = clamp(math.fabs(action.angle)/45, -1 , 1) #Generate speed multiplier
            leftSpeed *= proportion
            rightSpeed *= proportion
            
        setBothMotors(robot,config,leftSpeed,rightSpeed)              
        
def setBothMotors(robot,config,left,right):
    if config["Hardware"]["InvertLeftMotor"].lower() in ["n","no","0"]:
        powerMotor(robot, int(config["Hardware"]["LeftMotorNumber"]), left, config)
    else:
        powerMotor(robot, int(config["Hardware"]["LeftMotorNumber"]), -left, config)
    
    if config["Hardware"]["InvertRightMotor"].lower() in ["n","no","0"]:
        powerMotor(robot, int(config["Hardware"]["RightMotorNumber"]), right, config)
    else:
        powerMotor(robot, int(config["Hardware"]["RightMotorNumber"]), -right, config)
    
def clamp(val,minimum,maximum):
    if val < minimum:
        return minimum
    if val > maximum:
        return maximum
    return val

MotorList = [0,0] # Both motors start at 0

def powerMotor(SInstance, MotorToChange, Value, config):
    # SInstance = Self instance, i.e. The robot instance from the API
    # MotorToChange = The index of the motor being powered
    # Value = The value of the change being done   

    if Value == "coast": Value = 0 #Change to brake
    OldValue = Value

    if abs(Value - MotorList[MotorToChange]) > float(config["Hardware"]["CurrentProtectionMaxChange"]):
        if Value - MotorList[MotorToChange] >= 0: Value = MotorList[MotorToChange] + float(config["Hardware"]["CurrentProtectionMaxChange"])
        if Value - MotorList[MotorToChange] < 0: Value = MotorList[MotorToChange] - float(config["Hardware"]["CurrentProtectionMaxChange"])

    Value = clamp(Value, -1, 1)

    # Value is now acceptable
        
    MotorList[MotorToChange] = Value
    if MotorToChange == 0: SInstance.motor_board.m0 = Value
    if MotorToChange == 1: SInstance.motor_board.m1 = Value

    if Value != OldValue: return False
    return True

    #Returns whether or not the value requested is the new power
    
