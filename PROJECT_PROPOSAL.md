# CCNY Calculus 1 Final Project: Solar Cell Placement on Montefiore Square

## Project Overview
This project models the effectiveness of solar panel placement on Montefiore Square as part of its redesign, using calculus principles for optimization and energy production analysis.

## Mathematical Concepts Used

### 1. **Trigonometry & Spherical Geometry**
- Solar position calculation (declination, hour angle, elevation, azimuth)
- Angle of incidence on tilted surfaces using dot products
- Accounting for Earth's axial tilt and rotation

**Relevant Calculus:** Derivatives to find maximum elevation angle; arc sine/cosine for angle transformations

### 2. **Integration (Definite Integrals)**
- **Daily Energy Production**: Integrate irradiance over daylight hours
$$E_{daily} = \int_6^{18} I(t) \cdot A \cdot \cos(\theta(t)) \, dt$$
where $I(t)$ = solar irradiance, $A$ = panel area, $\theta(t)$ = angle of incidence

- **Annual Energy Production**: Sum daily energy across 365 days with seasonal variations
$$E_{annual} = \sum_{d=1}^{365} E_{daily}(d)$$

### 3. **Optimization (Calculus of Variations)**
- **Maximize Energy**: Find optimal tilt angle and azimuth direction
$$\max_{(\alpha, \beta)} E(day, \alpha, \beta)$$
subject to $0° \leq \alpha \leq 90°$ and $0° \leq \beta \leq 360°$

- **Use Lagrange Multipliers** for constrained optimization (e.g., maximum area constraint)

### 4. **Multivariable Calculus**
- Energy as function of: $E(day, tilt, azimuth, temperature)$
- Partial derivatives: $\frac{\partial E}{\partial \text{tilt}}$, $\frac{\partial E}{\partial \text{azimuth}}$
- Gradient descent for numerical optimization

### 5. **Differential Equations (Optional Advanced)**
- Model shadow movement across the square using parametric curves
- Temperature variation throughout the day as ODE

## Physical Model Components

### Solar Position (Spherical Trigonometry)
The sun's position is determined by:
- **Declination** $\delta$: Earth's axial tilt angle
- **Hour Angle** $H$: Rotation angle based on time of day
- **Elevation** $\alpha_s$: Angle above horizon
- **Azimuth** $\gamma_s$: Compass direction

$$\sin(\alpha_s) = \sin(\phi) \sin(\delta) + \cos(\phi) \cos(\delta) \cos(H)$$

where $\phi$ = observer latitude (40.8° for NYC)

### Angle of Incidence
For a tilted solar panel with normal vector $\vec{n}$ and incident solar direction $\vec{s}$:
$$\cos(\theta) = \vec{n} \cdot \vec{s}$$

### Energy Yield
Direct normal irradiance follows the equation:
$$I_{dni} = I_0 \cdot e^{-0.7 \cdot (AM)^{0.678}}$$

where $I_0$ = solar constant, $AM$ = air mass (function of elevation angle)

### Panel Efficiency
$$\eta = \cos(\theta) \cdot \left(1 - 0.004 \cdot \Delta T\right)$$

where $\Delta T$ = temperature rise above 25°C

## Project Deliverables

1. **Mathematical Model** (`solar_cell_model.py`)
   - Implement solar position calculations
   - Energy integration functions
   - Optimization algorithms

2. **Analysis & Visualization**
   - Daily energy production curves
   - Annual production by tilt angle
   - Heatmap of optimal placement on the square
   - Comparison: south-facing vs. optimal vs. flat roof

3. **Final Report** (`REPORT.md`)
   - Derivation of key formulas
   - Calculus techniques used
   - Numerical results for Montefiore Square
   - Recommendations for optimal configuration

4. **Presentation**
   - Visual diagrams of solar geometry
   - Energy production graphs
   - Cost-benefit analysis with integration

## Key Questions to Answer

1. **Optimization**: What tilt angle and azimuth maximize annual energy production for NYC?
2. **Seasonal Variation**: How does optimal angle change throughout the year?
3. **Spatial Distribution**: Where on Montefiore Square should panels be placed?
4. **Economic Efficiency**: What is the payback period based on energy production?

## References

- Spencer, J. W. (1971). Fourier series representation of the position of the sun
- Duffie, J. A., & Beckman, W. A. (2013). Solar engineering of thermal processes
- NREL Solar Position Algorithm
- NYC Solar Energy Statistics & Incentives

## Next Steps

1. ✅ Create Python model with solar calculations
2. ⬜ Generate energy production curves for different configurations
3. ⬜ Analyze seasonal variations
4. ⬜ Create visualization maps of Montefiore Square
5. ⬜ Write detailed mathematical report
