MotorList = [0,0] # Pull this from motors
MAXSAFECHANGE = 0.5

def PowerMotor(SInstance, MotorToChange, Value):
    # SInstance = Self instance, i.e. The robot instance from the API
    # MotorToChange = The index of the motor being powered
    # Value = The value of the change being done

    if abs(Value - MotorList[MotorToChange]) > MAXSAFECHANGE:
        if Value >= 0: Value = MotorList[MotorToChange] + MAXSAFECHANGE
        if Value < 0: Value = MotorList[MotorToChange] - MAXSAFECHANGE

    if Value > 1: Value = 1
    if Value < -1: Value = -1

    # Value is now acceptable
        
    MotorList[MotorToChange] = Value
    if MotorToChange == 0: SInstance.motor_board.m0 = Value
    if MotorToChange == 1: SInstance.motor_board.m1 = Value


    
