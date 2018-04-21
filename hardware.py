import math, time, logging
from action import *

#global variables for the PID controller.
prevTime = time.time()
prevError = 0
integral = 0
turnValue = 0 #This value is added to the right hand motor, subtracted from the left hand motor.

logger = logging.getLogger(__name__)

def resetSetpoint():
    global turnValue
    turnValue = 0

def moveLogic(robot, config, averageSpeed, action):
    #lowers speed when close to target , rarely used.
        if action.dist < float(config["Movement"]["MaxDistForFullPower"]):
            averageSpeed *= action.dist / float(config["Movement"]["MaxDistForFullPower"])
            logger.debug("Move speed lowered to " + str(averageSpeed))

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

        logger.info("PID info: P: {0} I: {1} D: {2} TurnValue: {3} dt: {4}".format(proportionalTerm ,integralTerm ,derivativeTerm , turnValue, dt))

        setBothMotors(robot,config,min(1,averageSpeed + turnValue), min(1,averageSpeed - turnValue))

def turnLogic(robot, config, averageSpeed, action):
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

    
def move(robot,action,tokens, config):
    logger.info("Move executed with action: Type: {0} Distance: {1} Angle: {2}".format(action.type, action.dist, action.angle))

    #The increase in speed because of the number of cubes.
    CUBE_SPEED_INCREASE = float(config["Movement"]["SpeedIncreasePerCube"]) * tokens #Compensate for drag of cube

    averageSpeed = CUBE_SPEED_INCREASE + float(config["Movement"]["BaseSpeed"])

    logger.debug("Move speed: {0} NumberOfCubes: {1} CubeSpeedIncrease: {2}".format(averageSpeed, tokens, CUBE_SPEED_INCREASE))
    
    if action.type == "move":
        #lowers speed when close to target , rarely used.
        #if action.dist < float(config["Movement"]["MaxDistForFullPower"]):
        #    averageSpeed *= action.dist / float(config["Movement"]["MaxDistForFullPower"])
        #    logger.debug("Move speed lowered to " + str(averageSpeed))

        #Start of PID controller.
        #calculates deltatime, cant be 0.
        #global prevTime
        #dt = max(0.0000001, time.time() - prevTime)
        #prevTime = time.time()

        #integral only measured when angle < 5 to avoid integral windup
        #global integral
        #if math.fabs(action.angle) < 5:
        #    integral += dt * action.angle

        #proportionalTerm = float(config["Movement"]["ProportionalConstant"]) * action.angle
        #integralTerm = float(config["Movement"]["IntegralConstant"]) * integral
        #derivativeTerm = float(config["Movement"]["DerivativeConstant"]) * ((action.angle - prevError) /dt)

        #global turnValue
        #turnValue += proportionalTerm + integralTerm + derivativeTerm
        #End of PID controller.

        #Limits the turn value such that both values can not be out of bounds.
        #if turnValue < 0 and averageSpeed + turnValue < -1:
        #    turnValue = -(averageSpeed + 1)
        #elif turnValue > 0 and averageSpeed - turnValue < -1:
        #    turnValue = averageSpeed + 1

        #logger.info("PID info: P: {0} I: {1} D: {2} TurnValue: {3} dt: {4}".format(proportionalTerm ,integralTerm ,derivativeTerm , turnValue, dt))

        #setBothMotors(robot,config,min(1,averageSpeed + turnValue), min(1,averageSpeed - turnValue))

        moveLogic(robot, config, averageSpeed, action)
               
    elif action.type == "stop":
        setBothMotors(robot, config, 0, 0) 
        
    elif action.type == "turn":
        #leftSpeed = averageSpeed
        #rightSpeed = averageSpeed
        #if action.angle < 0:
        #    leftSpeed *= -1
        #else:
        #    rightSpeed *= -1
        
        #if math.fabs(action.angle) < 45:
            #Not updated to PID system as turning is typically only done before moving
            #when the angle is too large. Therefore it does not handle movements that need
            #precision.
         #   proportion = clamp(math.fabs(action.angle)/45, -1 , 1) #Generate speed multiplier
         #   leftSpeed *= proportion
          #  rightSpeed *= proportion
            
        #setBothMotors(robot,config,leftSpeed,rightSpeed)              
        turnLogic(robot, config, averageSpeed, action)

    elif action.type == "reverse":
        setBothMotors(robot, config, -averageSpeed, -averageSpeed)

    elif action.type == "reverseTurn":
        turnLogic(robot, config, averageSpeed, action)
        time.sleep(0.5)
        moveLogic(robot, config, averageSpeed, action)
        time.sleep(0.5)
        turnLogic(robot, config, averageSpeed, action)
        

def setBothMotors(robot,config,left,right):
    if config["Hardware"]["InvertLeftMotor"].lower() in ["n","no","0"]:
        powerMotor(robot, int(config["Hardware"]["LeftMotorNumber"]), left + 0.2 ,config)
    else:
        powerMotor(robot, int(config["Hardware"]["LeftMotorNumber"]), -left - 0.2, config)
    
    if config["Hardware"]["InvertRightMotor"].lower() in ["n","no","0"]:
        powerMotor(robot, int(config["Hardware"]["RightMotorNumber"]), right, config)
    else:
        powerMotor(robot, int(config["Hardware"]["RightMotorNumber"]), -right, config)
    logger.info("Motors set to Left: {0} Right:  {1} M0: {2} M1: {3}".format(left,right,robot.motor_board.m0,robot.motor_board.m1))

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
    
def getZone(robot):
    return robot.zone