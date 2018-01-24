import math
import time
from action import *


MOTORRATIO = 1 #Speed of right wheel compared to left one.
BASESPEED = 40 #Speed of robot.
TURNSPEED = 1
MAXDIST = 200 #Distance that can be covered in between one camera update at full power.
MAXANGLE = 120 #Angle that can be convered between one camera update at full power.
POWERCHANGEDELAY = 0.2 #Number of seconds to wait between power shifts
    
def move(robot,action,tokens):
    
    CUBEMULTIPLIER = 1 + 0.5 * tokens #Compensate for drag of cube
    #Generates leftSpeed and rightSpeed from motor ratio(To go straight)
    if MOTORRATIO < 1:
        leftSpeed = BASESPEED
        rightSpeed = BASESPEED * MOTORRATIO  
    else:
        leftSpeed = BASESPEED / MOTORRATIO
        rightSpeed = BASESPEED ## At this point LeftSpeed / RightSpeed = MOTORRATIO
    
    if leftSpeed * CUBEMULTIPLIER < 100 and rightSpeed * CUBEMULTIPLIER < 100:
        leftSpeed *= CUBEMULTIPLIER
        rightSpeed *= CUBEMULTIPLIER #Apply CUBEMULTIPLIER if possible
    elif leftSpeed > rightSpeed:
        rightSpeed *= 100 / leftSpeed
        leftSpeed = 100
    elif rightSpeed > leftSpeed:
        leftSpeed *= 100 / rightSpeed
        rightSpeed = 100
    
    if action.type == "move":
        if action.dist < MAXDIST * (BASESPEED/100.0): #If distance is too short
            multiplier = action.dist / (MAXDIST * (BASESPEED/100.0))
            leftSpeed *= multiplier
            rightSpeed *= multiplier
            
        turn = clamp(float(action.angle)/ float(MAXANGLE),-1,1) #Proportion to turn
        if turn < 0: #Turn left
            print("Turn left")
            ###robot.motors[0].m0.power = leftSpeed * (1 + turn) / TURNSPEED
            powerMotor(robot, 0, leftSpeed * (1 + turn) / TURNSPEED)
            ###robot.motors[0].m1.power = rightSpeed
            powerMotor(robot, 1, rightSpeed)

                
            print("left speed: " + str(leftSpeed * (1 + turn) / TURNSPEED))
            print("right speed: " + str(rightSpeed))
        elif turn > 0: #Turn right
            print("Turn right")
            ###robot.motors[0].m0.power = leftSpeed
            powerMotor(robot, 0, leftSpeed)
            ###robot.motors[0].m1.power = rightSpeed * (1 - turn) / TURNSPEED
            powerMotor(robot, 1, rightSpeed * (1 - turn) / TURNSPEED)
                
            print("left speed: " + str(leftSpeed * (1 + turn) / TURNSPEED))
            print("right speed: " + str(rightSpeed))
        else:
            ###robot.motors[0].m0.power = leftSpeed
            powerMotor(robot, 0, leftSpeed)

            
            ###robot.motors[0].m1.power = rightSpeed
            powerMotor(robot, 1, rightSpeed)

                
    elif action.type == "stop":
        ###robot.motors[0].m0.power = 0
        LChange = powerMotor(robot, 0, 0)
        ###robot.motors[0].m1.power = 0
        RChange = powerMotor(robot, 1, 0)

        
        
    elif action.type == "turn":
        
        if action.angle < 0:
            leftSpeed *= -1
        else:
            rightSpeed *= -1
        
        if action.angle < MAXANGLE:
            proportion = clamp(float(action.angle)/float(MAXANGLE) , -1 , 1) #Generate speed multiplier
            leftSpeed *= proportion
            rightSpeed *= proportion
            
        ###robot.motors[0].m0.power = leftSpeed
        powerMotor(robot, 0, leftSpeed)
        ###robot.motors[0].m1.power = rightSpeed
        powerMotor(robot, 1, rightSpeed)
            
            
        
            
    
def clamp(val,minimum,maximum):
    if val < minimum:
        return minimum
    if val > maximum:
        return maximum
    return val

MotorList = [0,0] # Both motors start at 0
MAXSAFECHANGE = 0.5 # Adjust as needed

def powerMotor(SInstance, MotorToChange, Value):
    # SInstance = Self instance, i.e. The robot instance from the API
    # MotorToChange = The index of the motor being powered
    # Value = The value of the change being done   

    if Value == "coast": Value = 0 #Change to brake
    OldValue = Value

    if abs(Value - MotorList[MotorToChange]) > MAXSAFECHANGE:
        if Value - MotorList[MotorToChange] >= 0: Value = MotorList[MotorToChange] + MAXSAFECHANGE
        if Value - MotorList[MotorToChange] < 0: Value = MotorList[MotorToChange] - MAXSAFECHANGE

    Value = clamp(Value, -1, 1)

    # Value is now acceptable
        
    MotorList[MotorToChange] = Value
    if MotorToChange == 0: SInstance.motor_board.m0 = Value
    if MotorToChange == 1: SInstance.motor_board.m1 = Value

    if Value != OldValue: return False
    return True

    #Returns whether or not the value requested is the new power
    
