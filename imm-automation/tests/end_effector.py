from SERVER.website.assets.robot.end_effector import EndEffector

# Testing process
end_effector = EndEffector()
end_effector.pick_part()
end_effector.drop_part()
end_effector.cleanup()  # must add this after each calling of a function, otherwise the servo will not stop