"""
Solar Cell Placement Effectiveness Model
CCNY Calculus 1 Final Project - Montefiore Square Redesign

This module models the effectiveness of solar panel placement using calculus principles:
- Solar irradiance as a function of time and angle
- Optimization of panel placement
- Energy production estimation
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from scipy.integrate import quad, dblquad

# Constants
LATITUDE = 40.8  # NYC latitude in degrees
SOLAR_CONSTANT = 1361  # W/m^2 (solar constant)
MONTEFIORE_WIDTH = 100  # meters (estimated)
MONTEFIORE_LENGTH = 150  # meters (estimated)

def solar_declination(day_of_year):
    """
    Calculate solar declination angle (in radians)
    Derived from Earth's axial tilt using Fourier approximation
    
    Args:
        day_of_year: Day number (1-365)
    
    Returns:
        Declination angle in radians
    """
    # Fourier approximation of declination
    declination_rad = 0.40910518 - 22.95 * np.cos((day_of_year + 10.9) * np.pi / 173)
    return np.radians(declination_rad)


def hour_angle(time_hours, solar_noon=12):
    """
    Calculate hour angle of sun (in radians)
    15 degrees per hour rotation
    
    Args:
        time_hours: Time of day (0-24, float)
        solar_noon: Time of solar noon (typically ~12)
    
    Returns:
        Hour angle in radians
    """
    return np.radians(15 * (time_hours - solar_noon))


def solar_elevation_angle(latitude, declination, hour_angle_rad):
    """
    Calculate sun elevation angle above horizon (in radians)
    Using spherical trigonometry formula
    
    Args:
        latitude: Observer latitude in radians
        declination: Solar declination in radians
        hour_angle_rad: Hour angle in radians
    
    Returns:
        Elevation angle in radians
    """
    sin_elevation = (np.sin(latitude) * np.sin(declination) + 
                     np.cos(latitude) * np.cos(declination) * np.cos(hour_angle_rad))
    elevation = np.arcsin(np.clip(sin_elevation, -1, 1))
    return elevation


def solar_azimuth_angle(latitude, declination, hour_angle_rad, elevation):
    """
    Calculate solar azimuth angle (0° = North, 90° = East, 180° = South)
    
    Args:
        latitude: Observer latitude in radians
        declination: Solar declination in radians
        hour_angle_rad: Hour angle in radians
        elevation: Solar elevation angle in radians
    
    Returns:
        Azimuth angle in radians
    """
    numerator = np.sin(hour_angle_rad)
    denominator = (np.cos(hour_angle_rad) * np.sin(latitude) - 
                   np.tan(declination) * np.cos(latitude))
    azimuth = np.arctan2(numerator, denominator)
    return azimuth


def incident_angle(panel_tilt, panel_azimuth, solar_elevation, solar_azimuth):
    """
    Calculate angle of incidence on tilted panel surface
    Using vector dot product of surface normal and solar direction
    
    Args:
        panel_tilt: Panel tilt angle from horizontal (radians)
        panel_azimuth: Panel azimuth direction (radians)
        solar_elevation: Sun elevation angle (radians)
        solar_azimuth: Sun azimuth angle (radians)
    
    Returns:
        Angle of incidence in radians (0 = perpendicular, π/2 = grazing)
    """
    # Surface normal vector (pointing toward sun)
    normal_z = np.cos(panel_tilt)
    normal_xy = np.sin(panel_tilt)
    normal_x = normal_xy * np.cos(panel_azimuth)
    normal_y = normal_xy * np.sin(panel_azimuth)
    
    # Solar direction vector
    solar_z = np.sin(solar_elevation)
    solar_xy = np.cos(solar_elevation)
    solar_x = solar_xy * np.cos(solar_azimuth)
    solar_y = solar_xy * np.sin(solar_azimuth)
    
    # Dot product (cosine of incidence angle)
    cos_incident = (normal_x * solar_x + normal_y * solar_y + normal_z * solar_z)
    cos_incident = np.clip(cos_incident, 0, 1)  # Only receive light from front
    
    incident = np.arccos(cos_incident)
    return incident


def panel_efficiency(incident_angle_rad, temp_c=25):
    """
    Calculate panel efficiency factor based on incidence angle and temperature
    
    Args:
        incident_angle_rad: Angle of incidence in radians
        temp_c: Panel temperature in Celsius
    
    Returns:
        Efficiency factor (0-1)
    """
    # Cosine loss (angle of incidence loss)
    cos_loss = np.cos(incident_angle_rad)
    
    # Temperature coefficient (efficiency decreases with temperature)
    # Typical silicon panels: -0.4% efficiency per degree C above 25°C
    temp_coeff = 1 - 0.004 * (temp_c - 25)
    
    # Combined efficiency
    efficiency = cos_loss * temp_coeff
    return np.clip(efficiency, 0, 1)


def daily_energy_production(day_of_year, panel_tilt, panel_azimuth, panel_area=1.0):
    """
    Calculate total daily energy production using integration
    
    Args:
        day_of_year: Day number (1-365)
        panel_tilt: Panel tilt angle (radians)
        panel_azimuth: Panel azimuth (radians)
        panel_area: Panel area in m^2
    
    Returns:
        Daily energy in kWh
    """
    latitude_rad = np.radians(LATITUDE)
    declination = solar_declination(day_of_year)
    
    def irradiance_at_time(time_hours):
        """Irradiance integrated over panel area at given time"""
        h_angle = hour_angle(time_hours)
        elevation = solar_elevation_angle(latitude_rad, declination, h_angle)
        
        # No sun below horizon
        if elevation < 0:
            return 0
        
        azimuth = solar_azimuth_angle(latitude_rad, declination, h_angle, elevation)
        inc_angle = incident_angle(panel_tilt, panel_azimuth, elevation, azimuth)
        efficiency = panel_efficiency(inc_angle)
        
        # Direct normal irradiance (approximate, clear sky)
        air_mass = 1 / np.cos(np.pi/2 - elevation)
        air_mass = np.clip(air_mass, 1, 10)  # Limit to valid range
        dni = SOLAR_CONSTANT * np.exp(-0.7 * air_mass ** 0.678)
        
        # Horizontal component
        irradiance = dni * np.cos(inc_angle) * efficiency
        return irradiance * panel_area
    
    # Integrate over daylight hours (6 AM to 6 PM)
    energy_wh, _ = quad(irradiance_at_time, 6, 18)
    energy_kwh = energy_wh / 1000  # Convert Wh to kWh
    
    return energy_kwh


def optimize_panel_placement(panel_area=1.0, day_of_year=172):
    """
    Optimize panel tilt and azimuth for maximum annual energy production
    Uses scipy optimization
    
    Args:
        panel_area: Panel area in m^2
        day_of_year: Reference day for optimization (default: June 21 - summer solstice)
    
    Returns:
        Optimal tilt angle (degrees), optimal azimuth (degrees), max energy (kWh)
    """
    def negative_energy(params):
        tilt_rad = np.radians(params[0])
        azimuth_rad = np.radians(params[1])
        energy = daily_energy_production(day_of_year, tilt_rad, azimuth_rad, panel_area)
        return -energy  # Negative because we're minimizing
    
    # Initial guess: 35° tilt, 180° azimuth (facing south)
    initial_guess = [35, 180]
    
    # Constraints: tilt 0-90°, azimuth 0-360°
    bounds = [(0, 90), (0, 360)]
    
    result = minimize(negative_energy, initial_guess, bounds=bounds, method='L-BFGS-B')
    
    optimal_tilt = result.x[0]
    optimal_azimuth = result.x[1]
    max_energy = -result.fun
    
    return optimal_tilt, optimal_azimuth, max_energy


if __name__ == "__main__":
    print("Solar Cell Placement Effectiveness Model")
    print("=" * 50)
    
    # Test: Find optimal placement for summer solstice
    print("\nOptimizing for June 21 (Summer Solstice)...")
    tilt, azimuth, energy = optimize_panel_placement()
    print(f"Optimal Tilt: {tilt:.2f}°")
    print(f"Optimal Azimuth: {azimuth:.2f}° (0°=North, 180°=South)")
    print(f"Expected Daily Energy: {energy:.4f} kWh")
    
    print("\nModel setup complete!")
