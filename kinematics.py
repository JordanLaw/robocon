import math

def move_cal(f, s, r):
    L = 58.5    # (wheelbase, cm)
    W = 58.5    # (track width, cm)
    # L = 30    # (wheelbase, cm)
    # W = 24    # (track width, cm)
    R = math.sqrt(L**2 + W**2)

    FWD = f     # (forward/reverse command, -1 to +1)     (y-axis: go up or down)
    STR = s     # (strafe right command, -1 to +1)          (x-axis: go right or left)
    RCW = r     # (rotate clockwise command, -1 to +1)    (rotate)

    A = STR - RCW * (L/R)
    B = STR + RCW * (L/R)
    C = FWD - RCW * (W/R)
    D = FWD + RCW * (W/R)

    WS1 = math.sqrt(B**2 + C**2)    # front-right speed
    WS2 = math.sqrt(B**2 + D**2)    # front-left speed
    WS3 = math.sqrt(A**2 + D**2)    # back-left speed
    WS4 = math.sqrt(A**2 + C**2)    # back-right speed

    max_speed = max(WS1, WS2, WS3, WS4)

    if max_speed > 1:
        WS1 = WS1 / max_speed
        WS2 = WS2 / max_speed
        WS3 = WS3 / max_speed
        WS4 = WS4 / max_speed

    if C == 0 and B == 0:
        WA1 = 0
    else:
        WA1 = math.atan2(B, C) * 180 / math.pi

        if WA1 > 90:
            WA1 = -(WA1 - 90)
            WS1 = -WS1
        elif WA1 < -90:
            WA1 = -(WA1 + 90)
            WS1 = -WS1

    if D == 0 and B == 0:
        WA2 = 0
    else:
        WA2 = math.atan2(B, D) * 180 / math.pi

        if WA2 > 90:
            WA2 = -(WA2 - 90)
            WS2 = -WS2
        elif WA2 < -90:
            WA2 = -(WA2 + 90)
            WS2 = -WS2

    if A == 0 and D == 0:
        WA3 = 0
    else:
        WA3 = math.atan2(A, D) * 180 / math.pi

        if WA3 > 90:
            WA3 = -(WA3 - 90)
            WS3 = -WS3
        elif WA3 < -90:
            WA3 = -(WA3 + 90)
            WS3 = -WS3

    if A == 0 and C == 0:
        WA4 = 0
    else:
        WA4 = math.atan2(A, C) * 180 / math.pi

        if WA4 > 90:
            WA4 = -(WA4 - 90)
            WS4 = -WS4
        elif WA4 < -90:
            WA4 = -(WA4 + 90)
            WS4 = -WS4

    return WS1, WS2, WS3, WS4, WA1, WA2, WA3, WA4
