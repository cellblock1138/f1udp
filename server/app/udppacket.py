class UDPPacket(object):
    def __init__(self, data):
        self.m_time = data[0]
        self.m_lapTime = data[1]
        self.m_lapDistance = data[2]
        self.m_totalDistance = data[3]
        self.m_x = data[4] # World space position
        self.m_y = data[5]  # World space position
        self.m_z = data[6]  # World space position
        self.m_speed = data[7]  # Speed of car in meters per second!!! (NOT MPH... Idiots...)
        self.m_xv = data[8] # Velocity in world space
        self.m_yv = data[9] # Velocity in world space
        self.m_zv = data[10] # Velocity in world space
        self.m_xr = data[11] # World space right direction
        self.m_yr = data[12] # World space right direction
        self.m_zr = data[13] # World space right direction
        self.m_xd = data[14] # World space forward direction
        self.m_yd = data[15] # World space forward direction
        self.m_zd = data[16] # World space forward direction
        self.m_susp_pos = [data[17], data[18], data[19], data[20]] #[4] Note: All wheel arrays have the order: RL, RR, FL, FR
        self.m_susp_vel = [data[21], data[22], data[23], data[24]] #[4] 
        self.m_wheel_speed = [data[25], data[26], data[27], data[28]] #[4]
        self.m_throttle = data[29]
        self.m_steer = data[30]
        self.m_brake = data[31]
        self.m_clutch = data[32]
        self.m_gear = data[33]
        self.m_gforce_lat = data[34]
        self.m_gforce_lon = data[35]
        self.m_lap = data[36]  # Zero indexed it appears so +1
        self.m_engineRate = data[37]
        self.m_sli_pro_native_support = data[38] # SLI Pro support
        self.m_car_position = data[39]   # car race position
        self.m_kers_level = data[40] # kers energy left
        self.m_kers_max_level = data[41] # kers maximum energy
        self.m_drs = data[42] # 0 = off, 1 = on
        self.m_traction_control = data[43]   # 0 (off) - 2 (high)
        self.m_anti_lock_brakes = data[44]   # 0 (off) - 1 (on)
        self.m_fuel_in_tank = data[45]   # current fuel mass
        self.m_fuel_capacity = data[46]  # fuel capacity
        self.m_in_pits = data[47] # 0 = none, 1 = pitting, 2 = in pit area
        self.m_sector = data[48] # 0 = sector1, 1 = sector2, 2 = sector3
        self.m_sector1_time = data[49]   # time of sector1 (or 0)
        self.m_sector2_time = data[50]   # time of sector2 (or 0)
        self.m_brakes_temp = [data[51], data[52], data[53], data[54]] #[4] brakes temperature (centigrade)
        self.m_tyres_pressure = [data[55], data[56], data[57], data[58]]  #[4] tyres pressure PSI
        self.m_team_info = data[59]  # team ID 
        self.m_total_laps = data[60] # total number of laps in this race
        self.m_track_size = data[61] # track size meters
        self.m_last_lap_time = data[62]  # last lap time
        self.m_max_rpm = data[63] # cars max RPM, at which point the rev limiter will kick in
        self.m_idle_rpm = data[64]   # cars idle RPM
        self.m_max_gears = data[65]  # maximum number of gears
        self.m_sessionType = data[66] # 0 = unknown, 1 = practice, 2 = qualifying, 3 = race
        self.m_drsAllowed = data[67] # 0 = not allowed, 1 = allowed, -1 = invalid / unknown
        self.m_track_number = data[68]   # -1 for unknown, 0-21 for tracks
        self.m_vehicleFIAFlags = data[69] # -1 = invalid/unknown, 0 = none, 1 = green, 2 = blue, 3 = yellow, 4 = red
        self.m_era = data[70] # era, 2017 (modern) or 1980 (classic)
        self.m_engine_temperature = data[71]     # engine temperature (centigrade)
        self.m_gforce_vert = data[72]    # vertical g-force component
        self.m_ang_vel_x = data[73]  # angular velocity x-component
        self.m_ang_vel_y = data[74]  # angular velocity y-component
        self.m_ang_vel_z = data[75]  # angular velocity z-component
        self.m_tyres_temperature = [data[76], data[77], data[78], data[79]]   #[4] tyres temperature (centigrade)
        self.m_tyres_wear = [data[80], data[81], data[82], data[83]]  #[4] tyre wear percentage
        self.m_tyre_compound = data[84]  # compound of tyre - 0 = ultra soft, 1 = super soft, 2 = soft, 3 = medium, 4 = hard, 5 = inter, 6 = wet
        self.m_front_brake_bias = data[85]         # front brake bias (percentage)
        self.m_fuel_mix = data[86]                 # fuel mix - 0 = lean, 1 = standard, 2 = rich, 3 = max
        self.m_currentLapInvalid = data[87]     # current lap invalid - 0 = valid, 1 = invalid
        self.m_tyres_damage = [data[88], data[89], data[90], data[91]]    #[4] tyre damage (percentage)
        self.m_front_left_wing_damage = data[92] # front left wing damage (percentage)
        self.m_front_right_wing_damage = data[93]    # front right wing damage (percentage)
        self.m_rear_wing_damage = data[94]   # rear wing damage (percentage)
        self.m_engine_damage = data[95]  # engine damage (percentage)
        self.m_gear_box_damage = data[96]    # gear box damage (percentage)
        self.m_exhaust_damage = data[97] # exhaust damage (percentage)
        self.m_pit_limiter_status = data[98] # pit limiter status - 0 = off, 1 = on
        self.m_pit_speed_limit = data[99]    # pit speed limit in mph
        self.m_session_time_left = data[100]  # NEW: time left in session in seconds 
        self.m_rev_lights_percent = data[101]  # NEW: rev lights indicator (percentage)
        self.m_is_spectating = data[102]  # NEW: whether the player is spectating
        self.m_spectator_car_index = data[103]  # NEW: index of the car being spectatedself.
        # Car data
        self.m_num_cars = data[104] # number of cars in data
        self.m_player_car_index = data[105] # index of player's car in the arrayself.
        self.CarUDPData = [
                            data[106:124],
                            data[124:142],
                            data[142:160],
                            data[160:178],
                            data[178:196],
                            data[196:214],
                            data[214:232],
                            data[232:250],
                            data[250:268],
                            data[268:286],
                            data[286:304],
                            data[304:322],
                            data[322:340],
                            data[340:358],
                            data[358:376],
                            data[376:394],
                            data[394:412],
                            data[412:430],
                            data[430:448],
                            data[448:466]
                        ]
        self.m_yaw = data[466]  # NEW (v1.8)
        self.m_pitch = data[467]  # NEW (v1.8)
        self.m_roll = data[468]  # NEW (v1.8)
        self.m_x_local_velocity = data[469]          # NEW (v1.8) Velocity in local space
        self.m_y_local_velocity = data[470]          # NEW (v1.8) Velocity in local space
        self.m_z_local_velocity = data[471]          # NEW (v1.8) Velocity in local space
        self.m_susp_acceleration = [data[472], data[473], data[474], data[475]]   #[4] NEW (v1.8) RL, RR, FL, FR
        self.m_ang_acc_x = data[476] # NEW (v1.8) angular acceleration x-component
        self.m_ang_acc_y = data[477] # NEW (v1.8) angular acceleration y-component
        self.m_ang_acc_z = data[478] # NEW (v1.8) angular acceleration z-component




