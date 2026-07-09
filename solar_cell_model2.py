"""
Solar Panel Tilt Optimization
CCNY Calculus 1 Final Project - Montefiore Square

Simple model using basic Calculus 1 concepts:
- Continuous functions
- Derivatives (rate of change)
- Integrals (area under curve)
- Optimization (find maximum)
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

# Simple constants
PEAK_POWER = 800  # Maximum power at noon (Watts for 1 m² panel)

def solar_power(time, tilt=30):
    """
    Simplified model of solar power output vs time of day.
    
    Assumes a bell curve: power is 0 at sunrise/sunset,
    peaks at noon, affected by how well panel faces the sun.
    
    Power = (peak power) × sin(hour angle) × cos(angle difference)
    
    Args:
        time: Hour of day (0-24)
        tilt: Panel tilt angle in degrees (0 = flat, 90 = vertical)
    
    Returns:
        Power in Watts
    """
    # No sun before 6 AM or after 6 PM
    if time < 6 or time > 18:
        return 0
    
    # How high is the sun? (simplified: peaks at noon)
    # Height increases then decreases throughout the day
    hour_from_noon = time - 12
    sun_height = 70 - (hour_from_noon ** 2) / 2  # Parabola
    
    if sun_height <= 0:
        return 0
    
    # Convert to radians
    sun_height_rad = np.radians(sun_height)
    tilt_rad = np.radians(tilt)
    
    # Panel receives more power when it faces the sun directly
    # Angle between panel and sun
    angle_diff = abs(sun_height - tilt)
    angle_factor = max(0, np.cos(np.radians(angle_diff)))
    
    # Calculate power
    power = PEAK_POWER * np.sin(sun_height_rad) * angle_factor
    return max(0, power)


def total_daily_energy(tilt):
    """
    Calculate total energy produced in one day using INTEGRATION.
    
    Energy = ∫(6 to 18) Power(t, tilt) dt
    
    This integral represents the AREA under the power curve.
    More area = more energy.
    
    Args:
        tilt: Panel tilt angle in degrees
    
    Returns:
        Total energy in Watt-hours (Wh)
    """
    result, _ = quad(lambda t: solar_power(t, tilt), 6, 18)
    return result


def power_derivative(time, tilt, delta=0.01):
    """
    Calculate dP/dt using the definition of derivative:
    dP/dt = [P(t + delta) - P(t - delta)] / (2 * delta)
    
    This shows how fast power is changing.
    
    Args:
        time: Time of day
        tilt: Panel tilt angle
        delta: Small step for calculation
    
    Returns:
        dP/dt in W/hour
    """
    p_after = solar_power(time + delta, tilt)
    p_before = solar_power(time - delta, tilt)
    return (p_after - p_before) / (2 * delta)


def energy_derivative(tilt, delta=0.5):
    """
    Calculate dE/dθ (how energy changes with tilt angle):
    dE/dθ = [E(θ + delta) - E(θ - delta)] / (2 * delta)
    
    Args:
        tilt: Panel tilt angle
        delta: Small step for calculation
    
    Returns:
        dE/dθ in Wh per degree
    """
    e_after = total_daily_energy(tilt + delta)
    e_before = total_daily_energy(tilt - delta)
    return (e_after - e_before) / (2 * delta)


def find_best_tilt():
    """
    Find the OPTIMAL TILT ANGLE where dE/dθ = 0
    
    This uses the idea that at a maximum, the derivative = 0.
    By testing different tilt angles and finding where 
    the derivative changes from positive to negative,
    we find the optimal angle.
    
    Returns:
        Best tilt angle (degrees) and corresponding energy (Wh)
    """
    best_tilt = 0
    best_energy = 0
    
    # Test tilt angles from 0° to 80°
    for tilt in np.arange(0, 81, 1):
        energy = total_daily_energy(tilt)
        if energy > best_energy:
            best_energy = energy
            best_tilt = tilt
    
    return best_tilt, best_energy


# ============================================================================
# PLOTTING / VISUALIZATION
# ============================================================================

def plot_power_throughout_day():
    """Plot power output throughout one day at different tilt angles"""
    times = np.linspace(6, 18, 100)
    
    plt.figure(figsize=(10, 6))
    
    # Plot for three different tilt angles
    for tilt in [0, 30, 60]:
        powers = [solar_power(t, tilt) for t in times]
        plt.plot(times, powers, linewidth=2, label=f'Tilt = {tilt}°')
    
    plt.xlabel('Time of Day (hours)')
    plt.ylabel('Power (Watts)')
    plt.title('Solar Power Output Throughout the Day')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('power_vs_time.png', dpi=100)
    print("✓ Saved power_vs_time.png")
    plt.close()


def plot_energy_vs_tilt():
    """Plot total daily energy vs panel tilt angle"""
    tilts = np.linspace(0, 80, 40)
    energies = [total_daily_energy(t) for t in tilts]
    
    best_tilt, best_energy = find_best_tilt()
    
    plt.figure(figsize=(10, 6))
    plt.plot(tilts, energies, 'b-', linewidth=2, label='Daily Energy')
    plt.plot(best_tilt, best_energy, 'r*', markersize=20, 
             label=f'Optimal: {best_tilt}° ({best_energy:.0f} Wh)')
    
    plt.xlabel('Panel Tilt Angle (degrees)')
    plt.ylabel('Daily Energy (Wh)')
    plt.title('Total Energy vs Panel Tilt - FIND THE MAXIMUM')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('energy_vs_tilt.png', dpi=100)
    print("✓ Saved energy_vs_tilt.png")
    plt.close()


def plot_derivative_of_energy():
    """Show dE/dθ (derivative of energy vs tilt)"""
    tilts = np.linspace(0, 80, 30)
    derivatives = [energy_derivative(t) for t in tilts]
    
    best_tilt, _ = find_best_tilt()
    
    plt.figure(figsize=(10, 6))
    plt.plot(tilts, derivatives, 'g-', linewidth=2, label='dE/dθ')
    plt.axhline(y=0, color='k', linestyle='-', linewidth=1)
    plt.plot(best_tilt, 0, 'r*', markersize=20, 
             label=f'Zero at {best_tilt}° (optimal)')
    
    plt.xlabel('Panel Tilt Angle (degrees)')
    plt.ylabel('dE/dθ (Wh per degree)')
    plt.title('Derivative of Energy - Shows Where Maximum Is')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('derivative_vs_tilt.png', dpi=100)
    print("✓ Saved derivative_vs_tilt.png")
    plt.close()


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("SOLAR PANEL OPTIMIZATION - Calculus 1")
    print("="*60)
    
    # EXAMPLE 1: Power at different times
    print("\n1. POWER OUTPUT AT DIFFERENT TIMES (30° tilt)")
    print("-"*60)
    for hour in [8, 10, 12, 14, 16]:
        p = solar_power(hour, tilt=30)
        print(f"   {hour}:00 → Power = {p:.1f} W")
    
    # EXAMPLE 2: Energy for different tilts
    print("\n2. TOTAL DAILY ENERGY (using INTEGRATION)")
    print("-"*60)
    for tilt in [0, 15, 30, 45, 60, 75]:
        energy = total_daily_energy(tilt)
        print(f"   {tilt}° tilt → {energy:.0f} Wh")
    
    # EXAMPLE 3: Finding the best angle
    print("\n3. OPTIMIZATION - FINDING BEST TILT")
    print("-"*60)
    best_tilt, best_energy = find_best_tilt()
    print(f"\n   BEST TILT ANGLE: {best_tilt}°")
    print(f"   MAXIMUM ENERGY: {best_energy:.0f} Wh")
    print(f"\n   At the optimal angle, the derivative dE/dθ = 0")
    print(f"   This is where energy stops increasing!")
    
    # EXAMPLE 4: Show how derivative changes
    print("\n4. DERIVATIVE ANALYSIS")
    print("-"*60)
    print("   dE/dθ (Wh per degree) at different angles:")
    for tilt in [10, 20, 30, 40, 50]:
        deriv = energy_derivative(tilt)
        status = "still going up" if deriv > 1 else "coming down" if deriv < -1 else "MAXIMUM"
        print(f"   {tilt}° → dE/dθ = {deriv:7.2f}  ({status})")
    
    # Generate plots
    print("\n" + "="*60)
    print("Generating graphs...")
    print("="*60)
    
    plot_power_throughout_day()
    plot_energy_vs_tilt()
    plot_derivative_of_energy()
    
    print("\n✓ All done!")
    print("\nFiles created:")
    print("  • power_vs_time.png")
    print("  • energy_vs_tilt.png")
    print("  • derivative_vs_tilt.png")
    print()
