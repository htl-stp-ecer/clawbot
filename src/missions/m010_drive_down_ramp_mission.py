from raccoon import *

from src.hardware.defs import Defs
from src.kinematics.arm import arm


def line_follow():
    return strafe_follow_line_single(
        Defs.front_left_light_sensor,
        speed=1,
        side=LineSide.RIGHT,
        kp=0.4,
        ki=0.3,
        kd=0.0,
    )


class M010DriveDownRampMission(Mission):
    def sequence(self) -> Sequential:
        return seq([
            switch_calibration_set("default"),
            mark_heading_reference(),

            #background(
            #    wait_for_button("visit www.htlstp.ac.at"),
            #),

            background(
                Defs.arm_claw.p90deg(),
            ),

            line_follow().until(
                after_cm(25)
            ),

            spline(
                (0, -9, 0),
                (10, -9, 0),
            ),

            Defs.arm_claw.soft_close(),
            arm.move_angles(0, 55, -30),

            parallel(
                drive_backward(40),
                seq([
                    wait_for_seconds(0.5),
                    arm.move_angles(100, 90, -60),
                    Defs.arm_claw.p90deg(),
                    wait_for_seconds(0.2),
                    arm.move_angles(0, 90, -40),
                ])
            ),

        ])
