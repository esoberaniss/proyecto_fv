def annual_insolation(irradiance, h=1/6):
    integral = 0
    for i in range(len(irradiance)-1):
        integral += (irradiance[i] + irradiance[i+1]) * h / 2
    return integral